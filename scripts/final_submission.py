"""Package one verified final generation; never send the submission email."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from builder.core import ContractError, digest
from builder.runtime import redact, verify_readback, write_json


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def prepare(run, destination):
    result = json.loads((run/'result.json').read_text(encoding='utf-8'))
    if result.get('status') != 'deployed_verified' or result.get('mode') != 'folder-live':
        raise ContractError('Only a verified folder-mode deployment can be submitted')
    workflow = json.loads((run/'workflow.local.json').read_text(encoding='utf-8'))
    exported = json.loads((run/'workflow.export.json').read_text(encoding='utf-8'))
    verify_readback(workflow, exported)
    session = (run/'codex.session.jsonl').read_text(encoding='utf-8')
    events = [json.loads(line) for line in session.splitlines() if line.strip()]
    if not any(e.get('type') == 'session_meta' for e in events) or len(events) < 3:
        raise ContractError('Full Codex session log is required, not a short summary')
    if redact(session) != session:
        raise ContractError('Session still contains a credential; sanitize it before packaging')
    destination.mkdir(parents=True, exist_ok=False)
    for source, name in [('workflow.export.json','workflow.json'), ('codex.session.jsonl','builder.trace.jsonl'),
                         ('result.json','generation-result.json'), ('input-manifest.json','input-manifest.json'),
                         ('builder-source-hashes.json','builder-source-hashes.json'), ('analysis.json','requirements.json'),
                         ('trace.jsonl','pipeline.trace.jsonl'), ('generation-prompt.txt','generation-prompt.txt')]:
        raw = (run/source).read_text(encoding='utf-8')
        (destination/name).write_text(redact(raw),encoding='utf-8',newline='\n')
    print(json.dumps({'status':'prepared_not_submitted','directory':str(destination),
                      'next':'Commit these artifacts, then create manifest using that commit.'}))


def manifest(destination, team, members, repo, commit):
    if not team.strip() or not members or any(set(m) != {'name','email'} or '@' not in m['email'] for m in members):
        raise ContractError('Confirmed team and member names/emails are required')
    if len(members) > 2: raise ContractError('At most two team members')
    result = json.loads((destination/'generation-result.json').read_text(encoding='utf-8'))
    for name in ['workflow.json','builder.trace.jsonl','generation-result.json','input-manifest.json','builder-source-hashes.json']:
        relative = (destination/name).relative_to(ROOT).as_posix()
        if git('show',f'{commit}:{relative}') != (destination/name).read_bytes():
            raise ContractError(f'{name} is not identical to the named commit')
    data = {'team':team,'members':members,'repo':repo,'commit':commit,
            'run_command':'python builder/build.py {case_folder} {mock_url}',
            'workflow':(destination/'workflow.json').relative_to(ROOT).as_posix(),
            'trace':(destination/'builder.trace.jsonl').relative_to(ROOT).as_posix(),
            'mock_url':result['mock_url']}
    write_json(destination/'submission.json',data)
    print(json.dumps({'status':'manifest_ready_not_submitted','commit':commit,'file':str(destination/'submission.json')}))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare');p.add_argument('run',type=Path);p.add_argument('destination',type=Path)
    p=sub.add_parser('manifest');p.add_argument('destination',type=Path);p.add_argument('--team',required=True)
    p.add_argument('--members',type=Path,required=True);p.add_argument('--repo',required=True);p.add_argument('--commit',required=True)
    a=ap.parse_args()
    if a.action=='prepare':prepare(a.run.resolve(),a.destination.resolve())
    else:manifest(a.destination.resolve(),a.team,json.loads(a.members.read_text(encoding='utf-8')),a.repo,a.commit)


if __name__=='__main__':main()
