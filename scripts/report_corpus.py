"""CP10: generate and independently recompute a report from recorded corpus runs."""

import argparse
from collections import Counter
import json
from pathlib import Path
import tempfile

from baseline_corpus import evaluate, failure_category, summarize
from repair_corpus import EVIDENCE, ROOT, extract, verify as verify_repairs
from verify_cp5 import verify as verify_characterization
from modernize.characterize import digest, write_json
from modernize.documentation import DocumentationResponse, cross_check, observed_claims, render
from modernize.llm_run import usage_summary


def read(path):
    return json.loads(path.read_text())


def reference(stage, path):
    return 'cp%s.tar.gz!/%s' % (stage, path)


def build(root):
    """Read only retained evidence; never execute project code or call a provider."""
    for stage in (5, 6, 7, 8, 9):
        extract(stage, root / str(stage))
    characterization = verify_characterization(root / '5')
    baseline = evaluate(root / '6', root / '5')
    repairs = verify_repairs(root / '9')
    plan = read(root / '5/plan.json')
    reports = []
    all_calls = []
    for item in repairs['projects']:
        name = item['project']
        oracle, store = root / '5' / name, root / '9' / name
        training = read(oracle / 'training' / (name + '.json'))
        heldout = read(oracle / 'sealed' / (name + '.json'))
        fixtures = training + heldout
        results = read(store / 'repair/training-final.json') + read(store / 'heldout.json')
        expected = {f['case']['id']: f for f in fixtures}
        cp5 = read(oracle / 'private' / (name + '-report.json'))
        cp6 = next(p for p in baseline['projects'] if p['project'] == name)
        quarantine = read(oracle / 'private' / (name + '-quarantine.json'))
        failures = []
        for result in results:
            if not result['passed']:
                fixture = expected[result['id']]
                split = 'training' if fixture in training else 'heldout'
                path = 'repair/training-final.json' if split == 'training' else 'heldout.json'
                failures.append(dict(id=result['id'], split=split, case=fixture['case'],
                    category=failure_category(fixture['expected'], result['actual']),
                    expected=fixture['expected'], actual=result['actual'],
                    run=reference(9, name + '/' + path) + '#' + result['id']))
        usage = {}
        for stage, path in ((5, 'private/llm'), (7, 'llm'), (8, 'llm'), (9, 'llm')):
            log = root / str(stage) / name / path / 'calls.jsonl'
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            usage['cp%s' % stage] = dict(**usage_summary(calls),
                evidence_kinds=dict(Counter(c['evidence_kind'] for c in calls)),
                record=reference(stage, name + '/' + path + '/calls.jsonl'))
            all_calls.extend(calls)
        docs = read(root / '7' / name / 'documentation.json')
        mismatches = []
        for entry in docs['entries']:
            response = DocumentationResponse.model_validate(entry['response'], strict=True)
            if entry['text'] != render(response):
                raise ValueError('documentation text differs from validated response')
            if entry['kind'] == 'function':
                path, target = entry['key'][len(name) + 1:].split('::')
                observed = observed_claims(training, path, target)
                differences = cross_check(response, observed)
                if observed != entry['observed'] or differences != entry['cross_check']:
                    raise ValueError('documentation claim check differs from observations')
                if differences:
                    mismatches.append(dict(key=entry['key'], differences=differences))
        # Preserve source-grounded suspicions as suspicions, never as proven failures.
        suspected = [dict(key=e['key'], text=e['response']['summary'],
                          record=reference(7, name + '/documentation.json'))
                     for e in docs['entries'] if 'suspected legacy bug:' in e['response']['summary'].lower()]
        diffs = {p.relative_to(store / 'full-diffs').as_posix(): p.read_text()
                 for p in sorted((store / 'full-diffs').rglob('*.diff'))}
        reports.append(dict(project=name, status=item['status'],
            rates=dict(legacy_on_legacy=cp6['legacy'], legacy_on_modern=cp6['modern'],
                       converted_on_modern=summarize(fixtures, results)),
            training=item['final'], heldout=item['heldout'],
            coverage=cp5['coverage'], coverage_targets=cp5['targets'],
            quarantine=quarantine, inventory_exclusions=cp5['inventory']['exclusions'],
            repair=dict(attempts=item['attempts'], retry_counts=item['retry_counts'],
                        max_attempts_per_function=item['max_attempts_per_function']),
            usage=usage, diffs=diffs, documentation=docs, documentation_mismatches=mismatches,
            suspected_legacy_bugs=suspected, unresolved=failures,
            review=dict(automatic=read(store / 'full-review.json'),
                        manual=next(p for p in read(root / '9/cp9-review.json')['projects'] if p['project'] == name)),
            review_flags=item['needs_human_review'],
            records=dict(baseline=reference(6, name + '.json'),
                coverage=reference(5, name + '/private/' + name + '-report.json'),
                quarantine=reference(5, name + '/private/' + name + '-quarantine.json'),
                training=reference(9, name + '/repair/training-final.json'),
                heldout=reference(9, name + '/heldout.json'),
                repairs=reference(9, name + '/repair/attempts.json'),
                diffs=reference(9, name + '/full-diffs/'),
                documentation=reference(7, name + '/documentation.json'))))
    totals = {}
    for runtime in reports[0]['rates']:
        tests = sum(p['rates'][runtime]['tests'] for p in reports)
        passed = sum(p['rates'][runtime]['passed'] for p in reports)
        totals[runtime] = dict(tests=tests, passed=passed, pass_rate_percent=100 * passed / tests)
    totals.update(quarantined=sum(len(p['quarantine']) for p in reports),
        heldout_tests=sum(p['heldout']['tests'] for p in reports),
        heldout_passed=sum(p['heldout']['passed'] for p in reports),
        repair_proposals=sum(len(p['repair']['attempts']) for p in reports),
        accepted_repairs=sum(a['accepted'] for p in reports for a in p['repair']['attempts']),
        changed_files=sum(len(p['diffs']) for p in reports),
        usage=dict(**usage_summary(all_calls), evidence_kinds=dict(Counter(c['evidence_kind'] for c in all_calls))))
    return dict(schema_version='cp10.v1',
        status='needs_human_review' if any(p['status'] == 'needs_human_review' for p in reports) else 'passed',
        scope='Committed successful corpus runs only: characterization, documentation, transformation and repair. '
              'Excludes infrastructure checks, failed/probe runs and coding-agent authoring costs. '
              'Mock token/cost totals are not estimates of live provider use. No new sandbox execution.',
        comparison='Exact CP5 comparison, including types, exceptions, streams and files. '
                   'All three headline rates use the same non-quarantined training plus held-out cases. '
                   'Coverage includes eligible legacy observations only; dynamic/time paths may be absent. '
                   'Failure causes show the first differing component. Suspected bugs are source-grounded, not proven.',
        archives={'cp%s.tar.gz' % n: digest((EVIDENCE / ('cp%s.tar.gz' % n)).read_bytes()) for n in (5, 6, 7, 8, 9)},
        records='archive!/member identifies an immutable archive member; #case-id identifies a raw replay within it.',
        characterization=dict(plan=plan, verification=characterization),
        anti_gaming_review=read(root / '9/cp9-review.json'),
        totals=totals, projects=reports)


