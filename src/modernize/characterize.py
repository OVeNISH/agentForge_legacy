"""Bounded input-only proposal, legacy observation, replay and fixture sealing."""

import base64
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from modernize.llm_prompts import CharacterizationInput
from modernize.sandbox import snapshot, validate_result

WORKER = '__cp5__.py'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + '\n')


def read_observation(record):
    if record.get('protocol_error') or record.get('result') is None or not record.get('container_removed'):
        raise ValueError('sandbox infrastructure/protocol failure; no oracle accepted')
    result = record['result']
    validate_result(result)
    if result['status'] != 'completed':
        raise ValueError('observation harness failed: ' + str(result))
    value = result['value']
    if value['type'] == 'str' and 'base64' in value:
        raw = base64.b64decode(value['base64'], validate=True).decode('ascii')
    elif value['type'] in ('str', 'unicode') and 'value' in value:
        raw = value['value']
    else:
        raise ValueError('harness must return serialized observation')
    observed = json.loads(raw)
    if not isinstance(observed, dict):
        raise ValueError('invalid observation')
    return observed


def comparable(record):
    observed = read_observation(record)
    outcome = observed['outcome']
    if outcome.get('status') not in ('completed', 'exception'):
        raise ValueError('invalid oracle outcome')
    # Traceback locations are diagnostics, not API behaviour; exception type,
    # args and message remain exact, as do every stream byte and captured file.
    return dict(outcome=outcome, **{key: record['result'][key] for key in
                ('stdout_base64', 'stderr_base64', 'files', 'target_exit_code')})


def coverage(inventory, observations):
    result = {}
    for kind in ('lines', 'branches'):
        possible = set(inventory[kind])
        covered = set().union(*(set(o[kind]) for o in observations)) & possible
        result[kind] = dict(covered=sorted(covered), possible=sorted(possible),
                            missing=sorted(possible - covered),
                            percent=100 * len(covered) / len(possible) if possible else 100.0)
    return result


def seal(root):
    paths = sorted(path for directory in ('training', 'sealed', 'private')
                   for path in (root / directory).rglob('*') if path.is_file())
    manifest = {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in paths}
    write_json(root / 'seal.json', manifest)
    for path in paths:
        path.chmod(0o400)
    return manifest


def verify_seal(root):
    root = Path(root)
    manifest = json.loads((root / 'seal.json').read_text())
    actual = {p.relative_to(root).as_posix(): digest(p.read_bytes())
              for directory in ('training', 'sealed', 'private')
              for p in (root / directory).rglob('*') if p.is_file()}
    if manifest != actual:
        raise ValueError('fixture/evidence checksum mismatch')
    return manifest


def export_training(root, destination):
    """The only repair-stage fixture export: no held-out/proposal/oracle logs."""
    root, destination = Path(root).resolve(), Path(destination).resolve()
    verify_seal(root)
    if destination == root or root in destination.parents:
        raise ValueError('repair view must be outside the sealed artifact store')
    shutil.copytree(root / 'training', destination)
    return destination


