import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from modernize.terminal import Terminal
from modernize.terminal_widgets import StageChecklist


class TerminalWidgetTests(unittest.TestCase):
    def test_pipeline_job_displays_failed_and_pending_stages_without_hiding_error(self):
        terminal = Terminal()
        process = MagicMock()
        process.stdout = iter(['analysis\n', 'example:characterization\n', 'pipeline error: unavailable\n'])
        process.wait.return_value = 2
        with patch('modernize.terminal.subprocess.Popen') as popen, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            popen.return_value.__enter__.return_value = process
            code = terminal.job(['python', 'run_pipeline.py', '--project', 'example', '--output', '/unused'])
        self.assertEqual(code, 2)
        for label in ('[done] Analyze original code', '[failed] Record legacy behavior / example',
                      '[pending] Check sealed held-out cases / example', 'pipeline error: unavailable'):
            self.assertIn(label, output.getvalue())

    def test_checklist_tracks_only_observed_stages_and_failed_active_step(self):
        progress = StageChecklist(['first', 'second'])
        self.assertEqual(progress.steps[-2:], [('first', 'heldout'), ('second', 'heldout')])
        progress.advance('', 'analysis')
        progress.advance('first', 'characterization')
        self.assertEqual(progress.states[('', 'analysis')], 'done')
        self.assertEqual(progress.states[('first', 'characterization')], 'active')
        progress.advance('first', 'characterization')
        progress.finish(2)
        self.assertEqual(progress.states[('first', 'characterization')], 'failed')
        self.assertEqual(progress.states[('second', 'heldout')], 'pending')
        self.assertIn(('[failed] Record legacy behavior / first', '31'), progress.rows())

    def test_completed_with_review_and_cancellation_have_distinct_states(self):
        for code, expected in ((0, 'done'), (3, 'done'), (130, 'cancelled')):
            with self.subTest(code=code):
                progress = StageChecklist(['example'])
                progress.advance('example', 'heldout')
                progress.finish(code)
                self.assertEqual(progress.states[('example', 'heldout')], expected)
                self.assertEqual(progress.states[('', 'analysis')], 'pending')

    def test_next_actions_open_correct_artifact_verify_and_return(self):
        terminal = Terminal()
        output = Path('/saved/run')
        with patch.object(terminal, 'choose', side_effect=['View report', 'Inspect changes', 'Verify', 'Return to prompt']), \
                patch.object(terminal, 'review_command') as review, patch.object(terminal, 'job') as job:
            self.assertFalse(terminal.next_actions(output))
        self.assertEqual(review.call_args_list[0].kwargs, {'choice': 'report'})
        self.assertEqual(review.call_args_list[1].kwargs, {'choice': 'diffs'})
        self.assertEqual(job.call_args.args[0][-2:], ['--verify', str(output)])
        with patch.object(terminal, 'choose', return_value='Run again'):
            self.assertTrue(terminal.next_actions(output))

    def test_run_again_is_iterative_and_new_output_is_requested(self):
        terminal = Terminal()
        with patch.object(terminal, 'run_once', side_effect=[Path('/run/one'), Path('/run/two')]) as run, \
                patch('modernize.terminal.interactive', return_value=True), \
                patch.object(terminal, 'next_actions', side_effect=[True, False]) as actions:
            terminal.run_command()
        self.assertEqual(run.call_count, 2)
        self.assertEqual(actions.call_args_list[1].args, (Path('/run/two'),))

    def test_summary_names_comparison_and_shows_both_heldout_rates(self):
        rate = lambda passed: dict(passed=passed, tests=3)
        report = dict(comparison='python2-python3.v1', projects=[dict(project='example',
            rates=dict(converted_on_modern=rate(1)), heldout=rate(2),
            policy=dict(**rate(3), heldout=rate(3)))])
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            (output / 'report.json').write_text(json.dumps(report))
            terminal = Terminal()
            terminal.color = False
            text = io.StringIO()
            with contextlib.redirect_stdout(text):
                terminal.summary(output)
        value = text.getvalue()
        self.assertLess(value.index('Comparison mode: python2-python3.v1'), value.index('Raw matches'))
        for label, count in [('Raw matches', '1/3'), ('Policy passes', '3/3'),
                             ('Held-out raw', '2/3'), ('Held-out policy', '3/3')]:
            self.assertRegex(value, label + r'\s+' + count)

    def test_worker_failure_is_red_and_review_is_amber_with_labels(self):
        terminal = Terminal()
        terminal.color = True
        for code, color, label in [(2, '31', 'Input, setup or stage error'), (3, '33', 'unresolved')]:
            with self.subTest(code=code), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(terminal.job([sys.executable, '-c', f'raise SystemExit({code})']), code)
            self.assertIn('\033[' + color + 'm', output.getvalue())
            self.assertIn(label, output.getvalue())

    def test_real_report_comparison_description_does_not_replace_policy_name(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            (output / 'report.json').write_text(json.dumps(dict(
                comparison='Exact comparisons; policy results are separate.',
                policy=dict(name='python2-python3.v1'), projects=[])))
            with contextlib.redirect_stdout(io.StringIO()) as text:
                Terminal().summary(output)
        self.assertIn('Comparison mode: python2-python3.v1', text.getvalue())
        self.assertNotIn('Exact comparisons', text.getvalue())
