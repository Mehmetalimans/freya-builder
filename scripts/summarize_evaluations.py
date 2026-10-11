"""Publish evaluation evidence without customer variables, transcripts or credentials."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from builder.evaluate import validate_results
from builder.runtime import write_json


def summarize(directory):
    directory = Path(directory)
    build = json.loads((directory / "result.json").read_text(encoding="utf-8"))
    recovered = directory / "evaluation.recovered.json"
    evaluation = json.loads((recovered if recovered.exists() else directory / "evaluation.json").read_text(encoding="utf-8"))
    result = {"run_id": directory.name, "builder_version": build["builder_version"],
              "workflow_sha256": build.get("workflow_sha256"), "platform_version": build.get("platform_version"),
              **{key: evaluation.get(key) for key in ("status", "brief", "split", "reps", "style", "case_ids", "seconds",
                  "benchmark_success", "credits_before", "credits_after", "observed_balance_delta_usd", "actual_cost_usd")}}
    history = directory / "simulation-history.json"
    result["simulations"] = json.loads(history.read_text()) if history.exists() else []
    result["recovered_read_only"] = evaluation.get("recovered_read_only", False)
    telemetry_path = directory / "evaluation.telemetry.json"
    telemetry = json.loads(telemetry_path.read_text(encoding="utf-8")) if telemetry_path.exists() else {}
    result["tool_telemetry"] = {"calls_observed": len(telemetry),
        "completions_including_workflow_end": sum(t["observed_tool_completions"] for t in telemetry.values()),
        "failed_result_events": sum(t["observed_failed_tool_results"] for t in telemetry.values())}
    infrastructure = directory / "evaluation.infrastructure.json"
    if infrastructure.exists(): result["infrastructure"] = json.loads(infrastructure.read_text(encoding="utf-8"))
    if evaluation["status"] != "measured":
        result["error"] = evaluation.get("error")
        return result
    report = evaluation["results"]
    validate_results(report, evaluation["case_ids"], evaluation["reps"])
    rows = [row for repeat in report["all_rows"] for row in repeat]
    result.update(passed=report["passed"], total=report["total"],
                  successful_call_runs=sum(row["pass"] for row in rows), total_call_runs=len(rows),
                  cases=report["final"],
                  failures=[{"repetition": i+1, "id": row["id"], "reasons": row["failed"]}
                            for i, repeat in enumerate(report["all_rows"]) for row in repeat if not row["pass"]])
    latency = [row["slowest_turn_s"] for row in rows if "slowest_turn_s" in row]
    result["latency"] = {"calls_observed": len(latency), "worst_turn_seconds": max(latency, default=None)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    results = [summarize(path) for path in args.runs]
    write_json(args.out, {"scope": "Public practice only; not hidden final benchmark",
        "cost_note": "Balance snapshots can include other workspace activity; actual invoices are unknown.",
        "evaluations": results})
    print(json.dumps({"report": str(args.out), "evaluations": len(results)}))


if __name__ == "__main__":
    main()
