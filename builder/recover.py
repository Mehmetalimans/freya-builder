"""Re-score a completed single repetition using only existing calls and read-only APIs."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from builder.core import ContractError
from builder.evaluate import credit_snapshot, retry_ledger_read, selected_cases, validate_results, call_telemetry
from builder.campaign import settle_campaign
from builder.runtime import ROOT, Trace, check_environment, check_run_workspace, exclusive, official_client, redact, write_json


def recover(directory):
    directory = Path(directory).resolve()
    old = json.loads((directory / "evaluation.json").read_text(encoding="utf-8"))
    saved = json.loads((directory / "result.json").read_text(encoding="utf-8"))
    if old["status"] == "measured" or old["reps"] != 1 or (directory / "evaluation.recovered.json").exists():
        raise ContractError("Recovery requires one unscored repetition and no existing recovery")
    check_environment(require_bank=True)
    check_run_workspace(saved, os.environ["FREYA_WORKSPACE_ID"])
    remote = json.loads((directory / "remote-simulation.json").read_text(encoding="utf-8"))
    started = time.monotonic()
    client = official_client(started + 300, Trace(directory / "recovery.trace.jsonl"))
    api = client.api
    def readonly(method, *args, **kwargs):
        if method != "GET": raise ContractError("Recovery never sends Freya mutations")
        return api(method, *args, **kwargs)
    client.api = readonly
    current = client.api("GET", "/api/v2/simulations/" + remote["simulation_id"])["simulation"]
    if current["status"] != "completed": raise ContractError("Remote simulation is not completed")
    iteration = client.get_iteration(remote["simulation_id"], remote["iteration_id"])
    runtime = directory / "evaluation-runtime"
    store = json.loads((runtime / ".personas.json").read_text(encoding="utf-8"))
    by_persona = {persona: key.split(":", 1)[0] for key, persona in store.items()}
    sessions = {}
    telemetry = {}
    for item in iteration["runs"]:
        case = by_persona.get(item["personaId"])
        if case not in old["case_ids"]: continue
        call = client.get_call(item["callId"])
        telemetry[item["callId"]] = call_telemetry(call)
        (directory / ("call-" + item["callId"] + ".json")).write_text(redact(json.dumps(call, ensure_ascii=False, indent=2)), encoding="utf-8")
        for message in call["messages"]:
            if message["role"] != "system": continue
            try: event = json.loads(message["message"])
            except (ValueError, TypeError): continue
            values = event.get("variable_table", {})
            if values.get("customer_id"):
                sessions[case] = {k: values[k] for k in ("customer_id", "first_name", "last_name", "title", "now") if k in values}
                break
    write_json(directory / "evaluation.telemetry.json", telemetry)
    if set(sessions) != set(old["case_ids"]): raise ContractError("Cannot match every recorded call to its bank session")
    sys.path.insert(0, str(runtime / "tools"))
    sys.modules["freya"] = client
    spec = importlib.util.spec_from_file_location("official_recovery_runner", runtime / "tools/run_cases.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    original_http = runner.http
    def existing_session_http(path, body=None):
        if path == "/v1/practice/sessions" and body is not None:
            return {"variables": sessions[body["case"]]}
        if body is not None: raise ContractError("Recovery never sends bank mutations")
        return retry_ledger_read(original_http, path)
    runner.http = existing_session_http
    client.run_simulation = lambda *args, **kwargs: (remote["simulation_id"], remote["iteration_id"], "completed")
    cases = selected_cases(old["brief"], old["split"], ",".join(old["case_ids"]))
    personas = {case: persona for persona, case in by_persona.items() if case in sessions}
    rows, _, _, _, _, _ = runner.run_once(saved["agent_id"], cases, personas)
    final = [{"id": row["id"], "family": row["family"], "passes": int(row["pass"]), "runs": 1, "pass": row["pass"]} for row in rows]
    report = {"final": final, "all_rows": [rows], "rows": rows, "passed": sum(row["pass"] for row in rows),
              "total": len(rows), "runs": 1, "simulation_id": remote["simulation_id"], "iteration_id": remote["iteration_id"],
              "seconds": None, "timing_note": "Read-only recovery; no new simulation timing was measured"}
    validate_results(report, old["case_ids"], 1)
    summary = {k: v for k, v in old.items() if k not in ("error", "error_type")}
    summary.update(status="measured", recovered_read_only=True, recovery_seconds=round(time.monotonic()-started, 3),
                   passed=report["passed"], total=report["total"], results=report,
                   benchmark_success=report["passed"]/len(rows), remote_job_may_still_be_running=False)
    if old.get("cost_mode") == "monitored_credit":
        with exclusive(ROOT / "state/budget.lock"):
            ledger_path = ROOT / "state/budget-ledger.json"
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            write_json(ledger_path, settle_campaign(ledger, credit_snapshot(client), directory.name))
    write_json(directory / "evaluation.recovered.json", summary)
    print(json.dumps({"status": "measured", "passed": report["passed"], "total": len(rows), "recovered_read_only": True}))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    recover(parser.parse_args().run_directory)
