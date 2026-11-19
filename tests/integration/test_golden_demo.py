import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GoldenDemoTests(unittest.TestCase):
    def test_demo_preserves_default_and_forwards_explicit_comparison(self):
        for arguments, expected in [([], ['artifacts/golden-demo']),
                                    (['artifacts/demo path', '--comparison', 'python2-python3.v1'],
                                     ['artifacts/demo path', '--comparison', 'python2-python3.v1'])]:
            result = subprocess.run(['sh', 'scripts/demo_golden.sh', *arguments], cwd=ROOT,
                env=dict(os.environ, PYTHON='echo'), capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), 'scripts/run_pipeline.py --project golden_ledger --output ' + ' '.join(expected))
