"""CP9: bounded training repairs, final held-out evaluation and evidence verification."""

import argparse
from collections import Counter
from datetime import datetime
from decimal import Decimal
import json
from pathlib import Path
import tarfile
import tempfile

from modernize.characterize import digest, export_training, read_observation, verify_seal, write_json
from modernize.config import Config
from modernize.documentation import fingerprint
from modernize.llm import LLMResponse, MockLLMClient, TokenUsage
from modernize.llm_run import LLMRun, RateCard, recompute_usage
from modernize.repair import REPLAY_WORKER, failure_context, metrics, repair, replay, review_changes
from modernize.sandbox import SandboxRunner, snapshot
from modernize.sandbox_codec import unpack_input
from modernize.transformation import SourceChanges, apply_changes, save_diffs

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/evidence'


class RecordedRepairClient(MockLLMClient):
    """Coding-LLM assessment replay; no fabricated patch or runtime-type impersonation."""
    def complete(self, prompt, **kwargs):
        self.calls.append(prompt)
        response = dict(patches=[], needs_human_review=[
            'Frozen CP5 observations distinguish Python 2 str/unicode, exception modules and '
            'argument types from Python 3 bytes/str/builtins. Source-only changes cannot '
            'reproduce those built-in runtime identities. No safe patch is proposed; '
            'comparisons and fixtures stay unchanged. Review remaining semantic differences too.'])
        return LLMResponse(json.dumps(response), self.model, TokenUsage())


def extract(number, destination):
    with tarfile.open(EVIDENCE / ('cp%s.tar.gz' % number)) as archive:
        archive.extractall(destination, filter='data')


def hashes(files):
    return {p: digest(raw) for p, raw in files.items()}


def execute(output):
    if any(output == p or p in output.parents for p in
           (ROOT / 'tests', ROOT / 'corpus', EVIDENCE, ROOT / 'src', ROOT / 'scripts')):
        raise ValueError('repair output cannot overwrite protected inputs')
    output.mkdir(parents=True, exist_ok=False)
    archives = [EVIDENCE / ('cp%s.tar.gz' % n) for n in (5, 6, 7, 8)]
    def protected():
        return fingerprint([ROOT / 'tests', ROOT / 'corpus']) | {str(p): digest(p.read_bytes()) for p in archives}
    before = protected()
    write_json(output / 'inputs-before.json', before)
    runner = SandboxRunner(Config().modern_image)
    reports = []
    try:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for n in (5, 7, 8):
                extract(n, root / str(n))
            facts = json.loads((EVIDENCE / 'cp2.json').read_text())['facts']
            projects = json.loads((ROOT / 'corpus/manifest.json').read_text())['projects']
            # All repair stages finish before the controller opens any held-out case.
            for project in projects:
                name = project['id']
                exported = export_training(root / '5' / name, root / 'exports' / name)
                fixtures = json.loads((exported / (name + '.json')).read_text())
                client = RecordedRepairClient()
                rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0),
                                 'mock only; no provider billing', '2026-11-19')
                llm = LLMRun(client, output / name / 'llm', rates)
                report = repair(root / '8' / name / 'source', name,
                    dict(files=[f for f in facts['files'] if f['path'].startswith(name + '/')]),
                    fixtures, llm, runner, output / name / 'repair')
                source = snapshot(output / name / 'repair/source')
                original = snapshot(root / '7' / name / 'source')
                review = review_changes(snapshot(root / '8' / name / 'mechanical'), source)
                review['full_diff_files'] = save_diffs(original, source, output / name / 'full-diffs')
                review['scope'] = 'Mechanical-to-final AST scan plus full incoming-CP7-to-final diffs; see cp9-review.json for coding-agent review.'
                write_json(output / name / 'full-review.json', review)
                write_json(output / name / 'final-source-lock.json', hashes(source))
                reports.append(report)
                print(json.dumps(dict(project=name, training=report['final'],
                    attempts=len(report['attempts']), status=report['status'])), flush=True)
            for report in reports:
                name = report['project']
                store = root / '5' / name
                seal = verify_seal(store)
                heldout = json.loads((store / 'sealed' / (name + '.json')).read_text())
                source = snapshot(output / name / 'repair/source')
                results = replay(runner, source, heldout)
                write_json(output / name / 'heldout.json', results)
                if verify_seal(store) != seal or hashes(snapshot(output / name / 'repair/source')) != report['final_sha256']:
                    raise ValueError('sealed fixtures or final source changed during held-out evaluation')
                report['heldout'] = metrics(heldout, results)
                report['usage'] = recompute_usage(output / name / 'llm')
                if report['heldout']['unresolved']:
                    report['status'] = 'needs_human_review'
                print(json.dumps(dict(project=name, heldout=report['heldout'])), flush=True)
    finally:
        after = protected()
        write_json(output / 'inputs-after.json', after)
        if before != after:
            raise ValueError('repair changed protected tests/fixtures/source/evidence')
    summary = dict(projects=reports, inputs_unchanged=True,
        inputs={p.name: digest(p.read_bytes()) for p in archives},
        heldout_policy='All repairs finished and final source locked before opening held-out cases; no subsequent repairs.',
        provenance='Coding LLM authored no-patch assessments replayed via deterministic mock; no paid provider calls.')
    write_json(output / 'summary.json', summary)
    return summary


