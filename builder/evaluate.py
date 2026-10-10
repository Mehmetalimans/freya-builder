"""Bounded wrapper around the official scorer; never treats local tests as scores."""
import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from builder.core import ContractError, digest
from builder.runtime import ROOT, KIT, Trace, check_environment, exclusive, official_client, redact, write_json


def selected_cases(brief, split):
    cases = json.loads((KIT / "public-test-set.json").read_text(encoding="utf-8"))
    # Frozen without reading scripts/checks: first seven A cases are development.
    dev = {c["id"] for c in [x for x in cases if x["brief"] == "A"][:7]}
    return [c for c in cases if c["brief"] == brief and ((c["id"] in dev) == (split == "dev"))]


def reserve_budget(policy, state, case_runs, simulations):
    rate = policy.get("verified_max_cost_per_case_usd")
    cap = policy.get("total_authorized_usd")
    valid_number = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    if (policy.get("live_tests_enabled") is not True or not valid_number(rate) or rate < 0
            or not policy.get("cost_bound_evidence")):
        raise ContractError("Live tests disabled: verify a maximum per-case cost (or confirmed free credits) first")
    if not valid_number(cap) or not 0 <= cap <= 100:
        raise ContractError("Configured cap exceeds the user's 100 USD authorization or is invalid")
    if case_runs <= 0 or simulations <= 0:
        raise ContractError("Empty evaluation")
    for key, amount in (("case_runs", case_runs), ("simulations", simulations)):
        limit = policy.get("max_" + key)
        if not isinstance(limit, int) or limit < 0 or state.get(key, 0) + amount > limit:
            raise ContractError("Evaluation exceeds the configured test quota")
    reserve = round(case_runs * rate, 6)
    if state.get("reserved_usd", 0) + state.get("other_spend_usd", 0) + reserve > cap:
        raise ContractError("Evaluation exceeds remaining authorized budget")
    return {**state, "reserved_usd": round(state.get("reserved_usd", 0) + reserve, 6),
            "case_runs": state.get("case_runs", 0) + case_runs,
            "simulations": state.get("simulations", 0) + simulations}, reserve


def validate_results(report, ids, reps):
    final = report.get("final", [])
    rows = report.get("all_rows", [])
    if len(rows) != reps or len(final) != len(ids) or {r["id"] for r in final} != set(ids):
        raise ContractError("Incomplete official scorer result; do not publish a pass rate")
    for repetition in rows:
        if len(repetition) != len(ids) or {r["id"] for r in repetition} != set(ids):
            raise ContractError("Missing or duplicate case in scorer result")
        if any(not isinstance(r.get("pass"), bool) for r in repetition):
            raise ContractError("Missing case verdict")
    recomputed = {case: all(next(r for r in rep if r["id"] == case)["pass"] for rep in rows) for case in ids}
    if any(r.get("pass") != recomputed[r["id"]] for r in final) or report.get("passed") != sum(recomputed.values()):
        raise ContractError("Scorer summary does not match all-repetitions-must-pass results")


