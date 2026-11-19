import importlib.util
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('verify_cp5', ROOT/'scripts/verify_cp5.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class CharacterizationEvidenceTests(unittest.TestCase):
    def test_raw_evidence_recomputes_checkpoint_metrics(self):
        result = verifier.verify_archive(ROOT/'docs/evidence/cp5.tar.gz')
        self.assertEqual(result['totals']['passes'], result['totals']['comparisons'])
        self.assertEqual(result['totals']['accepted'], 88)
        self.assertEqual(result['heldout_passes'], 15)
        self.assertEqual((result['mutations_detected'],result['mutations_total']), (7,8))
        self.assertEqual(result['totals']['quarantined'], 5)

    def test_golden_capture_agrees_with_hand_checkable_division(self):
        with tempfile.TemporaryDirectory() as directory:
            with tarfile.open(ROOT/'docs/evidence/cp5.tar.gz') as archive:
                archive.extractall(directory, filter='data')
            fixtures = [fixture for folder in ('training','sealed') for fixture in
                json.loads((Path(directory)/'golden_ledger'/folder/'golden_ledger.json').read_text())]
            for args, expected in (([7,2], '3'), ([-7,2], '-4')):
                fixture = next(f for f in fixtures if f['case']['target'] == 'split_bill'
                               and json.loads(f['case']['args_json']) == args)
                self.assertEqual(fixture['expected']['outcome']['value'], {'type':'int','value':expected})


if __name__ == '__main__':
    unittest.main()
