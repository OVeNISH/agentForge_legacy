"""CP5 evidence run: coding-LLM input proposals replayed by the mock boundary."""

import argparse
from decimal import Decimal
import json
from pathlib import Path
import tempfile

from modernize.characterize import Characterizer, digest, replay, seal, verify_seal, write_json
from modernize.config import Config
from modernize.llm import LLMResponse, MockLLMClient, TokenUsage
from modernize.llm_run import LLMRun, RateCard
from modernize.sandbox import SandboxRunner, snapshot

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / 'tests/fixtures/cp5/input_proposals.json'
MUTATIONS = (
    ('golden_ledger', 'main.py', 'amount / people', 'amount * people', 'division'),
    ('golden_ledger', 'main.py', 'total += amount', 'total -= amount', 'accumulation'),
    ('golden_ledger', 'main.py', "return int(text)", "return int(text) + 1", 'parse'),
    ('text_pipeline', 'main.py', 'filter(None, stripped)', 'stripped', 'filter'),
    ('text_pipeline', 'main.py', 'return len(pairs), pairs', 'return 0, pairs', 'zip_length'),
    ('ranking', 'main.py', 'cmp(right[1], left[1])', 'cmp(left[1], right[1])', 'sort_order'),
    ('file_report', 'reportkit/summary.py', 'sum(numbers) / len(numbers)', 'sum(numbers)', 'mean'),
    # Intentionally test the blind spot: unstable clock-dependent outcomes are quarantined.
    ('file_report', 'reportkit/__init__.py', 'time.time()', 'time.time() + 1000000', 'clock_blind_spot'),
)


class RecordedProposalClient(MockLLMClient):
    def complete(self, prompt, **kwargs):
        self.calls.append(prompt)
        context = json.loads(prompt.split('Context JSON:\n', 1)[1])
        function = context['function']
        key = context['project'] + '/' + function['path'] + '::' + function['target']
        rounds = json.loads(SEEDS.read_text())[key]
        cases = rounds[min(context['round'], len(rounds) - 1)]
        return LLMResponse(json.dumps(dict(cases=cases)), self.model, TokenUsage())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    runner = SandboxRunner(Config().legacy_image)
    reports = []
    write_json(output / 'plan.json', dict(line_target=90, explicit_branch_target=90,
        repeats=3, max_rounds=2, minimum_mutation_detection_percent=80,
        proposal_provenance='Coding LLM authored input-only proposals, deterministic mock replay; no provider calls',
        proposal_sha256=digest(SEEDS.read_bytes())))
    for project in json.loads((ROOT / 'corpus/manifest.json').read_text())['projects']:
        name = project['id']
        characterizer = Characterizer(runner, None, output / name)
        client = RecordedProposalClient()
        rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0),
                         'mock usage only; not provider billing', '2026-11-19')
        characterizer.llm = LLMRun(client, characterizer.output / 'private/llm', rates)
        report = characterizer.generate(ROOT / 'corpus' / name, name)
        seal(characterizer.output)
        reports.append(report)
        print(json.dumps(dict(project=name, accepted=report['accepted'],
            heldout=report['heldout'], quarantined=report['quarantined'],
            coverage={k: v['percent'] for k, v in report['coverage'].items()})), flush=True)
    mutations = []
    for project, path, before, after, name in MUTATIONS:
        store = output / project
        verify_seal(store)
        # Mutations see training cases only, never the sealed subset.
        fixtures = json.loads((store / 'training' / (project + '.json')).read_text())
        with tempfile.TemporaryDirectory() as directory:
            mutated = Path(directory)
            for relative, raw in snapshot(ROOT / 'corpus' / project).items():
                target = mutated / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            target = mutated / path
            original = target.read_text()
            if original.count(before) != 1:
                raise ValueError('mutation must identify exactly one site: ' + name)
            target.write_text(original.replace(before, after))
            results = replay(runner, mutated, fixtures)
        record = dict(project=project, name=name, file=path, before=before, after=after,
                      detected=any(not r['passed'] for r in results), results=results)
        write_json(output / 'mutations' / (name + '.json'), record)
        mutations.append(dict(project=project, name=name, detected=record['detected'],
                              comparisons=len(results), failures=sum(not r['passed'] for r in results)))
        verify_seal(store)
        print('mutation ' + name + ': ' + ('detected' if record['detected'] else 'survived'), flush=True)
    heldout = []
    for report in reports:
        project = report['project']
        store = output / project
        verify_seal(store)
        fixtures = json.loads((store / 'sealed' / (project + '.json')).read_text())
        results = replay(runner, ROOT / 'corpus' / project, fixtures)
        write_json(output / 'heldout-verification' / (project + '.json'), results)
        heldout.append(dict(project=project, tests=len(results), passed=sum(r['passed'] for r in results)))
        verify_seal(store)
    summary = dict(reports=reports, mutations=mutations, heldout=heldout,
        mutation_detection_percent=100 * sum(m['detected'] for m in mutations) / len(mutations),
        implementation_sha256={p.name: digest(p.read_bytes()) for p in
            [ROOT / 'src/modernize/characterize.py', ROOT / 'src/modernize/characterize_worker.py',
             Path(__file__), SEEDS]})
    write_json(output / 'summary.json', summary)
    if summary['mutation_detection_percent'] < 80 or any(r['uncovered_functions'] for r in reports) or \
            any(h['passed'] != h['tests'] for h in heldout):
        raise SystemExit('CP5 exit criteria failed; inspect retained evidence')
    print(json.dumps(dict(mutation_detection_percent=summary['mutation_detection_percent'],
                         heldout=heldout)), flush=True)


if __name__ == '__main__':
    main()