def markdown(report):
    def rate(value):
        return '%s/%s (%.2f%%)' % (value['passed'], value['tests'], value['pass_rate_percent'])
    def block(value, language='json'):
        text = json.dumps(value, sort_keys=True, indent=2) if language == 'json' else value
        fence = '`' * max(3, max((len(s) for s in text.split() if set(s) == {'`'}), default=0) + 1)
        return '\n' + fence + language + '\n' + text + '\n' + fence + '\n'
    lines = ['# Recorded modernization report', '', '**Status: ' + report['status'] + '**', '',
        report['scope'], '', report['comparison'], '',
        'See report.json for exact values, raw-record references, archive hashes and all report fields.', '',
        '| Project | Legacy / legacy | Legacy / modern | Converted / modern | Held-out converted |',
        '|---|---:|---:|---:|---:|']
    for project in report['projects']:
        lines.append('| ' + project['project'] + ' | ' + ' | '.join(
            rate(v) for v in [*project['rates'].values(), project['heldout']]) + ' |')
    lines.extend(['', '## Totals and usage', block(report['totals']),
                  '## Characterization plan and sanity checks', block(report['characterization']),
                  '## Recorded anti-gaming review', block(report['anti_gaming_review'])])
    if 'policy' in report:
        lines.extend(['## Cross-runtime policy (raw rates above are unchanged)', block(report['policy'])])
    if 'evaluation_profile' in report:
        lines.extend(['## Evaluation profile and exposed-case disposition', block(report['evaluation_profile'])])
    for project in report['projects']:
        if 'policy' in project:
            lines.extend(['## Policy results: ' + project['project'], block(project['policy'])])
        lines.extend(['## ' + project['project'], '', '### Evidence references', block(project['records']),
            '### Coverage, exclusions and quarantines', block({k: project[k] for k in
                ('coverage', 'coverage_targets', 'inventory_exclusions', 'quarantine')}),
            '### Repair attempts and usage', block(project['repair']), block(project['usage']),
            '### Unresolved failures', block(project['unresolved']),
            '### Review flags and suspected legacy bugs', block(project['review_flags']),
            block(project['suspected_legacy_bugs']),
            '### Documentation omissions and claim mismatches',
            block(dict(omitted=project['documentation']['omitted'], mismatches=project['documentation_mismatches']))])
        for entry in project['documentation']['entries']:
            lines.extend(['### ' + entry['kind'] + ': ' + entry['key'], '', entry['text'], ''])
        for path, diff in project['diffs'].items():
            lines.extend(['### Diff: ' + path, block(diff, 'diff')])
    return '\n'.join(lines) + '\n'


def generate(output):
    output = output.resolve()
    if any(output == p or p in output.parents for p in
           (ROOT / 'tests', ROOT / 'corpus', EVIDENCE, ROOT / 'src', ROOT / 'scripts')):
        raise ValueError('report output cannot overwrite protected inputs')
    with tempfile.TemporaryDirectory() as directory:
        report = build(Path(directory))
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / 'report.json', report)
    (output / 'report.md').write_text(markdown(report))
    return report


def verify(output):
    with tempfile.TemporaryDirectory() as directory:
        report = build(Path(directory))
    if read(output / 'report.json') != report:
        raise ValueError('report JSON differs from recomputed evidence')
    if (output / 'report.md').read_text() != markdown(report):
        raise ValueError('report Markdown differs from recomputed evidence')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    report = verify(args.verify) if args.verify else generate(args.output)
    print(json.dumps(dict(status=report['status'], totals=report['totals']), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
