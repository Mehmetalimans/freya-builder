"""Synthetic policy compilation checks; not live benchmarks or hidden briefs."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from builder.core import compile_workflow
from builder.runtime import KIT

ROOT=Path(__file__).resolve().parent.parent


def fixture_api(label):
    api=json.loads((KIT/'tools/openapi.json').read_text())
    def props(tool):
        return api['paths']['/'+tool]['post']['requestBody']['content']['application/json']['schema']['properties']
    if label=='c': props('transfer_to_agent')['queue']['enum'].append('hardship')
    if label=='d':
        props('transfer_to_agent')['queue']['enum']=['commercial_legal','factoring_support','general']
        props('add_note')['reason']['enum'].append('legal_counsel')
    if label=='e':
        props('transfer_to_agent')['queue']['enum']=['special_care','debt_counseling','general']
        props('add_note')['reason']['enum'] += ['unemployed','fraud_claim']
    return api


class SyntheticPolicies(unittest.TestCase):
    def test_preserves_quoted_policy_and_explicit_attempts_without_public_defaults(self):
        for label,name,bands in [('c','Anatolia Global Bank',[[1,10,1],[11,60,2]]),
                                 ('d','Apex Commercial Finance',[[1,14,1],[15,45,2]]),
                                 ('e','Nordic Trust Financial',[[1,5,1],[6,30,2]])]:
            with self.subTest(label=label):
                text=(ROOT/'briefs'/('brief-'+label+'.md')).read_text()
                wf,analysis=compile_workflow([('synthetic',text)],fixture_api(label))
                self.assertIn(text,wf['system_prompt'])
                self.assertIn(name,wf['system_prompt'])
                self.assertNotIn('Freya Bank',wf['system_prompt'])
                self.assertEqual(analysis['persuasion_limits'],bands)
                self.assertNotIn('reason=queue',json.dumps(wf))
                self.assertNotIn('On any transfer, add no notes at all',json.dumps(wf))

    def test_new_note_and_transfer_values_are_present_in_the_supplied_fixture_contract(self):
        for label,note,queue in [('c','hardship','hardship'),('d','legal_counsel','commercial_legal'),('e','fraud_claim','special_care')]:
            api=fixture_api(label)
            props=lambda tool:api['paths']['/'+tool]['post']['requestBody']['content']['application/json']['schema']['properties']
            self.assertIn(note,props('add_note')['reason']['enum'])
            self.assertIn(queue,props('transfer_to_agent')['queue']['enum'])


if __name__=='__main__': unittest.main()
