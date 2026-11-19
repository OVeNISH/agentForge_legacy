import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]


class TerminalCLITests(unittest.TestCase):
    def test_guided_session_help_project_errors_and_quit(self):
        result = subprocess.run([sys.executable, '-m', 'modernize', 'tui'], cwd=ROOT,
            env=dict(os.environ, PYTHONPATH=str(ROOT / 'src'), NO_COLOR='1'),
            input='/help\n/project ranking\n/status\n/unknown\n/quit\n',
            capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        for expected in ('Guided terminal', '/scan', '/review', '/verify', '/test',
                         str(ROOT / 'corpus/ranking'), 'Unknown command', 'Session closed'):
            self.assertIn(expected, result.stdout)
        self.assertEqual(result.stderr, '')

    def test_eof_exits_and_invalid_configuration_never_opens_session(self):
        command = [sys.executable, '-m', 'modernize']
        environment = dict(os.environ, PYTHONPATH=str(ROOT / 'src'))
        result = subprocess.run(command + ['tui'], input='', capture_output=True, text=True,
                                cwd=ROOT, env=environment, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Session closed', result.stdout)
        result = subprocess.run(command + ['--config', '/nonexistent/modernize-config.json', 'tui'],
            input='/quit\n', capture_output=True, text=True, cwd=ROOT, env=environment, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Guided terminal', result.stdout)
