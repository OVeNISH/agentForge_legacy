import os
from pathlib import Path
import subprocess
import sys
import unittest


class TerminalMenuTests(unittest.TestCase):
    def test_numbered_menu_selects_project_then_returns_to_prompt_and_exits(self):
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run([sys.executable, '-m', 'modernize', 'tui'], cwd=root,
            env=dict(os.environ, PYTHONPATH=str(root / 'src'), NO_COLOR='1'),
            input='\n1\nranking\n/help\n/menu\n/quit\n',
            capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        self.assertNotIn('\x1b', result.stdout)
        for expected in ('QUICK START', 'What would you like to do?', 'YOUR WORKSPACE',
                         str(root / 'corpus/ranking'), 'EXPLORE RESULTS', 'Session closed'):
            self.assertIn(expected, result.stdout)
        self.assertGreaterEqual(result.stdout.count('modernize> '), 3)
