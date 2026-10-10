"""Regressions found in integration/v3-final; synthetic inputs, no live calls."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from builder.core import ContractError, TOOLS, compile_workflow, make_post_process_code, read_contract

KIT = Path(__file__).resolve().parent.parent / 'starter-v3/build-the-builder'
API = json.loads((KIT / 'tools/openapi.json').read_text(encoding='utf-8'))


def hook(name, value):
    scope = {'result': deepcopy(value)}
    exec(make_post_process_code(name), scope)
    return scope['result']


class IntegrationRegressions(unittest.TestCase):
    def test_unseen_policy_has_no_stale_bank_dates_or_numeric_rules(self):
        policy = ('You represent Example Cooperative. Verify postal code first. '
                  'Allow four wrong answers. Callback hours are 08:00-09:00.\n'
                  'Business days are Monday through Friday, except bank holidays: 2031-05-01.\n'
                  '| 1 - 20 | early | the 4th business day after today |\n')
        wf, _ = compile_workflow([('synthetic', policy)], API)
        text = json.dumps(wf)
        for forbidden in ('2026-10-14', '2026-10-26', 'Freya Bank', '10:00-19:00',
                          '3 wrong answers', 'Date of birth verified', 'days_late: 8 to 45'):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_unrecognized_calendar_does_not_invent_weekdays_or_holidays(self):
        wf, analysis = compile_workflow([('policy', 'Business days depend on the country; consult the supplied account calendar.')], API)
        self.assertEqual(analysis['calendar']['status'], 'unsupported_definition_policy_only')
        self.assertNotIn('Monday through Friday', wf['system_prompt'])
        self.assertNotIn('2026-10-26', wf['system_prompt'])

    def test_identity_transport_failure_is_not_customer_rejection(self):
        wf, _ = compile_workflow([('policy', 'Use the supplied verification policy.')], API)
        text = json.dumps(wf)
        self.assertNotIn('false or an error: that is a wrong answer', text)
        self.assertNotIn('Never close as service_error during identity verification', text)
        data = hook('verify_identity', {'status': 'error', 'data': {'ok': False, 'verified': False, 'wrong_answers_left': 0}})['data']
        self.assertNotIn('wrong answers', data.get('what_to_do_next', '').lower())

    def test_failed_account_lookup_does_not_announce_loaded_account(self):
        data = hook('get_account', {'data': {'ok': False, 'error': 'unavailable'}})['data']
        self.assertNotIn('Account loaded', data.get('what_to_do_next', ''))

    def test_string_false_is_not_success(self):
        for name in TOOLS:
            with self.subTest(tool=name):
                data = hook(name, {'data': {'ok': 'false', 'verified': 'false', 'all_verified': 'false'}})['data']
                self.assertNotIn('what_to_do_next', data)

    def test_hook_cannot_invent_next_identity_question_or_attempt_limit(self):
        for data in ({'verified': True}, {'verified': False}, {'verified': False, 'wrong_answers_left': 0}):
            output = hook('verify_identity', {'data': data})['data'].get('what_to_do_next', '')
            self.assertNotIn('phone', output)
            self.assertNotIn('Three', output)
            self.assertNotIn('3 wrong', output)

    def test_hooks_do_not_override_close_enum_or_retry_policy(self):
        for name in TOOLS:
            for ok in (True, False):
                output = hook(name, {'data': {'ok': ok}})['data'].get('what_to_do_next', '')
                with self.subTest(tool=name, ok=ok):
                    self.assertNotIn('close_call(outcome=', output)
                    self.assertNotIn('Immediately retry', output)
                    self.assertNotIn('restructuring, human, or support', output)

    def test_bank_write_retries_remain_disabled_and_connect_retries_are_bounded(self):
        wf, _ = compile_workflow([('policy', 'Use supplied policy.')], API)
        for node in wf['nodes'].values():
            for tool in node.get('tools', []):
                self.assertEqual(tool['config']['maxRetries'], 0)
                self.assertEqual(tool['function']['parameters']['properties']['connect_retries']['default'], 2)

    def test_null_constraint_is_rejected_instead_of_silently_removed(self):
        document = deepcopy(API)
        props = document['paths']['/add_note']['post']['requestBody']['content']['application/json']['schema']['properties']
        props['reason']['enum'] = None
        with self.assertRaises(ContractError):
            compile_workflow([('policy', 'Use supplied policy.')], document)

    def test_malformed_response_metadata_does_not_crash_identity_detection(self):
        for response in ({'content': {'application/json': None}},
                         {'content': {'application/json': {'schema': {'properties': {'all_verified': None}}}}}):
            document = deepcopy(API)
            document['paths']['/verify_identity']['post']['responses']['200'] = response
            wf, analysis = compile_workflow([('policy', 'Use supplied policy.')], document)
            self.assertEqual(analysis['identity_gate'], 'dialogue_only')

    def test_null_required_is_rejected_with_contract_error(self):
        document = deepcopy(API)
        document['paths']['/add_note']['post']['requestBody']['content']['application/json']['schema']['required'] = None
        with self.assertRaises(ContractError):
            read_contract(document)

    def test_hooks_preserve_actual_bank_fields(self):
        data = {'ok': True, 'verified': False, 'all_verified': False,
                'wrong_answers_left': 4, 'products': [{'product_id': 'synthetic'}]}
        for name in TOOLS:
            with self.subTest(tool=name):
                output = hook(name, {'header': {'test': 'header'}, 'data': data})
                self.assertNotIn('header', output)
                self.assertEqual({k: output['data'][k] for k in data}, data)

    def test_changed_close_and_transfer_enums_have_no_stale_hook_instructions(self):
        document = deepcopy(API)
        for path, field, values in (('/transfer_to_agent', 'queue', ['helpdesk']),
                                    ('/close_call', 'outcome', ['done']),
                                    ('/close_call', 'reason', ['assisted'])):
            props = document['paths'][path]['post']['requestBody']['content']['application/json']['schema']['properties']
            props[field]['enum'] = values
        wf, _ = compile_workflow([('policy', 'Use helpdesk and close as done / assisted.')], document)
        for node in wf['nodes'].values():
            for tool in node.get('tools', []):
                hook_text = tool['post_process_code']
                self.assertNotIn('outcome="promise"', hook_text)
                self.assertNotIn('outcome="not_reached"', hook_text)
                self.assertNotIn('restructuring, human, or support', hook_text)
