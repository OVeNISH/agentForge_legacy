import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class CLITests(unittest.TestCase):
    def run_cli(self, *arguments):
        environment = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
        return subprocess.run([sys.executable, "-m", "modernize", *arguments],
                              cwd=ROOT, env=environment, capture_output=True,
                              text=True, timeout=10)

    def test_config_stdout_and_structured_stderr(self):
        result = self.run_cli("--config", str(ROOT / "config.example.json"), "config")
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = json.loads((ROOT / "config.example.json").read_text())
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(json.loads(result.stderr)["message"], "configuration_loaded")

    def test_help_and_version(self):
        for argument, expected in (("--help", "config"), ("--version", "modernize 0.1.0")):
            with self.subTest(argument=argument):
                result = self.run_cli(argument)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertEqual(result.stderr, "")

    def test_invalid_config_and_missing_command(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"log_level":"invalid"}')
            for arguments in (("--config", str(path), "config"),
                              ("--config", str(path.parent / "absent.json"), "config"), ()):
                with self.subTest(arguments=arguments):
                    result = self.run_cli(*arguments)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("error:", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
