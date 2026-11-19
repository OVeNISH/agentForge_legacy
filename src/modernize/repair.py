"""Training-only, bounded source repair followed by a separate final evaluation."""

import ast
from collections import Counter
import difflib
from importlib import resources
import json
from pathlib import Path
import tempfile

from modernize.characterize import WORKER, comparable, digest, read_observation, write_json
from modernize.llm_prompts import Prompt, strict_json
from modernize.sandbox import snapshot
from modernize.transformation import (SourceChanges, VALIDATE_WORKER, apply_changes,
    check_public_api, sandbox_call, save_diffs, stage)

REPLAY_WORKER = '__cp9__.py'


def load_repair_prompt():
    directory = resources.files('modernize').joinpath('prompts/repair')
    schema = strict_json(directory.joinpath('repair.v1.schema.json').read_text())
    if schema != SourceChanges.model_json_schema():
        raise ValueError('repair schema differs from response model')
    return Prompt('repair.v1', directory.joinpath('repair.v1.txt').read_text(), schema, SourceChanges)


def replay(runner, files, fixtures):
    if {WORKER, REPLAY_WORKER, VALIDATE_WORKER} & files.keys():
        raise ValueError('reserved repair harness path exists')
    with tempfile.TemporaryDirectory() as directory:
        stage(files, directory)
        for name, module in ((WORKER, 'characterize_worker.py'), (REPLAY_WORKER, 'repair_worker.py')):
            (Path(directory) / name).write_bytes(Path(__file__).with_name(module).read_bytes())
        results = []
        for fixture in fixtures:
            record = runner.run(directory, REPLAY_WORKER, 'run', args=(fixture['case'],))
            actual = comparable(record)
            results.append(dict(id=fixture['case']['id'], actual=actual, record=record,
                                passed=actual == fixture['expected']))
        return results


def metrics(fixtures, results, comparison=None):
    expected = {f['case']['id']: f['expected'] for f in fixtures}
    if len(expected) != len(fixtures) or len(results) != len(expected) or \
            {r['id'] for r in results} != set(expected):
        raise ValueError('evaluation must contain every unique fixture exactly once')
    for result in results:
        actual = comparable(result['record'])
        if actual != result['actual'] or result['passed'] != (actual == expected[result['id']]):
            raise ValueError('comparison disagrees with raw observation')
    passed_ids = {r['id'] for r in results if
                  (comparison(expected[r['id']], r['actual']) if comparison else r['passed'])}
    passed = len(passed_ids)
    return dict(tests=len(results), passed=passed,
                pass_rate_percent=100 * passed / len(results) if results else None,
                unresolved=[r['id'] for r in results if r['id'] not in passed_ids])


def failure_context(fixtures, results, key, comparison=None):
    cases = {f['case']['id']: f for f in fixtures}
    failures = []
    for result in results:
        fixture = cases[result['id']]
        matched = comparison(fixture['expected'], result['actual']) if comparison else result['passed']
        if matched or (fixture['case']['path'], fixture['case']['target']) != key:
            continue
        expected = json.dumps(fixture['expected'], sort_keys=True, indent=2).splitlines(True)
        actual = json.dumps(result['actual'], sort_keys=True, indent=2).splitlines(True)
        failures.append(dict(case=fixture['case'], expected=fixture['expected'], actual=result['actual'],
            diff=''.join(difflib.unified_diff(expected, actual, fromfile='expected', tofile='actual')),
            traceback=read_observation(result['record'])['traceback']))
    return failures


def review_changes(before, after):
    """Conservative flags for human inspection, never a proof of no gaming."""
    findings = []
    for path, raw in sorted(after.items()):
        if not path.endswith('.py') or before.get(path) == raw:
            continue
        old = ast.parse(before.get(path, b''))
        new = ast.parse(raw)
        def count(tree, kind):
            return sum(isinstance(n, kind) for n in ast.walk(tree))
        for kind, rule in ((ast.If, 'changed_branch_count'), (ast.ExceptHandler, 'changed_exception_handler_count')):
            if count(old, kind) != count(new, kind):
                findings.append(dict(path=path, rule=rule))
        for node in ast.walk(new):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [n.name for n in node.names] + [getattr(node, 'module', '') or '']
                if any(any(word in name.split('.') for word in ('tests', 'fixtures', 'sealed', 'private'))
                       for name in names):
                    findings.append(dict(path=path, rule='protected_import', line=node.lineno))
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and any(
                    word in node.value for word in ('args_json', 'expected', 'seal.json', 'fixtures/', 'sealed/')):
                findings.append(dict(path=path, rule='fixture_reference', line=node.lineno))
    return dict(status='needs_human_review' if findings else 'no_automatic_flags', findings=findings,
                limitation='Heuristic only; inspect all saved diffs for fixture branches, swallowed exceptions and changed comparisons.')


