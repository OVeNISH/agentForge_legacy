"""CP7 corpus documentation; coding-LLM prose replayed through the validated mock."""

import argparse
from decimal import Decimal
import json
from pathlib import Path
import tarfile
import tempfile

from modernize.characterize import digest, export_training, verify_seal, write_json
from modernize.config import Config
from modernize.documentation import fingerprint, generate
from modernize.llm import LLMResponse, MockLLMClient, TokenUsage
from modernize.llm_run import LLMRun, RateCard
from modernize.sandbox import SandboxRunner
from verify_cp5 import verify

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / 'docs/evidence/cp7-proposals.json'


class RecordedDocumentationClient(MockLLMClient):
    def complete(self, prompt, **kwargs):
        self.calls.append(prompt)
        context = json.loads(prompt.split('Context JSON:\n', 1)[1])
        summary = json.loads(PROPOSALS.read_text())[context['key']]
        observed = context.get('observed', {})
        response = dict(summary=summary,
            observed_return_types=observed.get('return_types', []),
            observed_exceptions=observed.get('exceptions', []),
            limitations='Source-based description. Claims cover training observations only; '
                'untested inputs, dynamic calls and quarantined behavior are not proven.')
        return LLMResponse(json.dumps(response), self.model, TokenUsage())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if any(output == p or p in output.parents for p in
           (ROOT / 'tests', ROOT / 'corpus', ROOT / 'docs/evidence')):
        raise ValueError('documentation output cannot overwrite protected inputs')
    output.mkdir(parents=True, exist_ok=False)
    protected = [ROOT / 'tests', ROOT / 'corpus', ROOT / 'docs/evidence/cp5.tar.gz',
                 ROOT / 'docs/evidence/cp6.tar.gz']
    # Include archive files as well as directory contents in the same checksum proof.
    before = fingerprint(protected[:2]) | {str(p): digest(p.read_bytes()) for p in protected[2:]}
    write_json(output / 'inputs-before.json', before)
    with tempfile.TemporaryDirectory() as directory:
        from modernize.documentation import WORKER
        from modernize.characterize import read_observation
        staged = Path(directory)
        (staged / WORKER).write_bytes((ROOT / 'src/modernize/documentation_worker.py').read_bytes())
        record = SandboxRunner(Config().legacy_image).run(staged, WORKER, 'self_check')
        write_json(output / 'worker-self-check.json', record)
        if not read_observation(record)['passed']:
            raise ValueError('documentation worker self-check failed')
    reports = []
    with tempfile.TemporaryDirectory() as oracle, tempfile.TemporaryDirectory() as exports:
        oracle = Path(oracle)
        with tarfile.open(ROOT / 'docs/evidence/cp5.tar.gz') as archive:
            archive.extractall(oracle, filter='data')
        verify(oracle)
        seals = {p.name: verify_seal(p) for p in oracle.iterdir() if (p / 'seal.json').is_file()}
        facts = json.loads((ROOT / 'docs/evidence/cp2.json').read_text())['facts']
        for project in json.loads((ROOT / 'corpus/manifest.json').read_text())['projects']:
            name = project['id']
            training = export_training(oracle / name, Path(exports) / name)
            fixtures = json.loads((training / (name + '.json')).read_text())
            client = RecordedDocumentationClient()
            rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0),
                             'mock usage only; no provider billing', '2026-11-19')
            llm = LLMRun(client, output / name / 'llm', rates)
            report = generate(ROOT / 'corpus' / name, name, facts, fixtures, llm,
                              SandboxRunner(Config().legacy_image), output / name)
            reports.append(report)
            print(json.dumps(report), flush=True)
        if seals != {p.name: verify_seal(p) for p in oracle.iterdir() if (p / 'seal.json').is_file()}:
            raise ValueError('characterization evidence changed')
    after = fingerprint(protected[:2]) | {str(p): digest(p.read_bytes()) for p in protected[2:]}
    write_json(output / 'inputs-after.json', after)
    if before != after:
        raise ValueError('documentation changed protected source/tests/fixtures/evidence')
    write_json(output / 'summary.json', dict(projects=reports, inputs_unchanged=True,
        proposals_sha256=digest(PROPOSALS.read_bytes()),
        provenance='Coding LLM authored summaries; mock replay; observed type claims derived from training outcomes; no paid calls'))


if __name__ == '__main__':
    main()