def verify(directory):
    """Recompute CP9 comparisons and loop decisions from frozen fixtures and raw runs."""
    summary = json.loads((directory / 'summary.json').read_text())
    before = json.loads((directory / 'inputs-before.json').read_text())
    if before != json.loads((directory / 'inputs-after.json').read_text()) or not summary['inputs_unchanged']:
        raise ValueError('protected input checksum proof failed')
    if not any('/tests/fixtures/' in p for p in before) or not any('/corpus/' in p for p in before):
        raise ValueError('checksum proof omits frozen inputs')
    for n in (5, 6, 7, 8):
        archive = EVIDENCE / ('cp%s.tar.gz' % n)
        if summary['inputs'][archive.name] != digest(archive.read_bytes()):
            raise ValueError('input evidence archive changed')
    image = next(r['record']['image_id'] for r in json.loads((EVIDENCE / 'cp3.json').read_text())['records']
                 if r['image'] == Config().modern_image)
    last_repair = max(datetime.fromisoformat(json.loads(line)['timestamp'])
        for item in summary['projects'] for line in
        (directory / item['project'] / 'llm/calls.jsonl').read_text().splitlines())
    with tempfile.TemporaryDirectory() as directory_name:
        root = Path(directory_name)
        for n in (5, 7, 8):
            extract(n, root / str(n))
        if [r['project'] for r in summary['projects']] != [p['id'] for p in
                json.loads((ROOT / 'corpus/manifest.json').read_text())['projects']]:
            raise ValueError('missing corpus project')
        for item in summary['projects']:
            name = item['project']
            store = directory / name
            project = store / 'repair'
            oracle = root / '5' / name
            verify_seal(oracle)
            fixtures = json.loads((oracle / 'training' / (name + '.json')).read_text())
            heldout = json.loads((oracle / 'sealed' / (name + '.json')).read_text())
            original = snapshot(root / '8' / name / 'source')
            current = original
            def checked(path, cases, source):
                records = json.loads(path.read_text())
                value = metrics(cases, records)
                inputs = {f['case']['id']: f['case'] for f in cases}
                source_hashes = dict(hashes(source), **{
                    '__cp5__.py': digest((ROOT / 'src/modernize/characterize_worker.py').read_bytes()),
                    REPLAY_WORKER: digest((ROOT / 'src/modernize/repair_worker.py').read_bytes())})
                for result in records:
                    record = result['record']
                    if record['source_sha256'] != source_hashes or record['image_id'] != image or \
                            unpack_input(record['request']['args']) != (inputs[result['id']],) or \
                            record['request']['script'] != REPLAY_WORKER or record['request']['function'] != 'run':
                        raise ValueError('replay source/image/request differs from frozen case')
                    if record['isolation']['NetworkMode'] != 'none' or not record['isolation']['ReadonlyRootfs'] or \
                            not record['container_removed'] or record['container_state']['Running']:
                        raise ValueError('invalid sandbox isolation/cleanup')
                    diagnostic = read_observation(record)['traceback']
                    if not isinstance(diagnostic, list) or (result['actual']['outcome']['status'] == 'exception' and not diagnostic):
                        raise ValueError('missing exception diagnostic traceback')
                return records, value
            initial_results, initial = checked(project / 'training-initial.json', fixtures, current)
            results = initial_results
            attempts = json.loads((project / 'attempts.json').read_text())
            report = json.loads((project / 'report.json').read_text())
            if type(report['max_attempts_per_function']) is not int or not 1 <= report['max_attempts_per_function'] <= 3:
                raise ValueError('invalid repair cap')
            counts = Counter()
            calls = [json.loads(line) for line in (store / 'llm/calls.jsonl').read_text().splitlines()]
            # The corpus demonstration has schema-valid no-patch responses, one per bounded attempt.
            if len(calls) != len(attempts):
                raise ValueError('repair attempt/call log count differs')
            for index, (attempt, call) in enumerate(zip(attempts, calls)):
                key = tuple(attempt['function'])
                counts[key] += 1
                if attempt['index'] != index or attempt['function_attempt'] != counts[key] or \
                        counts[key] > report['max_attempts_per_function']:
                    raise ValueError('repair cap or attempt order violated')
                context = json.loads(call['prompt'].split('Context JSON:\n', 1)[1])
                expected_context = dict(project=name, function=list(key), function_attempt=counts[key],
                    source={p: raw.decode('utf-8') for p, raw in current.items() if p.endswith('.py')},
                    source_sha256={p: digest(raw) for p, raw in current.items() if p.endswith('.py')},
                    failures=failure_context(fixtures, results, key),
                    previous_error=next((a.get('error') for a in reversed(attempts[:index]) if a['function'] == list(key)), None))
                if context != expected_context:
                    raise ValueError('repair context differs from training-only failures')
                if any(f['case']['id'] in call['prompt'] for f in heldout):
                    raise ValueError('held-out case leaked into repair prompt')
                if call['prompt_version'] != 'repair.v1' or call['validation']['status'] != 'passed' or call['evidence_kind'] != 'mock':
                    raise ValueError('invalid corpus mock provenance/schema validation')
                changes = SourceChanges.model_validate_json((project / ('changes-%s.json' % index)).read_text(), strict=True)
                if changes != SourceChanges.model_validate_json(call['response'], strict=True):
                    raise ValueError('patch differs from logged response')
                candidate = apply_changes(current, changes)
                if attempt['accepted']:
                    tested, _ = checked(project / ('training-%s.json' % index), fixtures, candidate)
                    if not {r['id'] for r in results if r['passed']} < {r['id'] for r in tested if r['passed']}:
                        raise ValueError('accepted repair regressed or failed to improve')
                    current, results = candidate, tested
                elif changes.patches or attempt['error'] != 'no source patch proposed; needs human review':
                    raise ValueError('unexpected corpus rejection; inspect its validation records')
            final_results, final = checked(project / 'training-final.json', fixtures, current)
            if final_results != results or current != snapshot(project / 'source'):
                raise ValueError('final source or results differ from accepted candidates')
            counts = {p + '::' + target: count for (p, target), count in sorted(counts.items())}
            unresolved = set(final['unresolved'])
            if any(counts.get(f['case']['path'] + '::' + f['case']['target']) != report['max_attempts_per_function']
                   for f in fixtures if f['case']['id'] in unresolved):
                raise ValueError('repair stopped before its per-function cap')
            if any(report[k] != value for k, value in dict(initial=initial, final=final, retry_counts=counts,
                    attempts=attempts, incoming_sha256=hashes(original), final_sha256=hashes(current),
                    training_fixture_sha256=digest(json.dumps(fixtures, sort_keys=True).encode()),
                    review=review_changes(original, current)).items()):
                raise ValueError('repair report disagrees with raw run records')
            if any(item[k] != report[k] for k in report if k != 'status'):
                raise ValueError('summary differs from repair report')
            if json.loads((store / 'final-source-lock.json').read_text()) != hashes(current):
                raise ValueError('final source lock differs')
            _, heldout_metrics = checked(store / 'heldout.json', heldout, current)
            if any(datetime.fromisoformat(r['record']['container_state']['StartedAt'].replace('Z', '+00:00')) <= last_repair
                   for r in json.loads((store / 'heldout.json').read_text())):
                raise ValueError('held-out execution must follow all repair calls')
            if item['heldout'] != heldout_metrics or item['usage'] != recompute_usage(store / 'llm'):
                raise ValueError('held-out/usage summary disagrees with raw records')
            if (final['unresolved'] or heldout_metrics['unresolved']) and item['status'] != 'needs_human_review':
                raise ValueError('unresolved failures must be escalated')
            review = json.loads((store / 'full-review.json').read_text())
            automatic = review_changes(snapshot(root / '8' / name / 'mechanical'), current)
            if any(review[k] != automatic[k] for k in automatic):
                raise ValueError('anti-gaming scan differs from sources')
            diffs = root / 'diffs' / name
            changed = save_diffs(snapshot(root / '7' / name / 'source'), current, diffs)
            if changed != review['full_diff_files'] or snapshot(diffs) != snapshot(store / 'full-diffs'):
                raise ValueError('saved full diff differs from final source')
    return summary


def verify_archive(path):
    with tempfile.TemporaryDirectory() as directory:
        with tarfile.open(path) as archive:
            archive.extractall(directory, filter='data')
        return verify(Path(directory))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    summary = verify_archive(args.verify) if args.verify else execute(args.output.resolve())
    print(json.dumps([dict(project=p['project'], training=p['final'], heldout=p['heldout'],
                           retry_counts=p['retry_counts'], status=p['status']) for p in summary['projects']], indent=2))


if __name__ == '__main__':
    main()
