import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('report_corpus', ROOT / 'scripts/report_corpus.py')
reporting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reporting)


class ReportingTests(unittest.TestCase):
    def test_report_recomputes_shared_denominators_and_all_required_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'report'
            report = reporting.generate(output)
            self.assertEqual(reporting.verify(output), report)
            self.assertEqual(report['status'], 'needs_human_review')
            totals = report['totals']
            self.assertEqual(totals['legacy_on_legacy']['passed'], 88)
            self.assertEqual(totals['legacy_on_modern']['passed'], 3)
            self.assertEqual(totals['converted_on_modern']['passed'], 28)
            self.assertEqual({v['tests'] for k, v in totals.items() if k.endswith(('legacy', 'modern'))}, {88})
            self.assertEqual((totals['heldout_passed'], totals['heldout_tests']), (3, 15))
            self.assertEqual((totals['quarantined'], totals['repair_proposals'], totals['accepted_repairs']), (5, 30, 0))
            self.assertEqual(totals['usage']['known_total_tokens'], 0)
            self.assertEqual(totals['usage']['known_estimated_usd'], '0')
            self.assertEqual(totals['usage']['evidence_kinds'], {'mock': totals['usage']['attempts']})
            self.assertTrue(any(p['suspected_legacy_bugs'] for p in report['projects']))
            for project in report['projects']:
                self.assertEqual(project['rates']['converted_on_modern']['passed'],
                                 project['training']['passed'] + project['heldout']['passed'])
                self.assertEqual(len(project['unresolved']), project['rates']['converted_on_modern']['tests'] -
                                 project['rates']['converted_on_modern']['passed'])
                self.assertTrue(all(f['run'].startswith('cp9.tar.gz!/') for f in project['unresolved']))
                kinds = {e['kind'] for e in project['documentation']['entries']}
                self.assertTrue({'function', 'module', 'package'} <= kinds)
                self.assertTrue(project['diffs'])
                self.assertTrue(all(q['reason'] for q in project['quarantine']))
            with self.assertRaises(FileExistsError):
                reporting.generate(output)

    def test_edited_report_numbers_and_markdown_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'report'
            report = reporting.generate(output)
            original = (output / 'report.json').read_text()
            report['totals']['converted_on_modern']['passed'] += 1
            (output / 'report.json').write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, 'JSON differs'):
                reporting.verify(output)
            (output / 'report.json').write_text(original)
            with (output / 'report.md').open('a') as stream:
                stream.write('Invented claim: all tests passed.\n')
            with self.assertRaisesRegex(ValueError, 'Markdown differs'):
                reporting.verify(output)

    def test_tampered_raw_replay_is_rejected_before_publishing(self):
        extract = reporting.extract
        def tamper(stage, output):
            extract(stage, output)
            if stage == 9:
                path = output / 'golden_ledger/heldout.json'
                records = reporting.read(path)
                records[0]['passed'] = not records[0]['passed']
                path.write_text(json.dumps(records))
        with tempfile.TemporaryDirectory() as directory, patch.object(reporting, 'extract', tamper):
            output = Path(directory) / 'report'
            with self.assertRaisesRegex(ValueError, 'raw observation'):
                reporting.generate(output)
            self.assertFalse(output.exists())
        with self.assertRaisesRegex(ValueError, 'protected inputs'):
            reporting.generate(ROOT / 'tests/new-report')


if __name__ == '__main__':
    unittest.main()
