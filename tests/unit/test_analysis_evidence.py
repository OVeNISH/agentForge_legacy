import hashlib
import json
from pathlib import Path
import unittest

from modernize.facts_schema import PROJECT, validate, validate_files


ROOT = Path(__file__).resolve().parents[2]


class AnalysisEvidenceTests(unittest.TestCase):
    def test_recorded_corpus_analysis_is_complete_valid_and_reproducible(self):
        evidence = json.loads((ROOT / 'docs/evidence/cp2.json').read_text())
        facts = evidence['facts']
        validate(facts, PROJECT)
        validate_files(facts['files'])
        self.assertEqual(facts, evidence['parallel_facts'])
        canonical = json.dumps(facts, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), evidence['normalized_sha256'])
        corpus = ROOT / 'corpus'
        actual = {p.relative_to(corpus).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in corpus.rglob('*.py')}
        self.assertEqual({f['path']: f['sha256'] for f in facts['files']}, actual)
        for mode in ('sequential', 'parallel'):
            run = evidence[mode]
            self.assertEqual(run['status'], 'passed')
            self.assertEqual(sorted(p['path'] for p in run['parses']), sorted(actual))
            self.assertTrue(all(p['returncode'] == 0 for p in run['parses']))
        self.assertEqual(evidence['invalid_source_run']['status'], 'failed')
        for path, digest in evidence['analyzer_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)
