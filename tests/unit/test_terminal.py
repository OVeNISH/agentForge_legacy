import contextlib
import io
import json
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from modernize.analysis import Python2Adapter
from modernize.cli import main
from modernize.terminal import Terminal, plain, repository


class TerminalTests(unittest.TestCase):
    def test_installed_scan_uses_isolated_python_without_repository_scripts(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d).resolve()
            with patch('modernize.terminal.repository', return_value=None):
                terminal = Terminal()
            terminal.project = source
            with patch.object(terminal, 'output_folder', return_value=source.parent / 'scan-output'), \
                    patch.object(terminal, 'analysis_options', return_value=['--analysis', 'sequential']), \
                    patch.object(terminal, 'job', return_value=0) as job, contextlib.redirect_stdout(io.StringIO()):
                terminal.scan_command()
            self.assertEqual(job.call_args.args[0][:5], [sys.executable, '-u', '-I', '-m', 'modernize'])
            with self.assertRaisesRegex(ValueError, 'checkout'):
                terminal.script('run_pipeline.py')

    def test_output_reprompts_for_existing_or_nested_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d).resolve()
            source = root / 'project'
            source.mkdir()
            output = root / 'new-output'
            terminal = Terminal()
            with patch.object(terminal, 'ask', side_effect=[str(source), str(source / 'nested'), str(output)]), \
                    contextlib.redirect_stdout(io.StringIO()) as text:
                self.assertEqual(terminal.output_folder('scan', source), output)
            self.assertIn('already exists', text.getvalue())
            self.assertIn('outside the input project', text.getvalue())
            self.assertFalse(output.exists())

    def test_scan_keeps_custom_paths_as_single_arguments_and_config(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / 'project with spaces; literal'
            source.mkdir()
            output = root / 'output'
            config = root / 'config.json'
            terminal = Terminal(config)
            terminal.project = source
            with patch.object(terminal, 'ask', return_value=str(output)), \
                    patch.object(terminal, 'choose', side_effect=['parallel', '2']), \
                    patch.object(terminal, 'job', return_value=0) as job, contextlib.redirect_stdout(io.StringIO()):
                terminal.scan_command()
            command = job.call_args.args[0]
            self.assertEqual(command[command.index('scan') + 1], str(source))
            self.assertEqual(command[command.index('--config') + 1], str(config.resolve()))
            self.assertEqual(command[-4:], ['--analysis', 'parallel', '--workers', '2'])

    def test_run_requires_registered_project_and_explicit_policy_selection(self):
        with tempfile.TemporaryDirectory() as d:
            terminal = Terminal()
            output = Path(d) / 'run'
            def execute(command):
                output.mkdir()
                (output / 'run.json').write_text('{}')
                (output / 'report.json').write_text(json.dumps(dict(projects=[dict(project='golden_ledger',
                    rates=dict(converted_on_modern=dict(passed=0, tests=1)),
                    policy=dict(passed=0, tests=1, heldout=dict(passed=0, tests=1)))])))
                return 3
            text = io.StringIO()
            with patch.object(terminal, 'ask', return_value=str(output)), \
                    patch.object(terminal, 'choose', side_effect=['golden_ledger', 'python2-python3.v1', 'sequential']), \
                    patch.object(terminal, 'job', side_effect=execute) as job, contextlib.redirect_stdout(text):
                terminal.run_command()
            command = job.call_args.args[0]
            self.assertEqual(command[command.index('--comparison') + 1], 'python2-python3.v1')
            self.assertEqual(terminal.output, output.resolve())
            self.assertIn('Raw', text.getvalue())
            self.assertIn('Policy', text.getvalue())
            terminal.project = Path(d)
            with self.assertRaisesRegex(ValueError, 'registered corpus'):
                terminal.run_command()

    def test_worker_exit_codes_stream_output_without_terminal_control_injection(self):
        terminal = Terminal()
        for code in (0, 3):
            text = io.StringIO()
            with contextlib.redirect_stdout(text):
                terminal.color = False
                actual = terminal.job([sys.executable, '-c',
                    "import sys; print(chr(27) + '[2Jworker output'); sys.exit(" + str(code) + ')'])
            self.assertEqual(actual, code)
            self.assertNotIn('\x1b', text.getvalue())
            self.assertIn('worker output', text.getvalue())
            if code == 3:
                self.assertIn('unresolved', text.getvalue())
        self.assertEqual(plain('a\x1b\x07\x9db\n'), 'ab\n')

    def test_review_is_read_only_and_rejects_external_symlinks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            output = root / 'run'
            output.mkdir()
            facts = output / 'facts.json'
            facts.write_text('safe\x1b[2Jcontent')
            before = facts.read_bytes()
            terminal = Terminal()
            with patch.object(terminal, 'choose', return_value='facts'), patch('modernize.terminal.pydoc.pager') as pager:
                terminal.review_command(str(output))
            self.assertNotIn('\x1b', pager.call_args.args[0])
            self.assertEqual(facts.read_bytes(), before)
            target = output / 'p/repair/source'
            target.mkdir(parents=True)
            external = root / 'outside.py'
            external.write_text('secret')
            (target / 'escape.py').symlink_to(external)
            with patch.object(terminal, 'choose', return_value='source'), self.assertRaisesRegex(ValueError, 'No saved'):
                terminal.review_command(str(output))

    def test_cancellation_signals_controller_and_waits_for_cleanup(self):
        class Interrupted:
            first = True
            def __iter__(self):
                if self.first:
                    self.first = False
                    raise KeyboardInterrupt
                return iter(['cleanup finished\n'])
        process = MagicMock()
        process.stdout = Interrupted()
        process.wait.return_value = -signal.SIGINT
        with patch('modernize.terminal.subprocess.Popen') as popen, contextlib.redirect_stdout(io.StringIO()):
            popen.return_value.__enter__.return_value = process
            self.assertEqual(Terminal().job(['worker']), 130)
        process.send_signal.assert_called_once_with(signal.SIGINT)
        self.assertTrue(popen.call_args.kwargs['start_new_session'])
        with patch('modernize.analysis.subprocess.run', side_effect=[KeyboardInterrupt, subprocess.CompletedProcess([], 0)] ) as run:
            adapter = Python2Adapter('legacy')
            adapter.image_id = 'sha256:example'
            with self.assertRaises(KeyboardInterrupt):
                adapter._parse_one(('m.py', b'pass'))
            self.assertEqual(run.call_args_list[-1].args[0][:3], ['docker', 'rm', '-f'])

    def test_interactive_auto_launch_and_repo_detection(self):
        with patch('modernize.cli.sys.stdin.isatty', return_value=True), \
                patch('modernize.terminal.launch', return_value=0) as launch:
            self.assertEqual(main([]), 0)
            launch.assert_called_once_with(None)
        expected = Path(__file__).resolve().parents[2]
        with patch('modernize.terminal.Path.cwd', return_value=Path('/tmp/untrusted-project')):
            self.assertEqual(repository(), expected)
        with patch('modernize.terminal.repository', return_value=None):
            terminal = Terminal()
            with self.assertRaisesRegex(ValueError, 'checkout'):
                terminal.script('run_pipeline.py')

    def test_structured_worker_output_is_readable_and_preserves_raw_policy_distinction(self):
        terminal = Terminal()
        text = io.StringIO()
        command = [sys.executable, '-c', "import json; print(json.dumps({'status':'needs_human_review','totals':{'converted_on_modern':{'passed':1,'tests':2}}},indent=2)); print(json.dumps({'policy':{'name':'example','passed':2,'tests':2,'heldout_passed':1,'heldout_tests':1}},indent=2))"]
        with contextlib.redirect_stdout(text):
            terminal.job(command)
        self.assertIn('Raw converted: 1/2', text.getvalue())
        self.assertIn('Policy example: 2/2; held-out 1/1', text.getvalue())
        self.assertIn('needs_human_review', text.getvalue())