class Characterizer:
    def __init__(self, runner, llm, output, *, repeats=3, max_rounds=2,
                 line_target=90, branch_target=90, heldout_exclude_ids=()):
        if type(repeats) is not int or not 3 <= repeats <= 5 or \
                type(max_rounds) is not int or not 1 <= max_rounds <= 3:
            raise ValueError('require 3..5 observations and 1..3 proposal rounds')
        if any(type(x) not in (int, float) or not 0 < x <= 100 for x in (line_target, branch_target)):
            raise ValueError('coverage targets must be positive percentages <=100')
        self.runner, self.llm, self.output = runner, llm, Path(output)
        self.repeats, self.max_rounds = repeats, max_rounds
        self.targets = dict(lines=line_target, branches=branch_target)
        self.heldout_exclude_ids = frozenset(heldout_exclude_ids)
        self.output.mkdir(parents=True, exist_ok=False)
        (self.output / 'private').mkdir(mode=0o700)
        self.records = self.output / 'private/runs.jsonl'

    def _execute(self, project, operation, value, label):
        record = self.runner.run(project, WORKER, 'run', args=(operation, value))
        with self.records.open('a') as stream:
            stream.write(json.dumps(dict(label=label, record=record), sort_keys=True) + '\n')
        # Fail closed on harness/protocol failure rather than quarantining it.
        read_observation(record)
        return record

    def generate(self, project, project_id):
        files = snapshot(project)
        if WORKER in files:
            raise ValueError('reserved characterization harness path exists')
        source_hashes = {p: digest(raw) for p, raw in files.items()}
        with tempfile.TemporaryDirectory() as directory:
            staged = Path(directory)
            for path, raw in files.items():
                target = staged / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            (staged / WORKER).write_bytes(Path(__file__).with_name('characterize_worker.py').read_bytes())
            inventory = read_observation(self._execute(staged, 'inventory',
                [p for p in files if p.endswith('.py')], project_id + ':inventory'))
            cases, observations, quarantine, rounds = [], [], [], []
            seen = set()
            for round_number in range(self.max_rounds):
                before = coverage(inventory, observations)
                if round_number and all(before[k]['percent'] >= v for k, v in self.targets.items()):
                    break
                added = 0
                for function in inventory['functions']:
                    context = dict(project=project_id, function=function, round=round_number,
                        source={p: raw.decode('utf-8') for p, raw in files.items() if p.endswith('.py')},
                        uncovered={k: before[k]['missing'] for k in self.targets},
                        policy='Fresh sandbox; scratch file assets; unsupported services flagged. No expected outcomes.')
                    proposed = self.llm.generate('characterization_inputs.v1', context)
                    for proposal in proposed.cases:
                        validated = CharacterizationInput.model_validate(proposal.model_dump(), strict=True)
                        case = dict(path=function['path'], target=function['target'], **validated.model_dump())
                        identity = {k: v for k, v in case.items() if k not in ('category', 'reason')}
                        case_id = digest(json.dumps(identity, sort_keys=True).encode())[:20]
                        if case_id in seen:
                            continue
                        seen.add(case_id)
                        case['id'] = case_id
                        runs = [self._execute(staged, 'observe', case,
                                '%s:%s:%s' % (project_id, case_id, repeat)) for repeat in range(self.repeats)]
                        outcomes = [comparable(run) for run in runs]
                        if any(value != outcomes[0] for value in outcomes[1:]):
                            quarantine.append(dict(case=case, reason='nonidentical repeated legacy observations',
                                                   run_labels=['%s:%s:%s' % (project_id, case_id, r)
                                                               for r in range(self.repeats)]))
                            continue
                        cases.append(dict(case=case, expected=outcomes[0], observations=self.repeats,
                                          replay_passes=self.repeats - 1))
                        observations.extend(read_observation(run) for run in runs)
                        added += 1
                rounds.append(dict(round=round_number, added=added, coverage=coverage(inventory, observations)))
        if source_hashes != {p: digest(raw) for p, raw in snapshot(project).items()}:
            raise ValueError('original source changed during characterization')
        # Split after generation: feedback never distinguishes future held-out cases.
        heldout_ids = set()
        for function in inventory['functions']:
            candidates = [c for c in cases if all(c['case'][k] == function[k] for k in ('path', 'target'))]
            fresh = [c for c in candidates if c['case']['id'] not in self.heldout_exclude_ids]
            if self.heldout_exclude_ids and not fresh:
                raise ValueError('no fresh held-out candidate for ' + function['target'])
            if len(candidates) >= 2 and fresh:
                heldout_ids.add(min(fresh, key=lambda c: c['case']['id'])['case']['id'])
        training = [c for c in cases if c['case']['id'] not in heldout_ids]
        heldout = [c for c in cases if c['case']['id'] in heldout_ids]
        write_json(self.output / 'training' / (project_id + '.json'), training)
        write_json(self.output / 'sealed' / (project_id + '.json'), heldout)
        write_json(self.output / 'private' / (project_id + '-quarantine.json'), quarantine)
        result = dict(project=project_id, source_sha256=source_hashes, inventory=inventory,
            coverage=coverage(inventory, observations), targets=self.targets, rounds=rounds,
            repeats=self.repeats, accepted=len(cases), training=len(training), heldout=len(heldout),
            quarantined=len(quarantine), replay_comparisons=sum(c['replay_passes'] for c in cases),
            replay_passes=sum(c['replay_passes'] for c in cases),
            outcome_counts={kind: sum(c['expected']['outcome']['status'] == kind for c in cases)
                            for kind in ('completed', 'exception')},
            uncovered_functions=[f for f in inventory['functions'] if not any(
                c['case']['path'] == f['path'] and c['case']['target'] == f['target'] for c in cases)])
        write_json(self.output / 'private' / (project_id + '-report.json'), result)
        return result


def replay(runner, project, fixtures):
    """Replay immutable expectations on supplied source; never derive new ones."""
    with tempfile.TemporaryDirectory() as directory:
        staged = Path(directory)
        for path, raw in snapshot(project).items():
            target = staged / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        (staged / WORKER).write_bytes(Path(__file__).with_name('characterize_worker.py').read_bytes())
        results = []
        for fixture in fixtures:
            record = runner.run(staged, WORKER, 'run', args=('observe', fixture['case']))
            actual = comparable(record)
            results.append(dict(id=fixture['case']['id'], passed=actual == fixture['expected'],
                                actual=actual, record=record))
        return results
