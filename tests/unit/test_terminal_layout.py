import contextlib
import io
import os
import sys
import unittest
from unittest.mock import patch

from modernize.terminal import Terminal


class TerminalLayoutTests(unittest.TestCase):
    def test_panel_wraps_paths_without_losing_content_or_allowing_control_bytes(self):
        terminal = Terminal()
        terminal.color = False
        path = '/project/' + 'long-folder/' * 8
        output = io.StringIO()
        with patch('modernize.terminal.shutil.get_terminal_size', return_value=os.terminal_size((40, 24))), \
                contextlib.redirect_stdout(output):
            terminal.panel('WORKSPACE', [path, 'unsafe\x1b\x07text'])
        lines = output.getvalue().splitlines()
        self.assertTrue(all(len(line) <= 40 for line in lines))
        self.assertNotIn('\x1b', output.getvalue())
        self.assertNotIn('\x07', output.getvalue())
        body = ''.join(line[4:-2].strip() for line in lines if line.startswith('  | '))
        self.assertIn(path, body)
        self.assertIn('unsafetext', body)

    def test_empty_command_opens_menu_and_dispatches_selected_action(self):
        terminal = Terminal()
        with patch.object(terminal, 'choose', return_value='/status') as choose, \
                patch.object(terminal, 'status') as status:
            self.assertTrue(terminal.dispatch(''))
        status.assert_called_once()
        self.assertNotIn('/menu', choose.call_args.args[1])
        with patch.object(terminal, 'choose', return_value='/quit'):
            self.assertFalse(terminal.dispatch('/menu'))

    def test_choice_explains_defaults_and_recovers_from_invalid_input(self):
        terminal = Terminal()
        terminal.color = False
        output = io.StringIO()
        with patch('builtins.input', side_effect=['unknown', '']), contextlib.redirect_stdout(output):
            self.assertEqual(terminal.choose('Comparison', ['strict', 'python2-python3.v1']), 'strict')
        for text in ('Compare raw observations exactly', 'keep raw results',
                     'Choose a listed number', 'Enter to use: 1'):
            self.assertIn(text, output.getvalue())

    def test_worker_stages_are_descriptive_and_preserve_arbitrary_output(self):
        terminal = Terminal()
        terminal.color = False
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = terminal.job([sys.executable, '-c',
                "print('analysis'); print('golden_ledger:heldout'); print('ordinary output')"])
        self.assertEqual(code, 0)
        self.assertIn('[Stage] Analyze original code', output.getvalue())
        self.assertIn('[Stage] Check sealed held-out cases / golden_ledger', output.getvalue())
        self.assertIn('ordinary output', output.getvalue())
