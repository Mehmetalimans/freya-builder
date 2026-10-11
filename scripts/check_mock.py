"""Run explicit source-derived HTTP contract fixtures; never infer bank routes."""
import argparse
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from builder.case_folder import inventory, origin
from builder.core import ContractError, digest
from builder.runtime import NoRedirect, utc_now, write_json


def validate_fixture(case):
    if not isinstance(case.get('id'), str) or not case.get('source'):
        raise ContractError('Each fixture needs an ID and source reference')
    path = case.get('path', '')
    if not path.startswith('/') or path.startswith('//') or '..' in path or '#' in path:
        raise ContractError('Fixture path must stay on the mock')
    if case.get('method') not in {'GET','POST','PUT','PATCH','DELETE','HEAD'}:
        raise ContractError('Fixture needs a documented HTTP method')
    if type(case.get('status')) is not int or not 100 <= case['status'] <= 599:
        raise ContractError('Fixture needs an exact expected status')
    if ('response_json' in case) == ('response_text' in case):
        raise ContractError('Specify exactly one expected JSON or text response')


def run_checks(mock_url, cases, opener=None):
    origin(mock_url)
    if not cases: raise ContractError('No contract fixtures supplied')
    for case in cases: validate_fixture(case)
    opener = opener or urllib.request.build_opener(NoRedirect())
    rows = []
    for case in cases:
        body = json.dumps(case['request_json'], ensure_ascii=False).encode() if 'request_json' in case else None
        req = urllib.request.Request(mock_url.rstrip('/') + case['path'], data=body,
            method=case['method'], headers={'Content-Type':'application/json','User-Agent':'Freya-contract-check/1'})
        started = time.monotonic()
        try:
            try:
                with opener.open(req, timeout=30) as response: status, raw = response.status, response.read()
            except urllib.error.HTTPError as error:
                status, raw = error.code, error.read()
            text = raw.decode('utf-8')
            if 'response_json' in case:
                content_equal = json.loads(text) == case['response_json']
            else: content_equal = text == case['response_text']
            rows.append({'id':case['id'],'pass':status == case['status'] and content_equal,
                         'status':status,'expected_status':case['status'],'body_equal':content_equal,
                         'seconds':round(time.monotonic()-started,3)})
        except (OSError, ValueError) as error:
            rows.append({'id':case['id'],'pass':False,'error_type':type(error).__name__,
                         'seconds':round(time.monotonic()-started,3)})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case_folder', type=Path); parser.add_argument('mock_url')
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=ROOT/'state/mock-verification.json')
    args = parser.parse_args()
    fixture_bytes = args.fixtures.read_bytes()
    fixtures = json.loads(fixture_bytes)
    inputs = inventory(args.case_folder)
    rows = run_checks(args.mock_url, fixtures['cases'])
    failed = sum(not row['pass'] for row in rows)
    result = {'status':'failed' if failed else 'passed','mock_url':args.mock_url.rstrip('/'),
              'case_sha256':inputs['sha256'],'fixtures_sha256':digest(fixture_bytes),
              'checked_at':utc_now(),'total':len(rows),'failed':failed,'results':rows}
    write_json(args.out,result)
    print(json.dumps({'status':result['status'],'total':len(rows),'failed':failed,'report':str(args.out)}))
    return bool(failed)


if __name__ == '__main__': raise SystemExit(main())
