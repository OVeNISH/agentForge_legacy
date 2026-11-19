"""CP8 layered corpus conversion; no characterization verification or repair."""

import argparse
from decimal import Decimal
import json
from pathlib import Path
import tarfile
import tempfile

from modernize.characterize import digest, export_training, read_observation, verify_seal, write_json
from modernize.config import Config
from modernize.documentation import fingerprint, observed_claims
from modernize.llm import LLMResponse, MockLLMClient, TokenUsage
from modernize.llm_run import LLMRun, RateCard
from modernize.sandbox import SandboxRunner
from modernize.transformation import MECHANICAL_WORKER, sandbox_call, transform

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / 'docs/evidence/cp8-proposals.json'


class RecordedTransformationClient(MockLLMClient):
    def complete(self, prompt, **kwargs):
        self.calls.append(prompt)
        context = json.loads(prompt.split('Context JSON:\n', 1)[1])
        plan = json.loads(PROPOSALS.read_text())[context['project']]
        source = dict(context['source'])
        reasons, hazards = {}, {}
        for edit in plan['edits']:
            path = edit['path']
            if source[path].count(edit['before']) != 1:
                raise ValueError('recorded semantic edit does not identify one source site: ' + path)
            source[path] = source[path].replace(edit['before'], edit['after'])
            reasons.setdefault(path, []).append(edit['reason'])
            hazards.setdefault(path, set()).add(edit['hazard'])
        for helper in plan['new_files']:
            if helper['path'] in source:
                raise ValueError('new helper already exists')
            source[helper['path']] = helper['source']
            reasons[helper['path']] = [helper['reason']]
            hazards[helper['path']] = {helper['hazard']}
        response = dict(patches=[dict(path=p, base_sha256=context['source_sha256'].get(p),
            source=source[p], reason=' '.join(reasons[p]), hazards=sorted(hazards[p])) for p in sorted(reasons)],
            needs_human_review=plan['needs_human_review'])
        return LLMResponse(json.dumps(response), self.model, TokenUsage())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if any(output == p or p in output.parents for p in
           (ROOT / 'tests', ROOT / 'corpus', ROOT / 'docs/evidence')):
        raise ValueError('conversion output cannot overwrite protected inputs')
    output.mkdir(parents=True, exist_ok=False)
    archives = [ROOT / 'docs/evidence' / ('cp%s.tar.gz' % n) for n in (5, 6, 7)]
    def protected():
        return fingerprint([ROOT / 'tests', ROOT / 'corpus']) | {
            str(p): digest(p.read_bytes()) for p in archives}
    before = protected()
    write_json(output / 'inputs-before.json', before)
    config = Config()
    legacy, modern = SandboxRunner(config.legacy_image), SandboxRunner(config.modern_image)
    reports = []
    try:
        self_check = sandbox_call(legacy, {}, MECHANICAL_WORKER, 'conversion_worker.py',
            'self_check', (), output / 'mechanical-self-check.json')
        if not self_check['passed']:
            raise ValueError('mechanical converter self-check failed')
        with tempfile.TemporaryDirectory() as oracle, tempfile.TemporaryDirectory() as documented, \
                tempfile.TemporaryDirectory() as exports:
            oracle, documented = Path(oracle), Path(documented)
            for path, destination in ((archives[0], oracle), (archives[2], documented)):
                with tarfile.open(path) as archive:
                    archive.extractall(destination, filter='data')
            facts = json.loads((ROOT / 'docs/evidence/cp2.json').read_text())['facts']
            for project in json.loads((ROOT / 'corpus/manifest.json').read_text())['projects']:
                name = project['id']
                seal = verify_seal(oracle / name)
                exported = export_training(oracle / name, Path(exports) / name)
                fixtures = json.loads((exported / (name + '.json')).read_text())
                files = [f for f in facts['files'] if f['path'].startswith(name + '/')]
                project_facts = dict(files=[{k: v for k, v in f.items() if k not in ('references', 'symbols')}
                    for f in files], calls=[c for c in facts['index']['calls'] if c['path'].startswith(name + '/')],
                    imports=[i for i in facts['index']['imports'] if i['source'].startswith(name + '/')])
                observed = {f['path'] + '::' + fn['qualname']:
                    observed_claims(fixtures, f['path'][len(name)+1:], fn['qualname'])
                    for f in files for fn in f['functions'] if '<lambda@' not in fn['qualname']}
                client = RecordedTransformationClient()
                rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0),
                                 'mock usage only; no provider billing', '2026-11-19')
                llm = LLMRun(client, output / name / 'llm', rates)
                report = transform(documented / name / 'source', name, project_facts, observed,
                                   llm, legacy, modern, output / name)
                if seal != verify_seal(oracle / name):
                    raise ValueError('frozen characterization artifacts changed')
                reports.append(report)
                print(json.dumps(dict(project=name, changed_files=report['changed_files'],
                    compile_import_files=report['compile_import_files'], attempts=report['attempts'])), flush=True)
    finally:
        after = protected()
        write_json(output / 'inputs-after.json', after)
        if before != after:
            raise ValueError('conversion changed protected tests/fixtures/source/evidence')
    write_json(output / 'summary.json', dict(projects=reports, inputs_unchanged=True,
        proposals_sha256=digest(PROPOSALS.read_bytes()),
        provenance='Coding LLM authored semantic edits; deterministic mock replay; no paid provider calls',
        behavior_verification='Deferred to CP9; compilation/import is not behavior equivalence'))


if __name__ == '__main__':
    main()
