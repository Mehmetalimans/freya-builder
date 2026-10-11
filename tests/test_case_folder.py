import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from builder.case_folder import check_mock_proof, inspect_workflow, inventory, origin, inspect_code
from builder.core import ContractError
from builder.runtime import ROOT


def example_workflow():
    return {'initial_node': 'help', 'system_prompt': 'Resolve the library request from returned records.', 'global_nodes': {},
            'nodes': {'help': {'name': 'help', 'node_type': 'conversation',
                'tools': [{'type': 'function', 'function': {'name': 'find_book', 'handler': '__function__:api_call',
                    'parameters': {'type': 'object', 'properties': {'url': {'default': 'https://library.example/items'},
                                                                 'method': {'default': 'GET'}}}}}],
                'transitions': [{'target_node': 'done'}]},
                'done': {'name': 'done', 'node_type': 'end_call', 'transitions': []}}}


class FolderContractTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = ROOT / 'runs' / 'test-temp'
        self.temp_root.mkdir(parents=True, exist_ok=True)
    def test_unrelated_domain_and_operation_are_accepted(self):
        self.assertEqual(inspect_workflow(example_workflow(), 'https://library.example')['tool_names'], ['find_book'])

    def test_external_phone_tool_is_rejected(self):
        workflow = example_workflow()
        workflow['nodes']['help']['tools'][0]['function']['parameters']['properties']['url']['default'] = 'https://other.example/items'
        with self.assertRaises(ContractError): inspect_workflow(workflow, 'https://library.example')

    def test_hostname_prefix_attack_is_rejected(self):
        workflow = example_workflow()
        workflow['nodes']['help']['tools'][0]['function']['parameters']['properties']['url']['default'] = 'https://library.example.other/items'
        with self.assertRaises(ContractError): inspect_workflow(workflow, 'https://library.example')

    def test_customer_fixtures_cannot_be_embedded(self):
        workflow = example_workflow(); workflow['test_variables'] = {'patron_id': 'fixture-only'}
        with self.assertRaises(ContractError): inspect_workflow(workflow, 'https://library.example')

    def test_platform_stripped_tool_placement_is_rejected(self):
        workflow = example_workflow(); workflow['nodes']['help']['node_type'] = 'code'
        with self.assertRaises(ContractError): inspect_workflow(workflow, 'https://library.example')

    def test_missing_transition_target_is_rejected(self):
        workflow = example_workflow(); workflow['nodes']['help']['transitions'][0]['target_node'] = 'missing'
        with self.assertRaises(ContractError): inspect_workflow(workflow, 'https://library.example')

    def test_mock_credentials_are_not_allowed_in_url(self):
        with self.assertRaises(ContractError): origin('https://name:password@library.example')

    def test_code_cannot_create_network_or_dynamic_execution(self):
        for code in ['import urllib.request', 'import requests', 'exec(vars.get("payload"))',
                     'open("private")', 'x.__class__.__bases__']:
            with self.subTest(code=code), self.assertRaises(ContractError): inspect_code(code)
        inspect_code('from decimal import Decimal\nx = Decimal(str(vars.get("value", 0)))')

    def test_input_changes_invalidate_manifest(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            path = Path(tmp) / 'brief.md'; path.write_text('Library rules', encoding='utf-8')
            first = inventory(tmp); path.write_text('Amended library rules', encoding='utf-8')
            self.assertNotEqual(first['sha256'], inventory(tmp)['sha256'])

    def test_mock_proof_must_match_inputs_and_be_fresh(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            path = Path(tmp) / 'proof.json'
            proof = {'status': 'passed', 'total': 2, 'failed': 0, 'mock_url': 'https://library.example',
                     'case_sha256': 'input-hash', 'checked_at': datetime.fromtimestamp(10000, timezone.utc).isoformat()}
            path.write_text(json.dumps(proof), encoding='utf-8')
            self.assertEqual(check_mock_proof(path, proof['mock_url'], {'sha256':'input-hash'}, now=10100)['total'], 2)
            for url, sha, now in [('https://other.example','input-hash',10100),
                                  (proof['mock_url'],'changed',10100),(proof['mock_url'],'input-hash',20000)]:
                with self.subTest(url=url, sha=sha, now=now), self.assertRaises(ContractError):
                    check_mock_proof(path,url,{'sha256':sha},now=now)


if __name__ == '__main__': unittest.main()
