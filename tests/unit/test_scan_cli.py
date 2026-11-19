import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from modernize.cli import main


class ScanCLITests(unittest.TestCase):
    def test_scan_writes_artifacts_and_records_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'input'
            source.mkdir()
            for success in (True, False):
                output = root / str(success)
                result = {'files': []}
                with patch('modernize.cli.scan', return_value=result,
                           side_effect=None if success else ValueError('broken.py: syntax error')), \
                        redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    if success:
                        self.assertEqual(main(['scan', str(source), '--output', str(output)]), 0)
                        self.assertEqual(json.loads((output / 'facts.json').read_text()), result)
                    else:
                        with self.assertRaises(SystemExit) as exit:
                            main(['scan', str(source), '--output', str(output)])
                        self.assertEqual(exit.exception.code, 2)
                        self.assertFalse((output / 'facts.json').exists())
                record = json.loads((output / 'run.json').read_text())
                self.assertEqual(record['status'], 'passed' if success else 'failed')
                if not success:
                    self.assertIn('broken.py', record['error'])

    def test_output_cannot_overwrite_input_or_existing_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'input'
            source.mkdir()
            existing = root / 'existing'
            existing.mkdir()
            sentinel = existing / 'keep.txt'
            sentinel.write_text('keep')
            for output in (source, source / 'nested', existing):
                with self.subTest(output=output), patch('modernize.cli.scan') as scanning, \
                        redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main(['scan', str(source), '--output', str(output)])
                scanning.assert_not_called()
            self.assertEqual(sentinel.read_text(), 'keep')
