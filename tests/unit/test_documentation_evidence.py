import base64
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

from modernize.characterize import digest, read_observation
from modernize.documentation import DocumentationResponse, cross_check, observed_claims, render, WORKER
from modernize.llm_run import recompute_usage
from modernize.sandbox_codec import unpack_input

ROOT = Path(__file__).resolve().parents[2]


class DocumentationEvidenceTests(unittest.TestCase):
    def test_documentation_coverage_claims_and_checksum_proof_recompute(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as oracle:
            root, oracle = Path(directory), Path(oracle)
            for archive, destination in [('cp7.tar.gz', root), ('cp5.tar.gz', oracle)]:
                with tarfile.open(ROOT / 'docs/evidence' / archive) as stream:
                    stream.extractall(destination, filter='data')
            summary = json.loads((root / 'summary.json').read_text())
            before = json.loads((root / 'inputs-before.json').read_text())
            self.assertEqual(before, json.loads((root / 'inputs-after.json').read_text()))
            self.assertTrue(any('/tests/fixtures/' in p for p in before))
            self.assertEqual(summary['proposals_sha256'], digest((ROOT / 'docs/evidence/cp7-proposals.json').read_bytes()))
            check = read_observation(json.loads((root / 'worker-self-check.json').read_text()))
            self.assertTrue(check['passed'])
            self.assertEqual(len(check['checks']), 7)
            facts = json.loads((ROOT / 'docs/evidence/cp2.json').read_text())['facts']
            totals = dict(function=0, **{'class': 0}, module=0, package=0)
            for report in summary['projects']:
                name = report['project']
                store = root / name
                data = json.loads((store / 'documentation.json').read_text())
                entries = data['entries']
                files = [f for f in facts['files'] if f['path'].startswith(name + '/')]
                targets = {f['path'] + '::' + d['qualname'] for f in files
                           for group in ('functions', 'classes') for d in f[group]}
                documented = {e['key'] for e in entries if e['kind'] in ('function', 'class')}
                self.assertEqual(targets, documented | {o['key'] for o in data['omitted']})
                self.assertTrue(all(o['reason'] for o in data['omitted']))
                fixtures = json.loads((oracle / name / 'training' / (name + '.json')).read_text())
                sealed = json.loads((oracle / name / 'sealed' / (name + '.json')).read_text())
                calls = [json.loads(line) for line in (store / 'llm/calls.jsonl').read_text().splitlines()]
                self.assertEqual(len(calls), len(entries))
                mismatches = []
                for entry, call in zip(entries, calls):
                    response = DocumentationResponse.model_validate_json(call['response'], strict=True)
                    self.assertEqual(response.model_dump(), entry['response'])
                    self.assertEqual(render(response), entry['text'])
                    context = json.loads(call['prompt'].split('Context JSON:\n', 1)[1])
                    self.assertEqual((context['kind'], context['key']), (entry['kind'], entry['key']))
                    self.assertEqual(call['validation']['status'], 'passed')
                    self.assertEqual(call['evidence_kind'], 'mock')
                    self.assertTrue(all(f['case']['id'] not in call['prompt'] for f in sealed))
                    if entry['kind'] == 'function':
                        path, target = entry['key'][len(name)+1:].split('::')
                        observed = observed_claims(fixtures, path, target)
                        self.assertEqual(context['observed'], observed)
                        self.assertEqual(entry['observed'], observed)
                        differences = cross_check(response, observed)
                        self.assertEqual(differences, entry['cross_check'])
                        if differences:
                            mismatches.append(dict(key=entry['key'], differences=differences))
                self.assertEqual(report['mismatches'], mismatches)
                kinds = [e['kind'] for e in entries]
                ranks = {'function': 0, 'class': 1, 'module': 2, 'package': 3}
                self.assertEqual([ranks[k] for k in kinds], sorted(ranks[k] for k in kinds))
                for kind in totals:
                    self.assertEqual(report['counts'][kind], kinds.count(kind))
                    totals[kind] += kinds.count(kind)
                record = json.loads((store / 'validation-run.json').read_text())
                self.assertEqual(record['source_sha256'][WORKER], digest((ROOT / 'src/modernize/documentation_worker.py').read_bytes()))
                docs, = unpack_input(record['request']['args'])
                validated = read_observation(record)
                for file in files:
                    path = file['path'][len(name)+1:]
                    self.assertEqual(record['source_sha256'][path], file['sha256'])
                    self.assertTrue(validated[path]['compiled'] and validated[path]['ast_equivalent'])
                    self.assertFalse(validated[path]['omitted'])
                    self.assertEqual((store / 'source' / path).read_bytes(),
                                     base64.b64decode(validated[path]['source_base64']))
                    module = next(e for e in entries if e['kind'] == 'module' and e['key'] == file['path'])
                    self.assertEqual((store / 'modules' / (path + '.md')).read_text(), module['text'] + '\n')
                    for entry in entries:
                        if entry['key'].startswith(file['path'] + '::'):
                            self.assertEqual(docs[path][entry['key'].split('::')[1]], entry['text'])
                self.assertEqual(record['isolation']['NetworkMode'], 'none')
                self.assertTrue(record['isolation']['ReadonlyRootfs'] and record['container_removed'])
                self.assertFalse(record['container_state']['Running'])
                self.assertEqual((store / 'architecture.md').read_text(), entries[-1]['text'] + '\n')
                usage = recompute_usage(store / 'llm')
                self.assertEqual(usage['attempts'], len(entries))
                self.assertEqual(usage['known_total_tokens'], 0)
            self.assertEqual(totals, dict(function=16, **{'class': 1}, module=7, package=4))


if __name__ == '__main__':
    unittest.main()
