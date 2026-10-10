"""Publish evaluation evidence without customer variables, transcripts or credentials."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from builder.evaluate import validate_results
from builder.runtime import write_json


def sentiment_summary(directory, rows):
    buckets = {k:0 for k in ('very-unhappy','unhappy','neutral','happy','very-happy')}
    for row in rows:
        path = Path(directory)/('call-' + str(row.get('call_id')) + '.json')
        if not path.exists(): continue
        call = json.loads(path.read_text(encoding='utf-8'))
        analysis = call.get('analysis') or {}
        label = analysis.get('sentiment') if isinstance(analysis,dict) else None
        if isinstance(label,str) and label in buckets: buckets[label] += 1
    labeled = sum(buckets.values())
    return {'status':'measured_on_labeled_calls' if labeled else 'unavailable_no_sentiment_labels',
            'total_call_runs':len(rows),'labeled_calls':labeled,'unlabeled_calls':len(rows)-labeled,
            'buckets':buckets,'happy_fraction_of_labeled':(buckets['happy']+buckets['very-happy'])/labeled if labeled else None,
            'note':'Missing labels are not neutral or unhappy. Platform labels are not a customer survey or benchmark score.'}


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
    pause = directory/'evaluation.user-paused.json'
    if evaluation.get('recovered_read_only') and pause.exists():
        paused = json.loads(pause.read_text())
        if paused['simulation_id'] not in {r['simulation_id'] for r in result['simulations']}:
            result['simulations'].append({'simulation_id':paused['simulation_id'],'iteration_id':paused['iteration_id'],
                                         'status':paused['simulation_status']})
    result["recovered_read_only"] = evaluation.get("recovered_read_only", False)
    telemetry_path = directory / "evaluation.telemetry.json"
    telemetry = json.loads(telemetry_path.read_text(encoding="utf-8")) if telemetry_path.exists() else {}
    result["tool_telemetry"] = {"calls_observed": len(telemetry),
        "completions_including_workflow_end": sum(t["observed_tool_completions"] for t in telemetry.values()),
        "failed_result_events": sum(t["observed_failed_tool_results"] for t in telemetry.values())}
    infrastructure = directory / "evaluation.infrastructure.json"
    if infrastructure.exists():
        key = "previous_infrastructure" if result["recovered_read_only"] else "infrastructure"
        result[key] = json.loads(infrastructure.read_text(encoding="utf-8"))
    if evaluation["status"] != "measured":
        result["error"] = evaluation.get("error")
        return result
    report = evaluation["results"]
    validate_results(report, evaluation["case_ids"], evaluation["reps"])
    rows = [row for repeat in report["all_rows"] for row in repeat]
    result['customer_sentiment'] = sentiment_summary(directory,rows)
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
