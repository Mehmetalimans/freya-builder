"""Incomplete recovery and missing sentiment must never become positive results."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from builder.core import ContractError
from builder.recover import recover, recover_paused
from builder.evaluate import terminal_results_ready
from scripts.summarize_evaluations import sentiment_summary
from test_builder import temporary_directory


class EvidenceTests(unittest.TestCase):
    def test_terminal_reconciliation_preserves_inconclusive_and_requires_quiet_interval(self):
        progress={'runsTotal':1,'runs':[{'personaId':'p','callId':'c','agentWorkflowId':'wf','agentVersionNumber':2,
                                       'outcome':'inconclusive','endedAt':'2031-04-02T10:00:00+00:00'}]}
        from datetime import datetime
        ended=datetime.fromisoformat(progress['runs'][0]['endedAt']).timestamp()
        saved={'workflow_id':'wf','platform_version':2}
        self.assertFalse(terminal_results_ready(progress,{'p'},saved,ended+119))
        self.assertTrue(terminal_results_ready(progress,{'p'},saved,ended+120))
        self.assertEqual(progress['runs'][0]['outcome'],'inconclusive')

    def test_reconciliation_never_accepts_active_unknown_or_wrong_version_calls(self):
        saved={'workflow_id':'wf','platform_version':2}
        for outcome,ended,version in (('running','2031-04-02T10:00:00Z',2),('pass',None,2),('pass','2031-04-02T10:00:00Z',3)):
            progress={'runsTotal':1,'runs':[{'personaId':'p','callId':'c','agentWorkflowId':'wf','agentVersionNumber':version,
                                           'outcome':outcome,'endedAt':ended}]}
            self.assertFalse(terminal_results_ready(progress,{'p'},saved,2000000000))

    def test_measured_result_cannot_be_recovered_again_even_if_pause_metadata_exists(self):
        with temporary_directory() as td:
            directory=Path(td)
            (directory/'evaluation.json').write_text(json.dumps({'status':'measured'}))
            (directory/'evaluation.infrastructure-paused.json').write_text('{}')
            with patch('builder.recover.official_client') as client, self.assertRaises(ContractError):
                recover(directory)
            client.assert_not_called()

    def test_recovery_rejects_missing_or_duplicate_repetitions_before_network(self):
        with temporary_directory() as td:
            directory=Path(td)
            (directory/'result.json').write_text('{}')
            (directory/'evaluation.user-paused.json').write_text(json.dumps({'simulation_id':'last','iteration_id':'it'}))
            for history in ([{'simulation_id':'first','iteration_id':'i'}],
                            [{'simulation_id':'last','iteration_id':'i'}]*3):
                (directory/'simulation-history.json').write_text(json.dumps(history))
                with patch('builder.recover.official_client') as client, self.assertRaises(ContractError):
                    recover_paused(directory)
                client.assert_not_called()

    def test_unlabeled_call_is_not_counted_as_neutral_and_empty_rate_is_null(self):
        with temporary_directory() as td:
            directory=Path(td)
            (directory/'call-1.json').write_text(json.dumps({'analysis':{'successEvaluation':{'success':True}}}))
            rows=[{'call_id':'1'},{'call_id':'2'}]
            missing=sentiment_summary(directory,rows)
            self.assertIsNone(missing['happy_fraction_of_labeled'])
            self.assertEqual(missing['buckets']['neutral'],0)
            (directory/'call-2.json').write_text(json.dumps({'analysis':{'sentiment':'happy'}}))
            mixed=sentiment_summary(directory,rows)
            self.assertEqual(mixed['labeled_calls'],1)
            self.assertEqual(mixed['unlabeled_calls'],1)
            self.assertEqual(mixed['happy_fraction_of_labeled'],1)
            (directory/'call-2.json').write_text(json.dumps({'analysis':{'sentiment':{'unknown_schema':True}}}))
            self.assertIsNone(sentiment_summary(directory,rows)['happy_fraction_of_labeled'])


if __name__ == '__main__': unittest.main()
