"""Recompute CP5 metrics from sealed observations and actual mutation replays."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile

from modernize.characterize import comparable, digest, read_observation, verify_seal
from modernize.llm_prompts import CharacterizationInput, load_prompt
from modernize.llm_run import recompute_usage
from modernize.sandbox import validate_value
from modernize.sandbox_codec import unpack_input

ROOT = Path(__file__).resolve().parents[1]


def verify(directory):
    directory = Path(directory)
    summary = json.loads((directory / 'summary.json').read_text())
    plan = json.loads((directory / 'plan.json').read_text())
    assert plan['minimum_mutation_detection_percent'] == 80
    counts, totals = [], Counter()
    for report in summary['reports']:
        project = report['project']
        store = directory / project
        verify_seal(store)
        fixtures = [item for folder in ('training', 'sealed')
                    for item in json.loads((store / folder / (project + '.json')).read_text())]
        training = json.loads((store / 'training' / (project + '.json')).read_text())
        sealed = json.loads((store / 'sealed' / (project + '.json')).read_text())
        assert {f['case']['id'] for f in training}.isdisjoint(f['case']['id'] for f in sealed)
        quarantine = json.loads((store / 'private' / (project + '-quarantine.json')).read_text())
        records = [json.loads(line) for line in (store / 'private/runs.jsonl').read_text().splitlines()]
        by_label = {r['label']: r['record'] for r in records}
        assert len(by_label) == len(records)
        inventory = read_observation(by_label[project + ':inventory'])
        assert inventory == report['inventory']
        expected_source = report['source_sha256']
        for path, expected in expected_source.items():
            assert digest((ROOT / 'corpus' / project / path).read_bytes()) == expected
        for run in by_label.values():
            read_observation(run)
            assert all(run['source_sha256'][p] == h for p, h in expected_source.items())
            assert run['isolation']['NetworkMode'] == 'none'
            assert run['isolation']['ReadonlyRootfs']
            assert not run['container_state']['Running']
        observations = []
        comparisons = passes = 0
        for fixture in fixtures:
            case = fixture['case']
            CharacterizationInput.model_validate({k:v for k,v in case.items()
                if k not in ('id','path','target')}, strict=True)
            outcomes = []
            for repeat in range(plan['repeats']):
                run = by_label['%s:%s:%s' % (project, case['id'], repeat)]
                request = unpack_input(run['request']['args'])
                assert request[0] == 'observe' and request[1] == case
                observation = read_observation(run)
                outcome = observation['outcome']
                if outcome['status'] == 'completed':
                    validate_value(outcome['value'])
                    if outcome['state'] is not None:
                        validate_value(outcome['state'])
                else:
                    validate_value(outcome['args'])
                observations.append(observation)
                outcomes.append(comparable(run))
            assert fixture['expected'] == outcomes[0]
            comparisons += len(outcomes) - 1
            passes += sum(o == fixture['expected'] for o in outcomes[1:])
            assert all(o == fixture['expected'] for o in outcomes)
        for excluded in quarantine:
            outcomes = [comparable(by_label[label]) for label in excluded['run_labels']]
            assert any(o != outcomes[0] for o in outcomes[1:])
        eligible_ids = {f['case']['id'] for f in fixtures}
        quarantined_ids = {q['case']['id'] for q in quarantine}
        assert eligible_ids.isdisjoint(quarantined_ids)
        observed_labels = {label.split(':')[1] for label in by_label if not label.endswith(':inventory')}
        assert observed_labels == eligible_ids | quarantined_ids
        computed = {}
        for kind in ('lines','branches'):
            possible = set(inventory[kind])
            hit = set().union(*(set(o[kind]) for o in observations)) & possible
            computed[kind] = dict(covered=sorted(hit), possible=sorted(possible),
                missing=sorted(possible-hit), percent=100*len(hit)/len(possible) if possible else 100.0)
        assert computed == report['coverage']
        assert (len(fixtures),len(training),len(sealed),len(quarantine),comparisons,passes) == (
            report['accepted'],report['training'],report['heldout'],report['quarantined'],
            report['replay_comparisons'],report['replay_passes'])
        assert not report['uncovered_functions']
        calls = [json.loads(line) for line in (store/'private/llm/calls.jsonl').read_text().splitlines()]
        for call in calls:
            assert call['evidence_kind'] == 'mock'
            assert call['validation']['status'] == 'passed'
            load_prompt(call['prompt_version']).response_model.model_validate_json(call['response'],strict=True)
        usage = recompute_usage(store/'private/llm')
        assert usage['known_total_tokens'] == 0 and usage['known_estimated_usd'] == '0'
        for key, value in dict(accepted=len(fixtures),training=len(training),heldout=len(sealed),
            quarantined=len(quarantine),comparisons=comparisons,passes=passes,
            oracle_container_runs=len(records),mock_calls=len(calls)).items():
            totals[key] += value
        counts.append(dict(project=project, accepted=len(fixtures), comparisons=comparisons,
            passes=passes, heldout=len(sealed), quarantined=len(quarantine),
            coverage={k:v['percent'] for k,v in computed.items()}))
    detected = 0
    for mutation in summary['mutations']:
        record = json.loads((directory/'mutations'/(mutation['name']+'.json')).read_text())
        project = mutation['project']
        training = json.loads((directory/project/'training'/(project+'.json')).read_text())
        expected = {f['case']['id']:f['expected'] for f in training}
        assert {r['id'] for r in record['results']} == set(expected)
        failures = 0
        original = (ROOT/'corpus'/project/record['file']).read_text()
        mutant_hash = digest(original.replace(record['before'],record['after']).encode())
        for result in record['results']:
            assert result['record']['source_sha256'][record['file']] == mutant_hash
            actual = comparable(result['record'])
            assert actual == result['actual']
            passed = actual == expected[result['id']]
            assert passed == result['passed']
            failures += not passed
        assert failures == mutation['failures']
        assert bool(failures) == mutation['detected'] == record['detected']
        detected += bool(failures)
        totals['mutation_container_runs'] += len(record['results'])
    rate = 100 * detected / len(summary['mutations'])
    assert rate == summary['mutation_detection_percent'] and rate >= 80
    heldout_passes = 0
    for held in summary['heldout']:
        project = held['project']
        fixtures = json.loads((directory/project/'sealed'/(project+'.json')).read_text())
        expected = {f['case']['id']:f['expected'] for f in fixtures}
        results = json.loads((directory/'heldout-verification'/(project+'.json')).read_text())
        assert {r['id'] for r in results} == set(expected)
        passed = sum(comparable(r['record']) == expected[r['id']] for r in results)
        assert passed == held['passed'] == held['tests'] == len(results)
        heldout_passes += passed
        totals['heldout_container_runs'] += len(results)
    return dict(projects=counts, totals=dict(totals), mutations_detected=detected,
                mutations_total=len(summary['mutations']), mutation_detection_percent=rate,
                heldout_passes=heldout_passes)


def verify_archive(path):
    with tempfile.TemporaryDirectory() as directory:
        with tarfile.open(path, 'r:gz') as archive:
            archive.extractall(directory, filter='data')
        return verify(directory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    result = verify(args.evidence) if args.evidence.is_dir() else verify_archive(args.evidence)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
