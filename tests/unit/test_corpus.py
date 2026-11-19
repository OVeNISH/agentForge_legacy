"""CP1 inventory and execution-evidence checks; never execute legacy code here."""

import hashlib
import json
from pathlib import Path
import unittest


CORPUS = Path(__file__).resolve().parents[2] / 'corpus'


class CorpusTests(unittest.TestCase):
    def test_inventory_has_provenance_and_all_required_hazards(self):
        projects = json.loads((CORPUS / 'manifest.json').read_text())['projects']
        self.assertGreaterEqual(len(projects), 4)
        self.assertLessEqual(len(projects), 6)
        self.assertEqual(len({p['id'] for p in projects}), len(projects))
        self.assertEqual(sum(p['golden'] for p in projects), 1)
        hazards = set()
        for project in projects:
            with self.subTest(project=project['id']):
                self.assertTrue((CORPUS / project['entry_point']).is_file())
                self.assertTrue(project['source'])
                self.assertEqual(project['license'], 'MIT')
                self.assertIn('Permission is hereby granted',
                              (CORPUS / project['license_file']).read_text())
                hazards.update(project['hazards'])
        self.assertEqual(hazards, {
            'print', 'except', 'dict_iteration', 'integer_division',
            'str_bytes_unicode', 'map_filter_zip', 'comparison_sort',
            'relative_import', 'file_io', 'time_random',
        })

    def test_every_project_has_successful_evidence_for_current_sources(self):
        projects = json.loads((CORPUS / 'manifest.json').read_text())['projects']
        evidence = json.loads((CORPUS / 'evidence' / 'cp1-runs.json').read_text())
        records = evidence['runs']
        self.assertEqual(sorted(r['project'] for r in records),
                         sorted(p['id'] for p in projects))
        self.assertTrue(evidence['image_id'].startswith('sha256:'))
        for record in records:
            with self.subTest(project=record['project']):
                self.assertEqual(record['exit_code'], 0)
                self.assertTrue(record['output'])
                sources = {
                    str(path.relative_to(CORPUS)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in (CORPUS / record['project']).rglob('*.py')
                }
                self.assertTrue(sources)
                self.assertEqual(record['source_sha256'], sources)
