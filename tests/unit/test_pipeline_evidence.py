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


class PipelineEvidenceTests(unittest.TestCase):
    def test_clean_checkouts_reproduce_strict_failures_from_fresh_raw_records(self):
        evidence = ROOT / 'docs/evidence'
        metadata = json.loads((evidence / 'cp11.json').read_text())
        archive = evidence / metadata['archive']
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), metadata['archive_sha256'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with tarfile.open(archive) as stream:
                stream.extractall(root, filter='data')
            reports = []
            for name in ('first', 'second'):
                output = root / name
                run = json.loads((output / 'run.json').read_text())
                self.assertEqual(run['revision'], metadata['clean_revision'])
                self.assertEqual(run['tracked_changes'], '')
                self.assertEqual(run['status'], 'needs_human_review')
                self.assertEqual(metadata['process_results'][name]['exit_code'], 3)
                report = verify(output)
                self.assertEqual(report['totals']['converted_on_modern']['passed'], 28)
                self.assertEqual(report['totals']['converted_on_modern']['tests'], 88)
                self.assertEqual(report['totals']['heldout_passed'], 3)
                self.assertEqual(report['totals']['heldout_tests'], 15)
                for project in run['projects']:
                    store = output / project
                    heldout = json.loads((store / 'characterization/sealed' / (project + '.json')).read_text())
                    prompts = (store / 'repair-llm/calls.jsonl').read_text()
                    self.assertTrue(all(f['case']['id'] not in prompts for f in heldout))
                reports.append({p['project']: dict(rates=p['rates'], heldout=p['heldout']) for p in report['projects']})
            self.assertEqual(reports[0], reports[1])


if __name__ == '__main__':
    unittest.main()
