import hashlib
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from run_pipeline import verify
from revalidation_inputs import exposed_ids


class PipelineFinalEvidenceTests(unittest.TestCase):
    def test_failed_evaluation_is_preserved_and_fresh_clean_runs_reproduce_policy_passes(self):
        evidence = ROOT / 'docs/evidence'
        metadata = json.loads((evidence / 'cp11-final.json').read_text())
        reports = []
        for archive_name, checksum, succeeded in [(metadata['failed_archive'], metadata['failed_archive_sha256'], False),
                                                  (metadata['archive'], metadata['archive_sha256'], True)]:
            archive = evidence / archive_name
            self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), checksum)
            with tempfile.TemporaryDirectory() as d:
                root = Path(d)
                with tarfile.open(archive) as stream:
                    stream.extractall(root, filter='data')
                for name in ('first', 'second'):
                    output = root / name
                    report = verify(output)
                    if not succeeded:
                        self.assertEqual(report['status'], 'needs_human_review')
                        self.assertEqual((report['policy']['passed'], report['policy']['tests']), (87, 88))
                        self.assertEqual((report['policy']['heldout_passed'], report['policy']['heldout_tests']), (14, 15))
                        continue
                    run = json.loads((output / 'run.json').read_text())
                    self.assertEqual(run['revision'], metadata['clean_revision'])
                    self.assertEqual(run['tracked_changes'], '')
                    self.assertEqual(metadata['process_results'][name]['exit_code'], 0)
                    self.assertEqual(report['status'], 'passed')
                    self.assertEqual((report['policy']['passed'], report['policy']['tests']), (120, 120))
                    self.assertEqual((report['policy']['heldout_passed'], report['policy']['heldout_tests']), (16, 16))
                    self.assertEqual(report['totals']['converted_on_modern']['passed'], 38)
                    self.assertEqual(report['totals']['quarantined'], 5)
                    self.assertEqual(report['totals']['accepted_repairs'], 2)
                    for project in report['projects']:
                        store = output / project['project']
                        oracle = store / 'characterization'
                        training = json.loads((oracle / 'training' / (project['project'] + '.json')).read_text())
                        heldout = json.loads((oracle / 'sealed' / (project['project'] + '.json')).read_text())
                        known = exposed_ids(project['project'])
                        self.assertTrue(all(f['case']['id'] not in known for f in heldout))
                        eligible_known = known & {f['case']['id'] for f in training + heldout}
                        self.assertTrue(eligible_known <= {f['case']['id'] for f in training})
                        for path in (store / 'documentation/llm/calls.jsonl', store / 'conversion/llm/calls.jsonl', store / 'repair-llm/calls.jsonl'):
                            prompts = path.read_text()
                            self.assertTrue(all(f['case']['id'] not in prompts for f in heldout))
                        self.assertTrue(project['policy']['source_review_matches'])
                    reports.append({p['project']: dict(rates=p['rates'], policy=p['policy']) for p in report['projects']})
        self.assertEqual(reports[0], reports[1])
