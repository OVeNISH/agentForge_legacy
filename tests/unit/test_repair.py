from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from modernize.characterize import digest
from modernize.llm import MockLLMClient
from modernize.llm_run import LLMRun, RateCard, RetryPolicy
from modernize.repair import failure_context, load_repair_prompt, metrics, repair, review_changes
from modernize.transformation import SourceChanges


def result(case_id, value):
    actual = dict(outcome=dict(status='completed', value=dict(type='int', value=str(value)), state=None),
                  stdout_base64='', stderr_base64='', files=[], target_exit_code=0)
    observation = dict(outcome=actual['outcome'], traceback=[])
    record = dict(container_removed=True, result=dict(status='completed',
        value=dict(type='str', value=json.dumps(observation)), exception=None,
        target_exit_code=0, stdout_base64='', stderr_base64='', files=[], capture_error=None))
    return dict(id=case_id, actual=actual, record=record, passed=value == 1)


def fixture(case_id='visible', target='f'):
    return dict(case=dict(id=case_id, path='m.py', target=target), expected=result(case_id, 1)['actual'])


class RepairTests(unittest.TestCase):
    def test_prompt_schema_retry_and_failure_diagnostics(self):
        prompt = load_repair_prompt()
        response = dict(patches=[], needs_human_review=['Exact runtime identity cannot be preserved.'])
        with tempfile.TemporaryDirectory() as directory:
            client = MockLLMClient(replies=('{}', json.dumps(response)))
            rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0), 'mock', '2026-11-19')
            llm = LLMRun(client, Path(directory) / 'llm', rates, RetryPolicy(backoff_seconds=0))
            self.assertEqual(llm.generate(prompt, {}).model_dump(), response)
            self.assertEqual(llm.records[0]['validation']['status'], 'failed')
        failure = failure_context([fixture()], [result('visible', 0)], ('m.py', 'f'))[0]
        self.assertIn('--- expected', failure['diff'])
        self.assertEqual(failure['traceback'], [])
        with self.assertRaises(ValueError):
            metrics([fixture()], [dict(result('visible', 0), passed=True)])

    def run_loop(self, proposed_source, *, regress=False):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        project, output = root / 'input', root / 'output'
        project.mkdir()
        original = b'def f(x):\n    return x\n'
        (project / 'm.py').write_bytes(original)
        fixtures = [fixture()]
        if regress:
            fixtures.append(fixture('other', 'g'))
        contexts = []
        class Proposer:
            def generate(self, prompt, context):
                contexts.append(context)
                return SourceChanges.model_validate(dict(patches=[] if proposed_source is None else [dict(
                    path='m.py', base_sha256=context['source_sha256']['m.py'], source=proposed_source,
                    reason='Restore integer result.', hazards=['division'])], needs_human_review=[]))
        def execute(runner, files, fixtures):
            fixed = b'+ 1' in files['m.py']
            values = [result('visible', int(fixed))]
            if regress:
                values.append(result('other', int(not fixed)))
            return values
        with patch('modernize.repair.replay', side_effect=execute), \
                patch('modernize.repair.sandbox_call', return_value=dict(files=[dict(
                    path='m.py', compiled=True, imported=True, definitions=[])])):
            report = repair(project, 'p', dict(files=[]), fixtures, Proposer(), None, output)
        self.assertEqual((project / 'm.py').read_bytes(), original)
        self.assertEqual(fixtures, [fixture()] + ([fixture('other', 'g')] if regress else []))
        self.assertTrue(all('sealed' not in c and 'heldout' not in c for c in contexts))
        return report, contexts, output

    def test_accepts_fix_and_publishes_only_validated_source(self):
        report, contexts, output = self.run_loop('def f(x):\n    return x + 1\n')
        self.assertEqual(report['final']['passed'], 1)
        self.assertEqual(report['retry_counts'], {'m.py::f': 1})
        self.assertEqual(report['status'], 'training_passed')
        self.assertEqual(len(contexts), 1)
        self.assertIn(b'+ 1', (output / 'source/m.py').read_bytes())

    def test_caps_invalid_and_empty_proposals_without_publication(self):
        for source in ('def broken(', None):
            with self.subTest(source=source):
                report, contexts, output = self.run_loop(source)
                self.assertEqual(report['retry_counts'], {'m.py::f': 2})
                self.assertEqual(report['status'], 'needs_human_review')
                self.assertTrue(all(not a['accepted'] for a in report['attempts']))
                self.assertTrue(contexts[1]['previous_error'])
                self.assertEqual((output / 'source/m.py').read_text(), 'def f(x):\n    return x\n')

    def test_regression_rejects_candidate_even_when_one_failure_is_fixed(self):
        report, contexts, output = self.run_loop('def f(x):\n    return x + 1\n', regress=True)
        self.assertEqual(report['final']['passed'], 1)
        self.assertEqual(report['retry_counts'], {'m.py::f': 2})
        self.assertTrue(all('regressing' in a['error'] for a in report['attempts']))
        self.assertNotIn(b'+ 1', (output / 'source/m.py').read_bytes())

    def test_diff_scan_flags_branches_exception_handlers_and_fixture_access(self):
        review = review_changes({'m.py': b'def f(x):\n    return x\n'}, {'m.py': b'''
import fixtures.data
def f(x):
    try:
        if x == 7:
            return 'expected'
    except Exception:
        pass
'''})
        self.assertEqual(review['status'], 'needs_human_review')
        self.assertEqual({f['rule'] for f in review['findings']}, {
            'changed_branch_count', 'changed_exception_handler_count', 'protected_import', 'fixture_reference'})


if __name__ == '__main__':
    unittest.main()
