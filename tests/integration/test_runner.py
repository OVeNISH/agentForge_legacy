from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


RUNNER = Path(__file__).resolve().parents[2] / "scripts" / "test.py"


class RunnerTests(unittest.TestCase):
    def run_suites(self, unit_passes=True, integration_passes=True, empty_unit=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            shutil.copyfile(RUNNER, root / "scripts" / "test.py")
            for group, passes in (("unit", unit_passes), ("integration", integration_passes)):
                suite = root / "tests" / group
                suite.mkdir(parents=True)
                if group == "unit" and empty_unit:
                    continue
                (suite / f"test_{group}_probe.py").write_text(
                    "import unittest\n"
                    "class Probe(unittest.TestCase):\n"
                    f"    def test_probe(self): self.assertTrue({passes!r})\n"
                )
            return subprocess.run([sys.executable, str(root / "scripts" / "test.py")],
                                  capture_output=True, text=True, timeout=10)

    def test_runs_unit_before_integration(self):
        result = self.run_suites()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["Running unit tests", "Running integration tests"])

    def test_actual_unit_failure_stops_integration(self):
        result = self.run_suites(unit_passes=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("FAILED (failures=1)", result.stderr)
        self.assertNotIn("Running integration tests", result.stdout)

    def test_actual_integration_failure_returns_nonzero(self):
        result = self.run_suites(integration_passes=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Running integration tests", result.stdout)
        self.assertIn("FAILED (failures=1)", result.stderr)

    def test_empty_suite_is_not_success(self):
        result = self.run_suites(empty_unit=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("No unit tests discovered", result.stderr)
