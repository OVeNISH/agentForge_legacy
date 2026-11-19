"""CP6: replay frozen cases on unchanged source and recompute baseline evidence."""

import argparse
from collections import Counter
import json
from pathlib import Path
import tarfile
import tempfile

from modernize.characterize import comparable, digest, replay, verify_seal, write_json
from modernize.config import Config
from modernize.sandbox import SandboxRunner, snapshot
from modernize.sandbox_codec import unpack_input
from verify_cp5 import verify

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / 'docs/evidence/cp5.tar.gz'


def failure_category(expected, actual):
    if expected == actual:
        return None
    outcome = actual['outcome']
    if outcome != expected['outcome']:
        if outcome['status'] == 'exception':
            name = outcome['name']
            if name in ('SyntaxError', 'IndentationError', 'TabError'):
                return 'syntax_error'
            if name in ('ImportError', 'ModuleNotFoundError'):
                return 'import_error'
            return 'runtime_exception:' + name
        return 'outcome_mismatch'
    return next(key + '_mismatch' for key in expected if expected[key] != actual[key])


def summarize(fixtures, results):
    expected = {f['case']['id']: f['expected'] for f in fixtures}
    ids = [r['id'] for r in results]
    if len(ids) != len(set(ids)) or set(ids) != set(expected):
        raise ValueError('baseline must contain every eligible fixture exactly once')
    categories = Counter()
    passed = 0
    for result in results:
        actual = comparable(result['record'])
        if result['actual'] != actual or result['passed'] != (actual == expected[result['id']]):
            raise ValueError('baseline comparison disagrees with raw observation')
        category = failure_category(expected[result['id']], actual)
        if category is None:
            passed += 1
        else:
            categories[category] += 1
    return dict(tests=len(results), passed=passed, pass_rate_percent=100 * passed / len(results),
                failures_by_cause=dict(sorted(categories.items())))


def evaluate(directory, oracle, *, execute=False):
    """Only execute=True launches containers; verification uses retained raw records."""
    verified = verify(oracle)
    images = {r['image']: r['record']['image_id'] for r in
              json.loads((ROOT / 'docs/evidence/cp3.json').read_text())['records']}
    runner = SandboxRunner(Config().modern_image) if execute else None
    summary = dict(cp5_archive_sha256=digest(ORACLE.read_bytes()), projects=[])
    for project in verified['projects']:
        name = project['project']
        store = oracle / name
        before = verify_seal(store)
        fixtures = [f for folder in ('training', 'sealed') for f in
                    json.loads((store / folder / (name + '.json')).read_text())]
        report = json.loads((store / 'private' / (name + '-report.json')).read_text())
        hashes = {p: digest(raw) for p, raw in snapshot(ROOT / 'corpus' / name).items()}
        if hashes != report['source_sha256']:
            raise ValueError('corpus differs from characterized source')
        runs = {r['label']: r['record'] for r in map(json.loads,
                (store / 'private/runs.jsonl').read_text().splitlines())}
        path = directory / (name + '.json')
        legacy = []
        for fixture in fixtures:
            case_id = fixture['case']['id']
            # Reuse the first independent CP5 replay, never the expectation-producing run.
            record = runs[name + ':' + case_id + ':1']
            actual = comparable(record)
            legacy.append(dict(id=case_id, actual=actual, record=record,
                               passed=actual == fixture['expected']))
        if execute:
            modern = replay(runner, ROOT / 'corpus' / name, fixtures)
            write_json(path, dict(legacy=legacy, modern=modern))
        recorded = json.loads(path.read_text())
        if recorded['legacy'] != legacy:
            raise ValueError('legacy baseline must match independent CP5 replay')
        cases = {f['case']['id']: f['case'] for f in fixtures}
        for runtime, results in recorded.items():
            if runtime not in ('legacy', 'modern'):
                raise ValueError('unknown baseline runtime')
            for result in results:
                record = result['record']
                if unpack_input(record['request']['args']) != ('observe', cases[result['id']]):
                    raise ValueError('recorded request differs from frozen input')
                if any(record['source_sha256'].get(p) != h for p, h in hashes.items()):
                    raise ValueError('execution used modified source')
                assert record['isolation']['NetworkMode'] == 'none'
                assert record['isolation']['ReadonlyRootfs']
                assert record['container_removed'] and not record['container_state']['Running']
                image = Config().legacy_image if runtime == 'legacy' else Config().modern_image
                assert record['image_id'] == images[image]
        item = dict(project=name, source_sha256=hashes,
                    legacy=summarize(fixtures, recorded['legacy']),
                    modern=summarize(fixtures, recorded['modern']),
                    quarantined=report['quarantined'], heldout=report['heldout'])
        summary['projects'].append(item)
        if verify_seal(store) != before or hashes != {
                p: digest(raw) for p, raw in snapshot(ROOT / 'corpus' / name).items()}:
            raise ValueError('source or fixtures changed during baseline')
        if execute:
            print(json.dumps(item), flush=True)
    if execute:
        write_json(directory / 'summary.json', summary)
    elif summary != json.loads((directory / 'summary.json').read_text()):
        raise ValueError('baseline summary disagrees with raw records')
    return summary


def verify_archive(path):
    with tempfile.TemporaryDirectory() as baseline, tempfile.TemporaryDirectory() as oracle:
        with tarfile.open(path) as archive:
            archive.extractall(baseline, filter='data')
        with tarfile.open(ORACLE) as archive:
            archive.extractall(oracle, filter='data')
        return evaluate(Path(baseline), Path(oracle))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify_archive(args.verify), sort_keys=True, indent=2))
        return
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory() as oracle:
        with tarfile.open(ORACLE) as archive:
            archive.extractall(oracle, filter='data')
        evaluate(args.output, Path(oracle), execute=True)


if __name__ == '__main__':
    main()
