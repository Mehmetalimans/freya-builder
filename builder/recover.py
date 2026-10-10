"""Re-score existing completed repetitions without starting calls or bank sessions."""
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
    if (directory/'evaluation.json').exists():
        existing = json.loads((directory/'evaluation.json').read_text(encoding='utf-8'))
        if existing.get('status') == 'measured':
            raise ContractError('This run already has an official measured result; preserve it')
    if (directory / 'evaluation.user-paused.json').exists() or (directory / 'evaluation.infrastructure-paused.json').exists():
        return recover_paused(directory)
    return recover_single(directory)


def recover_single(directory):
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


def recover_paused(directory):
    """A user-paused three-repeat run can finish remotely after its worker stops."""
    saved = json.loads((directory/'result.json').read_text(encoding='utf-8'))
    pause_path = directory/'evaluation.user-paused.json'
    if not pause_path.exists(): pause_path = directory/'evaluation.infrastructure-paused.json'
    pause = json.loads(pause_path.read_text(encoding='utf-8'))
    if (directory/'evaluation.recovered.json').exists():
        raise ContractError('This run already has recovered evidence')
    history = json.loads((directory/'simulation-history.json').read_text())
    last = {'simulation_id':pause['simulation_id'], 'iteration_id':pause['iteration_id']}
    if last['simulation_id'] not in {r['simulation_id'] for r in history}:
        history.append(last)
    if len(history) != 3 or len({r['simulation_id'] for r in history}) != 3:
        raise ContractError('Paused recovery requires exactly three distinct recorded simulations')
    check_environment(require_bank=True)
    check_run_workspace(saved, os.environ['FREYA_WORKSPACE_ID'])
    runtime = directory/'evaluation-runtime'
    store = json.loads((runtime/'.personas.json').read_text())
    by_persona = {persona:key.split(':',1)[0] for key,persona in store.items()}
    # IDs are from the recorded first repetition, never from a new case selection.
    first = json.loads((directory/'repetition-01.json').read_text())['rows']
    ids = [r['id'] for r in first]
    brief, split = pause.get('brief','A'), pause.get('split','dev')
    cases = selected_cases(brief,split,','.join(ids))
    started = time.monotonic()
    client = official_client(started+300, Trace(directory/'recovery.trace.jsonl'))
    api = client.api
    def readonly(method,*args,**kwargs):
        if method != 'GET': raise ContractError('Recovery never sends Freya mutations')
        return api(method,*args,**kwargs)
    client.api = readonly
    sys.path.insert(0,str(runtime/'tools'))
    sys.modules['freya'] = client
    spec = importlib.util.spec_from_file_location('paused_recovery_runner',runtime/'tools/run_cases.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    original_http = runner.http
    repetitions, telemetry = [], {}
    for index, remote in enumerate(history):
        current = client.api('GET','/api/v2/simulations/'+remote['simulation_id'])['simulation']
        if current['status'] not in ('completed','paused'): raise ContractError('A recorded remote simulation is incomplete')
        iteration = client.get_iteration(remote['simulation_id'],remote['iteration_id'])
        if (iteration.get('runsTotal') != len(ids) or len(iteration['runs']) != len(ids)
                or any(r.get('outcome') not in ('pass','fail') or not r.get('endedAt') for r in iteration['runs'])):
            raise ContractError('Every remote call must have a terminal verdict and end timestamp')
        sessions = {}
        matched = [r for r in iteration['runs'] if by_persona.get(r['personaId']) in ids]
        if len(matched) != len(ids): raise ContractError('Recorded case count is incomplete or duplicated')
        for item in matched:
            case = by_persona[item['personaId']]
            if case in sessions: raise ContractError('Duplicate recorded persona')
            call = client.get_call(item['callId'])
            if not call.get('endedAt'): raise ContractError('Recorded call is still active')
            if call.get('assistantWorkflowId') != saved['workflow_id'] or call.get('entityVersionNumber') != saved['platform_version']:
                raise ContractError('Recorded call workflow/version differs from the tested build')
            telemetry[item['callId']] = call_telemetry(call)
            (directory/('call-'+item['callId']+'.json')).write_text(redact(json.dumps(call,ensure_ascii=False,indent=2)),encoding='utf-8')
            for message in call.get('messages',[]):
                if message.get('role') != 'system': continue
                try: event = json.loads(message['message'])
                except (ValueError,TypeError): continue
                values = event.get('variable_table',{}) if isinstance(event,dict) else {}
                if values.get('customer_id'):
                    sessions[case] = {k:values[k] for k in ('customer_id','first_name','last_name','title','now') if k in values}
                    break
        if set(sessions) != set(ids): raise ContractError('Cannot match all existing bank sessions')
        def existing_session_http(path,body=None):
            if path == '/v1/practice/sessions' and body is not None:
                return {'variables':sessions[body['case']]}
            if body is not None: raise ContractError('Recovery never sends bank mutations')
            return retry_ledger_read(original_http,path)
        runner.http = existing_session_http
        client.run_simulation = lambda *args,**kwargs:(remote['simulation_id'],remote['iteration_id'],'completed')
        personas = {case:persona for persona,case in by_persona.items() if case in sessions}
        rows,*_ = runner.run_once(saved['agent_id'],cases,personas)
        repetitions.append(rows)
        write_json(directory/f'repetition-{index+1:02d}.recovered.json',{'rows':rows,**remote,'recovered_read_only':True})
    final = [{'id':c['id'],'family':c['family'],'passes':sum(next(r for r in rep if r['id']==c['id'])['pass'] for rep in repetitions),
              'runs':3,'pass':all(next(r for r in rep if r['id']==c['id'])['pass'] for rep in repetitions)} for c in cases]
    report = {'final':final,'all_rows':repetitions,'rows':repetitions[-1],'passed':sum(r['pass'] for r in final),
              'total':len(ids),'runs':3,'seconds':None}
    validate_results(report,ids,3)
    after = credit_snapshot(client)
    summary = {'status':'measured','brief':brief,'split':split,'reps':3,'case_ids':ids,'seconds':None,
               'workspace_id':saved['workspace_id'],'results':report,'passed':report['passed'],'total':len(ids),
               'benchmark_success':report['passed']/len(ids),'actual_cost_usd':None,'credits_after':after,
               'recovered_read_only':True,'recovery_seconds':round(time.monotonic()-started,3),
               'recorded_local_wait_seconds':saved.get('seconds'),'remote_job_may_still_be_running':False,
               'cost_note':'Read-only recovery; no new simulation, no measured complete-run duration or invoice.'}
    if pause_path.name == 'evaluation.infrastructure-paused.json':
        summary['platform_state_discrepancy'] = pause['reason']
    write_json(directory/'evaluation.telemetry.json',telemetry)
    write_json(directory/'evaluation.recovered.json',summary)
    with exclusive(ROOT/'state/budget.lock'):
        ledger_path = ROOT/'state/budget-ledger.json'
        ledger = json.loads(ledger_path.read_text())
        write_json(ledger_path,settle_campaign(ledger,after,directory.name))
    print(json.dumps({'status':'measured','passed':report['passed'],'total':len(ids),'recovered_read_only':True}))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    recover(parser.parse_args().run_directory)
