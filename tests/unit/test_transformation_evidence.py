import base64
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

from modernize.characterize import digest, read_observation
from modernize.documentation import observed_claims
from modernize.llm_run import recompute_usage
from modernize.sandbox import snapshot
from modernize.sandbox_codec import unpack_input
from modernize.transformation import (SourceChanges, apply_changes, check_public_api,
    save_diffs, MECHANICAL_WORKER, VALIDATE_WORKER)

ROOT = Path(__file__).resolve().parents[2]


class TransformationEvidenceTests(unittest.TestCase):
    def test_sources_diffs_imports_reasons_and_unchanged_fixtures_recompute(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for number in (5, 7, 8):
                with tarfile.open(ROOT / 'docs/evidence' / ('cp%s.tar.gz' % number)) as archive:
                    archive.extractall(root / str(number), filter='data')
            run = root / '8'
            summary = json.loads((run / 'summary.json').read_text())
            self.assertEqual(summary['proposals_sha256'], digest((ROOT / 'docs/evidence/cp8-proposals.json').read_bytes()))
            self.assertTrue(summary['inputs_unchanged'])
            before = json.loads((run / 'inputs-before.json').read_text())
            self.assertEqual(before, json.loads((run / 'inputs-after.json').read_text()))
            self.assertTrue(any('/tests/fixtures/' in p for p in before))
            for n in (5, 6, 7):
                key = next(p for p in before if p.endswith('/docs/evidence/cp%s.tar.gz' % n))
                self.assertEqual(before[key], digest((ROOT / 'docs/evidence' / ('cp%s.tar.gz' % n)).read_bytes()))
            self.assertTrue(read_observation(json.loads((run / 'mechanical-self-check.json').read_text()))['passed'])
            facts = json.loads((ROOT / 'docs/evidence/cp2.json').read_text())['facts']
            images = {r['image']: r['record']['image_id'] for r in
                      json.loads((ROOT / 'docs/evidence/cp3.json').read_text())['records']}
            total = calls = 0
            for report in summary['projects']:
                name = report['project']
                store = run / name
                original = snapshot(root / '7' / name / 'source')
                self.assertEqual(report['original_sha256'], {p: digest(raw) for p, raw in original.items()})
                mechanical_record = json.loads((store / 'mechanical-run.json').read_text())
                mechanical = read_observation(mechanical_record)
                base = dict(original, **{p: base64.b64decode(raw) for p, raw in mechanical['files'].items()})
                self.assertEqual(base, snapshot(store / 'mechanical'))
                self.assertEqual(mechanical_record['source_sha256'][MECHANICAL_WORKER],
                                 digest((ROOT / 'src/modernize/conversion_worker.py').read_bytes()))
                attempts = json.loads((store / 'attempts.json').read_text())
                self.assertEqual(attempts, report['attempts'])
                self.assertTrue(attempts[-1]['accepted'])
                accepted = attempts[-1]['attempt']
                changes = SourceChanges.model_validate_json((store / ('changes-%s.json' % accepted)).read_text(), strict=True)
                candidate = apply_changes(base, changes)
                self.assertEqual(snapshot(store / 'source'), candidate)
                self.assertEqual(report['converted_sha256'], {p: digest(raw) for p, raw in candidate.items()})
                self.assertEqual(report['semantic_changed_files'], [p.path for p in changes.patches])
                self.assertTrue(all(p.reason and p.hazards for p in changes.patches))
                self.assertEqual(report['needs_human_review'], changes.needs_human_review)
                diffs = root / 'diffs' / name
                changed = save_diffs(original, candidate, diffs)
                self.assertEqual(changed, report['changed_files'])
                self.assertEqual(snapshot(diffs), snapshot(store / 'diffs'))
                record = json.loads((store / ('validation-%s.json' % accepted)).read_text())
                validation = read_observation(record)
                self.assertEqual(record['source_sha256'][VALIDATE_WORKER],
                                 digest((ROOT / 'src/modernize/conversion_validate_worker.py').read_bytes()))
                self.assertEqual(unpack_input(record['request']['args']), (sorted(candidate),))
                self.assertTrue(all(f['compiled'] and f['imported'] for f in validation['files']))
                self.assertEqual(len(validation['files']), report['compile_import_files'])
                for p, raw in candidate.items():
                    self.assertEqual(record['source_sha256'][p], digest(raw))
                check_public_api(validation, dict(files=[f for f in facts['files']
                    if f['path'].startswith(name + '/')]), name)
                for evidence, image in ((mechanical_record, 'modernize-legacy:cp0'),
                                        (record, 'modernize-modern:cp0')):
                    self.assertEqual(evidence['image_id'], images[image])
                    self.assertEqual(evidence['isolation']['NetworkMode'], 'none')
                    self.assertTrue(evidence['isolation']['ReadonlyRootfs'] and evidence['container_removed'])
                    self.assertFalse(evidence['container_state']['Running'])
                fixtures = json.loads((root / '5' / name / 'training' / (name + '.json')).read_text())
                heldout = json.loads((root / '5' / name / 'sealed' / (name + '.json')).read_text())
                logs = [json.loads(line) for line in (store / 'llm/calls.jsonl').read_text().splitlines()]
                for call in logs:
                    self.assertEqual(call['evidence_kind'], 'mock')
                    self.assertEqual(call['validation']['status'], 'passed')
                    self.assertEqual(SourceChanges.model_validate_json(call['response'], strict=True), changes)
                    context = json.loads(call['prompt'].split('Context JSON:\n', 1)[1])
                    self.assertEqual(context['source_sha256'], {p: digest(raw) for p, raw in base.items()})
                    self.assertTrue(all(f['case']['id'] not in call['prompt'] for f in heldout))
                    for key, observed in context['observed_training_types'].items():
                        path, target = key[len(name)+1:].split('::')
                        self.assertEqual(observed, observed_claims(fixtures, path, target))
                usage = recompute_usage(store / 'llm')
                self.assertEqual(usage['attempts'], len(logs))
                self.assertEqual(usage['known_total_tokens'], 0)
                calls += len(logs)
                total += len(validation['files'])
            self.assertEqual((len(summary['projects']), total, calls), (4, 9, 4))


if __name__ == '__main__':
    unittest.main()
