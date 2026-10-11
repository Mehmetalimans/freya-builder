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
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from builder.core import ContractError, digest, canonical
from builder.campaign import check_campaign, reserve_campaign, settle_campaign
from builder.runtime import ROOT, KIT, Trace, check_environment, check_run_workspace, exclusive, official_client, redact, write_json


def selected_cases(brief, split, only=None):
    cases = json.loads((KIT / "public-test-set.json").read_text(encoding="utf-8"))
    # Frozen without reading scripts/checks: first seven A cases are development.
    dev = {c["id"] for c in [x for x in cases if x["brief"] == "A"][:7]}
    selected = [c for c in cases if c["brief"] == brief and ((c["id"] in dev) == (split == "dev"))]
    if only is not None:
        ids = only.split(",")
        if not all(ids) or len(set(ids)) != len(ids) or not set(ids) <= {c["id"] for c in selected}:
            raise ContractError("--only must contain unique case IDs from the requested brief and split")
        selected = [c for c in selected if c["id"] in ids]
    return selected


def verify_platform_version_binding(client, saved, workspace_id, export_path=None):
    """Ensure the deployed workflow version and sha256 match what is recorded in result.json before any paid simulation."""
    if not isinstance(saved, dict):
        raise ContractError("Invalid result.json metadata")
    expected_version = saved.get("platform_version")
    workflow_id = saved.get("workflow_id")
    if not workflow_id:
        raise ContractError("Result metadata missing workflow_id")
    if expected_version is None:
        raise ContractError("Result metadata missing platform_version; deploy and verify on Freya first")
    expected_sha = saved.get("workflow_sha256")
    if export_path:
        p = Path(export_path)
        local = p.with_name("workflow.local.json")
        if p.exists() and local.exists():
            compiled = json.loads(local.read_text(encoding="utf-8"))
            if expected_sha and digest(canonical(compiled)) != expected_sha:
                raise ContractError(
                    f"workflow.local.json sha256 mismatch with result.json: "
                    f"{digest(canonical(compiled))} != {expected_sha}"
                )
            export_data = json.loads(p.read_text(encoding="utf-8"))
            from builder.runtime import verify_readback
            verify_readback(compiled, export_data)
    try:
        resp = client.api("GET", f"/api/v2/versions/workflow/{workflow_id}", workspaceId=workspace_id)
        versions = resp.get("versions", [])
    except Exception as err:
        raise ContractError(f"Failed to query platform workflow versions: {err}")
    if not isinstance(versions, list) or not versions:
        raise ContractError(f"No versions found on platform for workflow {workflow_id}")
    published = [v for v in versions if v.get("isPublished")]
    active = max(published, key=lambda v: v.get("versionNumber", 0)) if published else max(versions, key=lambda v: v.get("versionNumber", 0))
    current_live_version = active.get("versionNumber")
    if current_live_version != expected_version:
        raise ContractError(
            f"Platform version mismatch: saved run recorded version {expected_version}, "
            f"but live workflow {workflow_id} has active version {current_live_version}. "
            "Refusing to evaluate stale build."
        )
    return current_live_version


