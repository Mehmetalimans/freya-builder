"""Measure supplied scenario personas against one frozen deployment, one simulation."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from builder.core import ContractError,digest
from builder.runtime import Trace,official_client,exclusive,write_json,redact,check_run_workspace
from builder.evaluate import credit_snapshot,verify_platform_version_binding,terminal_results_ready,call_telemetry,bounded_simulation_body


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run',type=Path);ap.add_argument('scenarios',type=Path)
    ap.add_argument('--only',help='Comma-separated supplied IDs');ap.add_argument('--max-seconds',type=int,default=1100)
    a=ap.parse_args()
    saved=json.loads((a.run/'result.json').read_text(encoding='utf-8'))
    if saved.get('status')!='deployed_verified':raise ContractError('A verified deployment is required')
    check_run_workspace(saved,os.environ.get('FREYA_WORKSPACE_ID'))
    cases=json.loads(a.scenarios.read_text(encoding='utf-8'))
    if a.only:
        requested=set(a.only.split(','));cases=[c for c in cases if c['id'] in requested]
        if {c['id'] for c in cases}!=requested:raise ContractError('Unknown scenario')
    if not cases or len(cases)>20:raise ContractError('Supply 1..20 explicit scenarios')
    out=a.run/('evaluation-'+uuid.uuid4().hex[:8]);out.mkdir()
    trace=Trace(out/'trace.jsonl');start=time.monotonic()
    report={'status':'failed','benchmark_success':None,'workflow_id':saved['workflow_id'],
            'platform_version':saved['platform_version'],'scenarios_sha256':digest(a.scenarios.read_bytes()),
            'cases':[c['id'] for c in cases],'interpretation':'Development persona judge; not hidden final score'}
    c=None
    scope=digest(os.environ['FREYA_WORKSPACE_ID'])[:16]
    with exclusive(ROOT/'state'/f'{scope}.lock'):
      try:
        c=official_client(start+a.max_seconds,trace)
        verify_platform_version_binding(c,saved,os.environ['FREYA_WORKSPACE_ID'],a.run/'workflow.export.json')
        running=c.api('GET','/api/v2/simulations',workspaceId=os.environ['FREYA_WORKSPACE_ID'],status='running',limit=1)
        if not isinstance(running.get('simulations'),list) or running['simulations']:
            raise ContractError('Workspace already has an active simulation')
        report['credits_before']=credit_snapshot(c)
        if report['credits_before']['creditsLeft']<=0:raise ContractError('No trial credits remain')
        personas=[{'name':case['id']+' '+case['title'],'prompt':case['prompt'],
                   'successCriteria':case['successCriteria'],'tags':['hackathon','final-development']} for case in cases]
        made=c.create_personas(personas)['personas']
        if len(made)!=len(cases):raise ContractError('Persona count mismatch')
        ids={case['id']:p['id'] for case,p in zip(cases,made)}
        write_json(out/'personas.json',{'specs':personas,'ids':ids})
        variables={ids[case['id']]:case['variables'] for case in cases}
        original=c.api;owned={};last=[0];reconciled=set()
        def tracked(method,path,body=None,**params):
            if method=='POST' and path=='/api/v2/simulations':body=bounded_simulation_body(body,3)
            value=original(method,path,body,**params)
            if method=='POST' and path=='/api/v2/simulations':
                sim=value.get('simulation',value);owned[sim['id']]=set(variables)
                report['simulation_id']=sim['id'];write_json(out/'result.json',report)
                print(json.dumps({'simulation_started':sim['id'],'directory':str(out)}),flush=True)
            sid=path.removeprefix('/api/v2/simulations/')
            if method=='GET' and sid in owned and value.get('simulation',value).get('status')=='running' and time.monotonic()-last[0]>30:
                last[0]=time.monotonic()
                its=original('GET',f'/api/v2/simulations/{sid}/iterations')
                iterations=its.get('iterations') or its.get('items') or []
                if len(iterations)==1:
                    progress=c.get_iteration(sid,iterations[0]['id']);write_json(out/'progress.json',progress)
                    if terminal_results_ready(progress,owned[sid],saved):
                        calls=[c.get_call(r['callId']) for r in progress['runs']]
                        if all(call.get('endedAt') for call in calls):
                            original('PUT',f'/api/v2/simulations/{sid}',{'status':'paused'})
                            value=original('GET',f'/api/v2/simulations/{sid}');reconciled.add(sid)
            return value
        c.api=tracked
        sid,iid,status=c.run_simulation(saved['agent_id'],'Final development '+out.name,variables,max_seconds=360,concurrency=3)
        report.update(simulation_id=sid,iteration_id=iid,platform_status=status)
        if status!='completed' and not(status=='paused' and sid in reconciled):raise ContractError('Simulation incomplete')
        progress=c.get_iteration(sid,iid);write_json(out/'iteration.json',progress)
        rows=progress['runs'];by_persona={r['personaId']:r for r in rows}
        if set(by_persona)!=set(variables) or len(rows)!=len(cases):raise ContractError('Missing or duplicate result')
        measured=[]
        for case in cases:
            r=by_persona[ids[case['id']]]
            if r.get('agentWorkflowId')!=saved['workflow_id'] or r.get('agentVersionNumber')!=saved['platform_version']:
                raise ContractError('Result belongs to another workflow version')
            call=c.get_call(r['callId'])
            (out/(case['id']+'.call.json')).write_text(redact(json.dumps(call,ensure_ascii=False,indent=2)),encoding='utf-8')
            measured.append({'id':case['id'],'judge_outcome':r.get('outcome'),'reason':r.get('reason'),
                             'call_id':r['callId'],'telemetry':call_telemetry(call)})
        report.update(status='measured',rows=measured,judge_passed=sum(r['judge_outcome']=='pass' for r in measured),total=len(measured))
      except Exception as error:
        report.update(error_type=type(error).__name__)
        if isinstance(error,ContractError):report['error']=str(error)
      finally:
        if c and 'credits_before' in report:
            try:
                report['credits_after']=credit_snapshot(c)
                b,e=report['credits_before'],report['credits_after']
                report['observed_balance_delta_usd']=round((b['creditsLeft']-e['creditsLeft'])*b['creditUsdRate'],6) if b['creditUsdRate']==e['creditUsdRate'] else None
            except Exception:report['credits_after_status']='unavailable'
        report['seconds']=round(time.monotonic()-start,3);write_json(out/'result.json',report)
    print(json.dumps({'status':report['status'],'directory':str(out),'passed':report.get('judge_passed'),'total':report.get('total'),'error':report.get('error')},ensure_ascii=False),flush=True)
    return 0 if report['status']=='measured' else 1


if __name__=='__main__':raise SystemExit(main())