def worker(run_dir, runtime, brief, split, reps, style, seconds):
    # Run the untouched organizer runner in an isolated scratch copy, with a bounded transport.
    sys.path.insert(0, str(runtime / "tools"))
    sys.path.insert(0, str(runtime))
    trace = Trace(run_dir / "evaluation.trace.jsonl")
    freya = official_client(time.monotonic() + seconds, trace)
    sys.modules["freya"] = freya
    telemetry = {}
    original_get_call = freya.get_call
    def get_call(call_id):
        call = original_get_call(call_id)
        errors, completions = 0, 0
        for message in call.get("messages", []):
            if message.get("role") != "system": continue
            try:
                event = message.get("message")
                event = json.loads(event) if isinstance(event, str) else event
                if not isinstance(event, dict): continue
                if event.get("event") == "function_call_complete":
                    completions += 1
                    result = event.get("result", {})
                    if isinstance(result, dict) and (result.get("status") == "error" or
                        (isinstance(result.get("data"), dict) and result["data"].get("ok") is False)):
                        errors += 1
            except (ValueError, TypeError):
                continue
        telemetry[call_id] = {"observed_tool_completions": completions, "observed_failed_tool_results": errors}
        return call
    freya.get_call = get_call
    spec = importlib.util.spec_from_file_location("official_run_cases", runtime / "tools" / "run_cases.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    ids = [c["id"] for c in selected_cases(brief, split)]
    saved = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    sys.argv = ["run_cases.py", saved["agent_id"], "--brief", brief, "--only", ",".join(ids),
                "--reps", str(reps), "--out", str(run_dir / "evaluation.raw.json")]
    if style: sys.argv.extend(["--style", style])
    runner.main()
    write_json(run_dir / "evaluation.telemetry.json", telemetry)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("--brief", required=True, choices=["A", "B"])
    parser.add_argument("--split", default="dev", choices=["dev", "holdout"])
    parser.add_argument("--reps", type=int, default=1, choices=[1, 3])
    parser.add_argument("--style", choices=["pieces", "corrects", "talkative", "asks_back", "in_words"])
    parser.add_argument("--max-seconds", type=int, default=1200)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    run_dir = args.run_directory.resolve()
    if not 1 <= args.max_seconds <= 1800: parser.error("max-seconds must be 1..1800")
    if args.worker:
        worker(run_dir, run_dir / "evaluation-runtime", args.brief, args.split, args.reps, args.style, args.max_seconds)
        return 0
    summary = {"status": "blocked", "benchmark_success": None, "actual_cost_usd": None,
               "brief": args.brief, "split": args.split, "reps": args.reps, "style": args.style,
               "remote_job_may_still_be_running": False}
    start = time.monotonic()
    try:
        saved = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        if saved["status"] != "deployed_verified": raise ContractError("First deploy and verify this build on Freya")
        if (run_dir / "evaluation.json").exists(): raise ContractError("This build already has an evaluation record; preserve it and create a new build run")
        check_environment(require_bank=True)
        ids = [c["id"] for c in selected_cases(args.brief, args.split)]
        scope = digest(os.environ["FREYA_WORKSPACE_ID"])[:16]
        with exclusive(ROOT / "state" / "budget.lock"), exclusive(ROOT / "state" / f"{scope}.lock"):
            policy = json.loads((ROOT / "budget.json").read_text(encoding="utf-8"))
            ledger_path = ROOT / "state" / "budget-ledger.json"
            ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists() else {}
            updated, reserve = reserve_budget(policy, ledger, len(ids) * args.reps, args.reps)
            # Reservation persists on crash/timeout; never silently refund an uncertain remote run.
            write_json(ledger_path, updated)
            summary.update(reserved_upper_bound_usd=reserve, case_ids=ids)
            runtime = run_dir / "evaluation-runtime"
            shutil.copytree(KIT, runtime, ignore=shutil.ignore_patterns("__pycache__", "results", "traces", ".personas.json", ".freya-agents.json"))
            command = [sys.executable, "-I", str(Path(__file__).resolve()), str(run_dir), "--brief", args.brief,
                       "--split", args.split, "--reps", str(args.reps), "--max-seconds", str(args.max_seconds), "--worker"]
            if args.style: command += ["--style", args.style]
            child = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   timeout=args.max_seconds, env={**os.environ, "PYTHONUTF8": "1"})
            (run_dir / "evaluation.log").write_text(redact(child.stdout + child.stderr), encoding="utf-8")
            if child.returncode: raise ContractError("Official runner failed; see the redacted evaluation log")
            report = json.loads((run_dir / "evaluation.raw.json").read_text(encoding="utf-8"))
            validate_results(report, ids, args.reps)
            summary.update(status="measured", passed=report["passed"], total=report["total"],
                           benchmark_success=report["passed"] / len(ids), results=report)
    except subprocess.TimeoutExpired:
        summary.update(status="timeout", remote_job_may_still_be_running=True,
                       error="Local wait stopped. No documented remote cancellation is assumed. Inspect Freya before another test.")
    except Exception as error:
        summary.update(error_type=type(error).__name__)
        if isinstance(error, ContractError): summary["error"] = str(error)
    summary["seconds"] = round(time.monotonic() - start, 3)
    # A rejected second attempt must not overwrite previous evidence.
    target = run_dir / ("evaluation.blocked.json" if (run_dir / "evaluation.json").exists() else "evaluation.json")
    write_json(target, summary)
    print(json.dumps({"status": summary["status"], "report": str(target), "error": summary.get("error")}, ensure_ascii=False))
    return 0 if summary["status"] == "measured" else 1


if __name__ == "__main__":
    raise SystemExit(main())
