import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('run_pipeline', ROOT / 'scripts/run_pipeline.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


def retained_run(root):
    """Use genuine retained replays to test the new report reader offline."""
    output = root / 'run'
    name = 'golden_ledger'
    for n in (5, 6, 7, 8, 9):
        with tarfile.open(ROOT / 'docs/evidence' / ('cp%s.tar.gz' % n)) as archive:
            archive.extractall(root / str(n), filter='data')
    store = output / name
    for source, target in [('5/' + name, 'characterization'), ('7/' + name, 'documentation'),
                           ('8/' + name, 'conversion'), ('9/' + name + '/repair', 'repair'),
                           ('9/' + name + '/llm', 'repair-llm'), ('9/' + name + '/full-diffs', 'diffs')]:
        shutil.copytree(root / source, store / target)
    for source, target in [('9/' + name + '/heldout.json', 'heldout.json'),
                           ('9/' + name + '/final-source-lock.json', 'final-source-lock.json'),
                           ('9/' + name + '/full-review.json', 'review.json')]:
        shutil.copyfile(root / source, store / target)
    documentation = pipeline.read(root / '7/summary.json')['projects'][0]
    pipeline.write_json(store / 'documentation/report.json', documentation)
    pipeline.write_json(store / 'baseline-modern.json', pipeline.read(root / '6' / (name + '.json'))['modern'])
    pipeline.write_json(output / 'run.json', dict(projects=[name]))
    for path in ('inputs-before.json', 'inputs-after.json'):
        pipeline.write_json(output / path, {'protected': 'unchanged'})
    return output


class PipelineTests(unittest.TestCase):
    def test_raw_report_preserves_strict_rates_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            output = retained_run(Path(directory))
            report = pipeline.summarize_run(output)
            self.assertEqual(report['totals']['converted_on_modern']['passed'], 11)
            self.assertEqual(report['totals']['converted_on_modern']['tests'], 18)
            self.assertEqual(report['status'], 'needs_human_review')
            pipeline.write_json(output / 'report.json', report)
            (output / 'report.md').write_text(pipeline.markdown(report))
            self.assertEqual(pipeline.verify(output), report)
            with (output / 'report.md').open('a') as stream:
                stream.write('unsupported claim')
            with self.assertRaisesRegex(ValueError, 'report differs'):
                pipeline.verify(output)
            path = output / 'golden_ledger/heldout.json'
            results = pipeline.read(path)
            results[0]['passed'] = not results[0]['passed']
            pipeline.write_json(path, results)
            with self.assertRaisesRegex(ValueError, 'raw observation'):
                pipeline.summarize_run(output)

    def test_failed_stage_retains_diagnostics_and_checksum_proof(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(pipeline, 'scan', side_effect=ValueError('parse failed')), \
                contextlib.redirect_stdout(io.StringIO()):
            output = Path(directory) / 'run'
            with self.assertRaisesRegex(ValueError, 'parse failed'):
                pipeline.execute(output, 'golden_ledger')
            run = pipeline.read(output / 'run.json')
            self.assertEqual((run['stage'], run['status'], run['error']), ('analysis', 'failed', 'parse failed'))
            self.assertEqual(pipeline.read(output / 'inputs-before.json'), pipeline.read(output / 'inputs-after.json'))
            self.assertFalse((output / 'report.json').exists())
            with self.assertRaises(FileExistsError):
                pipeline.execute(output)
        for path in (ROOT / 'tests/nested', ROOT / 'corpus/nested', ROOT / '.git/nested'):
            with self.assertRaisesRegex(ValueError, 'protected inputs'):
                pipeline.execute(path)

    def test_command_exit_codes_distinguish_review_verification_and_failure(self):
        report = dict(status='needs_human_review', totals={}, projects=[])
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with patch.object(pipeline, 'execute', return_value=report):
                self.assertEqual(pipeline.main(['--output', '/tmp/unused-pipeline-test']), 3)
            with patch.object(pipeline, 'verify', return_value=report):
                self.assertEqual(pipeline.main(['--verify', '/tmp/unused-pipeline-test']), 0)
                self.assertEqual(pipeline.main(['--compare', '/tmp/a', '/tmp/b']), 0)
            with patch.object(pipeline, 'execute', side_effect=ValueError('invalid input')):
                self.assertEqual(pipeline.main(['--output', '/tmp/unused-pipeline-test']), 2)


if __name__ == '__main__':
    unittest.main()