def repair(project, project_id, facts, fixtures, llm, runner, output, *, max_attempts=2, comparison=None):
    """Accept only a training export; the caller evaluates sealed cases after return."""
    if type(max_attempts) is not int or not 1 <= max_attempts <= 3:
        raise ValueError('repair cap must be 1..3 attempts per function')
    project, output = Path(project).resolve(), Path(output).resolve()
    if output == project or project in output.parents:
        raise ValueError('repair output must be outside input source')
    output.mkdir(parents=True, exist_ok=False)
    fixtures_hash = digest(json.dumps(fixtures, sort_keys=True).encode())
    initial = snapshot(project)
    current = initial
    initial_hashes = {p: digest(raw) for p, raw in initial.items()}
    results = replay(runner, current, fixtures)
    write_json(output / 'training-initial.json', results)
    initial_metrics = metrics(fixtures, results, comparison)
    cases = {f['case']['id']: f['case'] for f in fixtures}
    counts, attempts, flags = Counter(), [], []
    try:
        while True:
            unresolved = set(metrics(fixtures, results, comparison)['unresolved'])
            keys = sorted({(cases[r['id']]['path'], cases[r['id']]['target'])
                for r in results if r['id'] in unresolved and
                counts[(cases[r['id']]['path'], cases[r['id']]['target'])] < max_attempts})
            if not keys:
                break
            key = keys[0]
            counts[key] += 1
            index = len(attempts)
            attempt = dict(index=index, function=list(key), function_attempt=counts[key], accepted=False)
            context = dict(project=project_id, function=list(key), function_attempt=counts[key],
                source={p: raw.decode('utf-8') for p, raw in current.items() if p.endswith('.py')},
                source_sha256={p: digest(raw) for p, raw in current.items() if p.endswith('.py')},
                failures=failure_context(fixtures, results, key, comparison),
                previous_error=next((a.get('error') for a in reversed(attempts) if a['function'] == list(key)), None))
            try:
                changes = llm.generate(load_repair_prompt(), context)
                write_json(output / ('changes-%s.json' % index), changes.model_dump())
                flags.extend(changes.needs_human_review)
                if not changes.patches:
                    raise ValueError('no source patch proposed; needs human review')
                if any(p.path in (WORKER, REPLAY_WORKER) for p in changes.patches):
                    raise ValueError('repair cannot modify observation harnesses')
                candidate = apply_changes(current, changes)
                validation = sandbox_call(runner, candidate, VALIDATE_WORKER, 'conversion_validate_worker.py',
                    'run', (sorted(p for p in candidate if p.endswith('.py')),), output / ('validation-%s.json' % index))
                if {f['path'] for f in validation['files']} != {p for p in candidate if p.endswith('.py')} or any(
                        not f['compiled'] or not f['imported'] for f in validation['files']):
                    raise ValueError('repair validation is incomplete')
                check_public_api(validation, facts, project_id)
                tested = replay(runner, candidate, fixtures)
                write_json(output / ('training-%s.json' % index), tested)
                metrics(fixtures, tested)
                passed_before = set(cases) - set(metrics(fixtures, results, comparison)['unresolved'])
                passed_after = set(cases) - set(metrics(fixtures, tested, comparison)['unresolved'])
                raw_before = {r['id'] for r in results if r['passed']}
                raw_after = {r['id'] for r in tested if r['passed']}
                if not passed_before < passed_after or not raw_before <= raw_after:
                    raise ValueError('candidate must fix at least one failure without regressing any passing test')
                save_diffs(current, candidate, output / ('diffs-%s' % index))
                current, results = candidate, tested
                attempt['accepted'] = True
                attempt['error'] = None
            except (ValueError, SyntaxError) as error:
                attempt['error'] = str(error)[:2000]
            attempts.append(attempt)
            write_json(output / 'attempts.json', attempts)
    finally:
        if fixtures_hash != digest(json.dumps(fixtures, sort_keys=True).encode()) or initial_hashes != {
                p: digest(raw) for p, raw in snapshot(project).items()}:
            raise ValueError('repair changed frozen fixtures or incoming source')
    with tempfile.TemporaryDirectory(dir=output) as directory:
        pending = Path(directory) / 'source'
        stage(current, pending)
        pending.rename(output / 'source')
    write_json(output / 'training-final.json', results)
    write_json(output / 'attempts.json', attempts)
    changed = save_diffs(initial, current, output / 'diffs')
    review = review_changes(initial, current)
    write_json(output / 'review.json', review)
    final = metrics(fixtures, results, comparison)
    report = dict(project=project_id, initial=initial_metrics, final=final, attempts=attempts,
        retry_counts={p + '::' + target: count for (p, target), count in sorted(counts.items())},
        max_attempts_per_function=max_attempts, changed_files=changed, review=review,
        needs_human_review=sorted(set(flags)),
        status='needs_human_review' if final['unresolved'] or flags or review['findings'] else 'training_passed',
        incoming_sha256=initial_hashes, final_sha256={p: digest(raw) for p, raw in current.items()},
        training_fixture_sha256=fixtures_hash)
    write_json(output / 'report.json', report)
    return report
