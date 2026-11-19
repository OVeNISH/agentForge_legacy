import copy
import importlib.util
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('baseline_corpus', ROOT / 'scripts/baseline_corpus.py')
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)


class BaselineTests(unittest.TestCase):
    def test_failure_groups_preserve_exact_comparison(self):
        expected = dict(outcome=dict(status='completed', value={'type': 'int', 'value': '3'}),
                        stdout_base64='', stderr_base64='', files=[], target_exit_code=0)
        self.assertIsNone(baseline.failure_category(expected, expected))
        for name, category in [('SyntaxError', 'syntax_error'), ('ModuleNotFoundError', 'import_error'),
                               ('TypeError', 'runtime_exception:TypeError')]:
            actual = dict(expected, outcome=dict(status='exception', name=name))
            self.assertEqual(baseline.failure_category(expected, actual), category)
        actual = copy.deepcopy(expected)
        actual['outcome']['value'] = {'type': 'float', 'value': '3.0'}
        self.assertEqual(baseline.failure_category(expected, actual), 'outcome_mismatch')
        self.assertEqual(baseline.failure_category(expected, dict(expected, stdout_base64='IA==')),
                         'stdout_base64_mismatch')

    def test_archived_baseline_recomputes_and_detects_tampering(self):
        result = baseline.verify_archive(ROOT / 'docs/evidence/cp6.tar.gz')
        self.assertEqual(len(result['projects']), 4)
        self.assertEqual(sum(p['legacy']['tests'] for p in result['projects']), 88)
        for project in result['projects']:
            self.assertEqual(project['legacy']['pass_rate_percent'], 100)
            self.assertEqual(project['modern']['tests'], project['legacy']['tests'])
        with self.assertRaisesRegex(ValueError, 'every eligible fixture'):
            baseline.summarize([{'case': {'id': 'a'}, 'expected': {}}], [])
        with tempfile.TemporaryDirectory() as directory:
            with tarfile.open(ROOT / 'docs/evidence/cp6.tar.gz') as archive:
                archive.extractall(directory, filter='data')
            results = json.loads((Path(directory) / 'golden_ledger.json').read_text())['modern']
            with tempfile.TemporaryDirectory() as oracle:
                with tarfile.open(baseline.ORACLE) as archive:
                    archive.extractall(oracle, filter='data')
                fixtures = [f for folder in ('training', 'sealed') for f in json.loads(
                    (Path(oracle) / 'golden_ledger' / folder / 'golden_ledger.json').read_text())]
            results[0]['passed'] = not results[0]['passed']
            with self.assertRaisesRegex(ValueError, 'raw observation'):
                baseline.summarize(fixtures, results)


if __name__ == '__main__':
    unittest.main()
