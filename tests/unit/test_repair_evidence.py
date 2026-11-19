import importlib.util
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('repair_corpus', ROOT / 'scripts/repair_corpus.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class RepairEvidenceTests(unittest.TestCase):
    def test_raw_runs_caps_checksums_heldout_separation_and_diffs_recompute(self):
        summary = verifier.verify_archive(ROOT / 'docs/evidence/cp9.tar.gz')
        self.assertEqual(sum(p['final']['passed'] for p in summary['projects']), 25)
        self.assertEqual(sum(p['final']['tests'] for p in summary['projects']), 73)
        self.assertEqual(sum(p['heldout']['passed'] for p in summary['projects']), 3)
        self.assertEqual(sum(p['heldout']['tests'] for p in summary['projects']), 15)
        self.assertEqual(sum(len(p['attempts']) for p in summary['projects']), 30)
        self.assertTrue(all(p['status'] == 'needs_human_review' for p in summary['projects']))
        self.assertTrue(all(p['usage']['known_total_tokens'] == 0 for p in summary['projects']))

    def test_tampered_counts_or_heldout_records_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with tarfile.open(ROOT / 'docs/evidence/cp9.tar.gz') as archive:
                archive.extractall(root, filter='data')
            path = root / 'golden_ledger/heldout.json'
            original = path.read_text()
            results = json.loads(original)
            results[0]['passed'] = not results[0]['passed']
            path.write_text(json.dumps(results))
            with self.assertRaisesRegex(ValueError, 'raw observation'):
                verifier.verify(root)
            path.write_text(original)
            report_path = root / 'golden_ledger/repair/report.json'
            report = json.loads(report_path.read_text())
            report['retry_counts']['main.py::split_bill'] = 0
            report_path.write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, 'raw run records'):
                verifier.verify(root)


if __name__ == '__main__':
    unittest.main()