def reserve_budget(policy, state, case_runs, simulations, credit_pilot=False):
    rate = policy.get("verified_max_cost_per_case_usd")
    cap = policy.get("total_authorized_usd")
    valid_number = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    if not credit_pilot and (policy.get("live_tests_enabled") is not True or not valid_number(rate) or rate < 0
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
    if credit_pilot:
        if policy.get("credit_pilot_authorized") is not True or case_runs != 1 or simulations != 1:
            raise ContractError("Credit pilot requires explicit authorization and exactly one case/repetition")
        if state.get("credit_pilot_started"):
            raise ContractError("Credit pilot already reserved; reconcile its result and billing before more tests")
        reserve = round(cap - state.get("reserved_usd", 0) - state.get("other_spend_usd", 0), 6)
        if reserve <= 0: raise ContractError("No remaining authorized credit")
    else:
        reserve = round(case_runs * rate, 6)
    if state.get("reserved_usd", 0) + state.get("other_spend_usd", 0) + reserve > cap:
        raise ContractError("Evaluation exceeds remaining authorized budget")
    return {**state, **({"credit_pilot_started": True} if credit_pilot else {}),
            "reserved_usd": round(state.get("reserved_usd", 0) + reserve, 6),
            "case_runs": state.get("case_runs", 0) + case_runs,
            "simulations": state.get("simulations", 0) + simulations}, reserve


def credit_snapshot(client):
    snapshot = client.api("GET", "/api/v2/workspaces/" + os.environ["FREYA_WORKSPACE_ID"] + "/credits")
    for key in ("creditsLeft", "creditUsdRate"):
        value = snapshot.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
            raise ContractError("Invalid workspace credit snapshot")
    return {k: snapshot[k] for k in ("creditsLeft", "creditUsdRate")}


def retry_ledger_read(http, path, body=None):
    # Session creation is a mutation and must never be retried here.
    if body is not None or not path.startswith("/v1/practice/ledger/"):
        return http(path, body)
    for attempt in range(3):
        try:
            return http(path)
        except (json.JSONDecodeError, urllib.error.URLError, TimeoutError):
            if attempt == 2: raise
            time.sleep(attempt + 1)


def call_telemetry(call):
    errors, completions = 0, 0
    for message in call.get("messages", []):
        if message.get("role") != "system": continue
        try:
            event = message.get("message")
            event = json.loads(event) if isinstance(event, str) else event
            if not isinstance(event, dict): continue
            if event.get("event") == "function_call_error":
                errors += 1
            elif event.get("event") == "function_call_complete":
                completions += 1
                result = event.get("result", {})
                if isinstance(result, dict) and (result.get("status") == "error" or
                    (isinstance(result.get("data"), dict) and result["data"].get("ok") is False)):
                    errors += 1
        except (ValueError, TypeError):
            continue
    return {"observed_tool_completions": completions, "observed_failed_tool_results": errors}


def bounded_simulation_body(body):
    if body.get("mode") != "chat" or body.get("runsPerPersona") != 1:
        raise ContractError("Only a single text repetition per simulation is allowed")
    return {**body, "maxRetries": 0, "maxConcurrentCalls": 1}


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


def worker(run_dir, runtime, brief, split, reps, style, seconds, only=None, monitored=False):
    # Run the untouched organizer runner in an isolated scratch copy, with a bounded transport.
    check_environment(require_bank=True)
    saved = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
    check_run_workspace(saved, os.environ["FREYA_WORKSPACE_ID"])
    sys.path.insert(0, str(runtime / "tools"))
    sys.path.insert(0, str(runtime))
    trace = Trace(run_dir / "evaluation.trace.jsonl")
    freya = official_client(time.monotonic() + seconds, trace)
    verify_platform_version_binding(freya, saved, os.environ["FREYA_WORKSPACE_ID"], run_dir / "workflow.export.json")
    original_api = freya.api
    policy = json.loads((ROOT / "budget.json").read_text(encoding="utf-8"))
    simulation_history = []
    def tracked_api(method, path, body=None, **params):
        if method == "POST" and path == "/api/v2/simulations":
            if monitored:
                check_campaign(policy, credit_snapshot(freya), len(body["selectedPersonaIds"]))
            body = bounded_simulation_body(body)
        result = original_api(method, path, body, **params)
        if method == "POST" and path == "/api/v2/simulations":
            sim = result.get("simulation", result)
            write_json(run_dir / "remote-simulation.json", {"simulation_id": sim["id"], "status": sim.get("status")})
            trace.emit("simulation_started", simulation_id=sim["id"], case_count=len(body["selectedPersonaIds"]), max_retries=0)
        return result
    freya.api = tracked_api
    original_run = freya.run_simulation
    def run_simulation(*args, **kwargs):
        sim_id, iteration_id, status = original_run(*args, **kwargs)
        write_json(run_dir / "remote-simulation.json", {"simulation_id": sim_id, "iteration_id": iteration_id, "status": status})
        simulation_history.append({"simulation_id": sim_id, "iteration_id": iteration_id, "status": status})
        write_json(run_dir / "simulation-history.json", simulation_history)
        if status != "completed": raise ContractError("Simulation did not complete; no benchmark score is valid")
        return sim_id, iteration_id, status
    freya.run_simulation = run_simulation
    sys.modules["freya"] = freya
    telemetry = {}
    original_get_call = freya.get_call
    def get_call(call_id):
        call = original_get_call(call_id)
        (run_dir / ("call-" + call_id + ".json")).write_text(redact(json.dumps(call, ensure_ascii=False, indent=2)), encoding="utf-8")
        telemetry[call_id] = call_telemetry(call)
        return call
    freya.get_call = get_call
    spec = importlib.util.spec_from_file_location("official_run_cases", runtime / "tools" / "run_cases.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    original_bank_http = runner.http
    runner.http = lambda path, body=None: retry_ledger_read(original_bank_http, path, body)
    original_run_once = runner.run_once
    scored_repetitions = 0
    def run_once(*args, **kwargs):
        nonlocal scored_repetitions
        result = original_run_once(*args, **kwargs)
        rows, sim_id, iteration_id, status, took, median_wait = result
        scored_repetitions += 1
        write_json(run_dir / f"repetition-{scored_repetitions:02d}.json", {
            "rows": rows, "simulation_id": sim_id, "iteration_id": iteration_id,
            "status": status, "seconds": took, "median_slowest_turn_seconds": median_wait})
        trace.emit("repetition_scored", repetition=scored_repetitions,
                   passed=sum(row["pass"] for row in rows), total=len(rows), seconds=round(took, 3))
        return result
    runner.run_once = run_once
    ids = [c["id"] for c in selected_cases(brief, split, only)]
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
    parser.add_argument("--only", help="Comma-separated case IDs within the chosen split; use one for an initial smoke test")
    parser.add_argument("--credit-pilot", action="store_true", help="Explicitly authorized single-case measurement with unknown tariff; reserves all remaining budget")
    parser.add_argument("--monitored-credit", action="store_true", help="Authorized campaign with per-simulation credit checks and a billing buffer")
    parser.add_argument("--style", choices=["pieces", "corrects", "talkative", "asks_back", "in_words"])
    parser.add_argument("--max-seconds", type=int, default=1200)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    run_dir = args.run_directory.resolve()
    if not 1 <= args.max_seconds <= 1800: parser.error("max-seconds must be 1..1800")
    if args.credit_pilot and args.monitored_credit: parser.error("Choose one credit mode")
    if args.worker:
        worker(run_dir, run_dir / "evaluation-runtime", args.brief, args.split, args.reps, args.style, args.max_seconds, args.only, args.monitored_credit)
        return 0
    summary = {"status": "blocked", "benchmark_success": None, "actual_cost_usd": None,
               "evaluator_sha256": digest(Path(__file__).read_bytes()),
               "brief": args.brief, "split": args.split, "reps": args.reps, "style": args.style,
               "remote_job_may_still_be_running": False}
    start = time.monotonic()
    billing_client = None
    try:
        saved = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        if saved["status"] != "deployed_verified": raise ContractError("First deploy and verify this build on Freya")
        if (run_dir / "evaluation.json").exists(): raise ContractError("This build already has an evaluation record; preserve it and create a new build run")
        check_environment(require_bank=True)
        check_run_workspace(saved, os.environ["FREYA_WORKSPACE_ID"])
        summary["workspace_id"] = saved["workspace_id"]
        ids = [c["id"] for c in selected_cases(args.brief, args.split, args.only)]
        if args.credit_pilot and (args.split != "dev" or len(ids) != 1 or args.reps != 1):
            raise ContractError("Credit pilot is limited to one development case and one repetition")
        scope = digest(os.environ["FREYA_WORKSPACE_ID"])[:16]
        with exclusive(ROOT / "state" / "budget.lock"), exclusive(ROOT / "state" / f"{scope}.lock"):
            billing_client = official_client(start + args.max_seconds, Trace(run_dir / "billing.trace.jsonl"))
            live_version = verify_platform_version_binding(billing_client, saved, os.environ["FREYA_WORKSPACE_ID"], run_dir / "workflow.export.json")
            summary["platform_version"] = live_version
            summary["workflow_sha256"] = saved.get("workflow_sha256")
            running = billing_client.api("GET", "/api/v2/simulations", workspaceId=os.environ["FREYA_WORKSPACE_ID"], status="running", limit=1)
            if not isinstance(running.get("simulations"), list) or running["simulations"]:
                raise ContractError("Workspace already has a running simulation, or its status is ambiguous")
            policy = json.loads((ROOT / "budget.json").read_text(encoding="utf-8"))
            ledger_path = ROOT / "state" / "budget-ledger.json"
            ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists() else {}
            updated, reserve = (None, None) if args.monitored_credit else reserve_budget(policy, ledger, len(ids) * args.reps, args.reps, args.credit_pilot)
            summary["credits_before"] = credit_snapshot(billing_client)
            if summary["credits_before"]["creditsLeft"] <= 0:
                raise ContractError("No available workspace credit")
            if args.monitored_credit:
                updated = reserve_campaign(policy, ledger, summary["credits_before"], len(ids), args.reps, run_dir.name)
            # Reservation persists on crash/timeout; never silently refund an uncertain remote run.
            write_json(ledger_path, updated)
            summary.update(reserved_upper_bound_usd=None if (args.credit_pilot or args.monitored_credit) else reserve,
                           authorization_reserved_usd=reserve, cost_mode="monitored_credit" if args.monitored_credit else ("authorized_credit_pilot" if args.credit_pilot else "verified_rate"), case_ids=ids)
            runtime = run_dir / "evaluation-runtime"
            shutil.copytree(KIT, runtime, ignore=shutil.ignore_patterns("__pycache__", "results", "traces", ".personas.json", ".freya-agents.json"))
            remaining = int(args.max_seconds - (time.monotonic() - start))
            if remaining <= 0: raise TimeoutError("Evaluation time limit reached before starting the worker")
            command = [sys.executable, "-I", str(Path(__file__).resolve()), str(run_dir), "--brief", args.brief,
                       "--split", args.split, "--reps", str(args.reps), "--max-seconds", str(remaining), "--worker"]
            if args.style: command += ["--style", args.style]
            if args.only: command += ["--only", args.only]
            if args.monitored_credit: command += ["--monitored-credit"]
            summary["remote_job_may_still_be_running"] = True
            child = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   timeout=remaining, env={**os.environ, "PYTHONUTF8": "1"})
            (run_dir / "evaluation.log").write_text(redact(child.stdout + child.stderr), encoding="utf-8")
            remote_file = run_dir / "remote-simulation.json"
            if remote_file.exists():
                remote = json.loads(remote_file.read_text(encoding="utf-8"))
                summary["remote_simulation"] = remote
                summary["remote_job_may_still_be_running"] = remote.get("status") not in ("completed", "failed", "paused")
            if child.returncode: raise ContractError("Official runner failed; see the redacted evaluation log")
            report = json.loads((run_dir / "evaluation.raw.json").read_text(encoding="utf-8"))
            validate_results(report, ids, args.reps)
            summary.update(status="measured", passed=report["passed"], total=report["total"],
                           benchmark_success=report["passed"] / len(ids), results=report)
            if args.monitored_credit:
                after = credit_snapshot(billing_client)
                write_json(ledger_path, settle_campaign(updated, after, run_dir.name))
    except subprocess.TimeoutExpired:
        summary.update(status="timeout", remote_job_may_still_be_running=True,
                       error="Local wait stopped. No documented remote cancellation is assumed. Inspect Freya before another test.")
    except Exception as error:
        summary.update(error_type=type(error).__name__)
        if isinstance(error, ContractError): summary["error"] = str(error)
    if billing_client is not None and "credits_before" in summary:
        try:
            summary["credits_after"] = credit_snapshot(billing_client)
            before, after = summary["credits_before"], summary["credits_after"]
            summary["observed_balance_delta_usd"] = round((before["creditsLeft"] - after["creditsLeft"]) * before["creditUsdRate"], 6) if before["creditUsdRate"] == after["creditUsdRate"] else None
            summary["cost_note"] = "Balance delta is a snapshot, not a settled per-call invoice; incomplete reservations remain held"
        except Exception:
            summary["billing_after_status"] = "unavailable_reservation_retained"
    summary["seconds"] = round(time.monotonic() - start, 3)
    # A rejected second attempt must not overwrite previous evidence.
    target = run_dir / ("evaluation.blocked.json" if (run_dir / "evaluation.json").exists() else "evaluation.json")
    write_json(target, summary)
    print(json.dumps({"status": summary["status"], "report": str(target), "error": summary.get("error")}, ensure_ascii=False))
    return 0 if summary["status"] == "measured" else 1


if __name__ == "__main__":
    raise SystemExit(main())
