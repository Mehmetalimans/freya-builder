"""Integration boundaries retained from the teammate audit; no live calls."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

from builder.calendar import calendar_spec, calendar_code, offer_code
from builder.core import ContractError, canonical, compile_workflow, digest
from builder.evaluate import verify_platform_version_binding
from builder.runtime import KIT, verify_readback
from test_builder import temporary_directory


class AuditBoundaries(unittest.TestCase):
    def setUp(self):
        self.api = json.loads((KIT/'tools/openapi.json').read_text())
        self.wf, _ = compile_workflow([('policy', (KIT/'briefs/brief-a.md').read_text())], self.api)
        self.export = {'workflow': {**deepcopy(self.wf), 'agent_config': {'llmConfig': {'provider':'experimental-5','model':'experimental-5'}}}}

    def test_readback_checks_behavior_not_only_prompt(self):
        for change in ('on_enter', 'globals', 'extra_node'):
            export = deepcopy(self.export)
            if change == 'on_enter': export['workflow']['nodes']['identity']['on_enter'] = {'type':'silent'}
            if change == 'globals': export['workflow']['global_nodes'] = {'injected': {'name':'injected'}}
            if change == 'extra_node': export['workflow']['nodes']['injected'] = {'name':'injected'}
            with self.subTest(change=change), self.assertRaises(ContractError):
                verify_readback(self.wf, export)

    def test_version_binding_accepts_normalized_export_but_rejects_stale_or_unpublished(self):
        with temporary_directory() as td:
            path = Path(td)/'workflow.export.json'
            path.write_text(json.dumps(self.export))
            (path.parent/'workflow.local.json').write_text(json.dumps(self.wf))
            saved={'workflow_id':'wf','agent_id':'agent','platform_version':5,'workflow_sha256':digest(canonical(self.wf))}
            client=Mock()
            client.api.side_effect=[{'versions':[{'versionNumber':5,'isPublished':True}]}, {'workflow':{'agentId':'agent','workflow':self.export['workflow']}}]
            self.assertEqual(verify_platform_version_binding(client,saved,'ws',path),5)
            for versions in ([{'versionNumber':6,'isPublished':True}], [{'versionNumber':5,'isPublished':False}]):
                client.api.side_effect=[{'versions':versions}]
                with self.subTest(versions=versions), self.assertRaises(ContractError):
                    verify_platform_version_binding(client,saved,'ws',path)

    def test_calendar_requires_explicit_workdays(self):
        self.assertIsNone(calendar_spec([('policy','Bank holidays: 2031-04-04.')]))
        self.assertIsNone(calendar_spec([('policy','Business days are Something through Else, except bank holidays: 2031-04-04.')]))
        spec=calendar_spec([('policy','Business days are Tuesday through Saturday, except bank holidays: 2031-04-04.')])
        self.assertEqual(spec['workdays'],[1,2,3,4,5])
        values={'now':'2031-04-05T10:00'}
        exec(calendar_code(spec),{'vars':values})
        self.assertIn('2031-04-08 Tuesday | business day AFTER today #1',values['calendar_facts'])

    def test_array_products_use_actual_lateness_and_missing_values_do_not_become_zero(self):
        values={'now':'2031-04-02T10:00','payment_offer_quote':'April 4','payment_offer_date':'2031-04-04',
                'get_account_response.data.products':[{'product_id':'synthetic','days_late':5}]}
        code=offer_code({'holidays':['2031-05-01']}, [[1,20,4]])
        exec(code,{'vars':values})
        self.assertIn('PRODUCT synthetic',values['payment_date_facts'])
        values['payment_offer_quote']='April 4'
        del values['get_account_response.data.products'][0]['days_late']
        exec(code,{'vars':values})
        self.assertIn('unavailable',values['payment_date_facts'])


if __name__ == '__main__': unittest.main()
