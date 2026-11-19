"""Run fresh corpus stages; exit 3 after reporting unresolved migrations."""

import argparse
from datetime import datetime
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from baseline_corpus import summarize
from characterize_corpus import RecordedProposalClient
from document_corpus import RecordedDocumentationClient
from transform_corpus import RecordedTransformationClient
from repair_corpus import RecordedRepairClient
from report_corpus import markdown
from pipeline_repair_client import PolicyRepairClient, review_hash
from revalidation_inputs import RevalidationProposalClient, exposed_ids, FRESH
from modernize import comparison as cross_runtime
from modernize.analysis import Python2Adapter, scan
from modernize.characterize import (Characterizer, comparable, coverage, digest,
    export_training, read_observation, replay, seal, verify_seal, write_json)
from modernize.config import load_config
from modernize.documentation import fingerprint, generate, observed_claims
from modernize.llm_run import LLMRun, RateCard, usage_summary
from modernize.repair import repair, replay as replay_repaired, review_changes
from modernize.repair import metrics
from modernize.sandbox import SandboxRunner, snapshot
from modernize.transformation import save_diffs, stage, transform

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = [ROOT / p for p in ('tests', 'corpus', 'src', 'scripts', 'docs/evidence')]


def read(path):
    return json.loads(path.read_text())


def mock_run(client, output):
    return LLMRun(client, output, RateCard(client.model, Decimal(0), Decimal(0), Decimal(0),
        'deterministic mock replay only; no provider billing', '2026-11-19'))


def project_names(project):
    names = [p['id'] for p in read(ROOT / 'corpus/manifest.json')['projects']]
    if project != 'all' and project not in names:
        raise ValueError('unknown corpus project: ' + project)
    return names if project == 'all' else [project]


def summarize_run(output):
    """Recompute report numbers from this run's raw replays, never CP5–CP10 archives."""
    run = read(output / 'run.json')
    if read(output / 'inputs-before.json') != read(output / 'inputs-after.json'):
        raise ValueError('pipeline changed protected inputs')
    reports, calls = [], []
    last_repair = max((datetime.fromisoformat(json.loads(line)['timestamp'])
        for name in run['projects'] for line in (output / name / 'repair-llm/calls.jsonl').read_text().splitlines()), default=None)
    for name in run['projects']:
        store = output / name
        oracle = store / 'characterization'
        verify_seal(oracle)
        training = read(oracle / 'training' / (name + '.json'))
        heldout = read(oracle / 'sealed' / (name + '.json'))
        fixtures = training + heldout
        cp5 = read(oracle / 'private' / (name + '-report.json'))
        records = {r['label']: r['record'] for r in map(json.loads,
            (oracle / 'private/runs.jsonl').read_text().splitlines())}
        observations = []
        legacy = []
        for fixture in fixtures:
            case_id = fixture['case']['id']
            for repeat in range(cp5['repeats']):
                record = records['%s:%s:%s' % (name, case_id, repeat)]
                if comparable(record) != fixture['expected']:
                    raise ValueError('legacy oracle replay differs from fixture')
                observations.append(read_observation(record))
            record = records[name + ':' + case_id + ':1']
            legacy.append(dict(id=case_id, actual=comparable(record), record=record, passed=True))
        if coverage(cp5['inventory'], observations) != cp5['coverage']:
            raise ValueError('coverage differs from raw legacy observations')
        modern = read(store / 'baseline-modern.json')
        converted_training = read(store / 'repair/training-final.json')
        converted_heldout = read(store / 'heldout.json')
        converted = converted_training + converted_heldout
        for result in converted_heldout:
            started = datetime.fromisoformat(result['record']['container_state']['StartedAt'].replace('Z', '+00:00'))
            if last_repair is not None and started <= last_repair:
                raise ValueError('held-out run preceded repair completion')
        final = snapshot(store / 'repair/source')
        if read(store / 'final-source-lock.json') != {p: digest(b) for p, b in final.items()}:
            raise ValueError('final source lock differs')
        for result in converted:
            if any(result['record']['source_sha256'].get(p) != digest(b) for p, b in final.items()):
                raise ValueError('converted replay differs from final source')
        attempts = read(store / 'repair/attempts.json')
        repair_report = read(store / 'repair/report.json')
        if attempts != repair_report['attempts']:
            raise ValueError('repair attempts differ from report')
        docs = read(store / 'documentation/documentation.json')
        quarantines = read(oracle / 'private' / (name + '-quarantine.json'))
        with tempfile.TemporaryDirectory() as directory:
            save_diffs(snapshot(store / 'documentation/source'), final, Path(directory))
            if snapshot(directory) != snapshot(store / 'diffs'):
                raise ValueError('saved diffs differ from final source')
        diffs = {p.relative_to(store / 'diffs').as_posix(): p.read_text()
                 for p in sorted((store / 'diffs').rglob('*.diff'))}
        usage = {}
        for label, path in [('characterization', 'characterization/private/llm'),
                            ('documentation', 'documentation/llm'), ('conversion', 'conversion/llm'), ('repair', 'repair-llm')]:
            stage_calls = [json.loads(line) for line in (store / path / 'calls.jsonl').read_text().splitlines()]
            usage[label] = usage_summary(stage_calls)
            calls.extend(stage_calls)
        expected = {f['case']['id']: f for f in fixtures}
        unresolved = [dict(id=r['id'], case=expected[r['id']]['case'], expected=expected[r['id']]['expected'],
            actual=r['actual'], run=name + ('/repair/training-final.json' if r in converted_training else '/heldout.json'))
            for r in converted if not r['passed']]
        flags = read(store / 'conversion/report.json')['needs_human_review'] + repair_report['needs_human_review']
        reports.append(dict(project=name, status='needs_human_review' if unresolved or flags else 'passed',
            rates=dict(legacy_on_legacy=summarize(fixtures, legacy), legacy_on_modern=summarize(fixtures, modern),
                       converted_on_modern=summarize(fixtures, converted)),
            training=summarize(training, converted_training), heldout=summarize(heldout, converted_heldout),
            coverage=cp5['coverage'], coverage_targets=cp5['targets'], quarantine=quarantines,
            inventory_exclusions=cp5['inventory']['exclusions'], repair=dict(attempts=attempts,
                retry_counts=repair_report['retry_counts'], max_attempts_per_function=repair_report['max_attempts_per_function']),
            usage=usage, diffs=diffs, documentation=docs, documentation_mismatches=read(store / 'documentation/report.json')['mismatches'],
            suspected_legacy_bugs=[dict(key=e['key'], text=e['response']['summary']) for e in docs['entries']
                                  if 'suspected legacy bug:' in e['response']['summary'].lower()],
            unresolved=unresolved, review_flags=flags,
            records=dict(characterization=name + '/characterization/private/runs.jsonl',
                baseline=name + '/baseline-modern.json', training=name + '/repair/training-final.json',
                heldout=name + '/heldout.json', documentation=name + '/documentation/documentation.json',
                diffs=name + '/diffs/', repair=name + '/repair/attempts.json')))
    totals = {}
    for key in reports[0]['rates']:
        tests = sum(p['rates'][key]['tests'] for p in reports)
        passed = sum(p['rates'][key]['passed'] for p in reports)
        totals[key] = dict(tests=tests, passed=passed, pass_rate_percent=100 * passed / tests)
    totals.update(quarantined=sum(len(p['quarantine']) for p in reports),
        heldout_tests=sum(p['heldout']['tests'] for p in reports), heldout_passed=sum(p['heldout']['passed'] for p in reports),
        repair_proposals=sum(len(p['repair']['attempts']) for p in reports),
        accepted_repairs=sum(a['accepted'] for p in reports for a in p['repair']['attempts']), usage=usage_summary(calls))
    report = dict(schema_version='cp11.v1', status='needs_human_review' if any(p['status'] != 'passed' for p in reports) else 'passed',
        scope='Fresh sandbox executions using recorded corpus mock proposals. No prior run archive supplies outcomes. '
              'Mock tokens/costs do not estimate provider use. Raw stage records are retained under this run directory.',
        comparison='Exact frozen comparisons; all headline rates use training plus held-out cases. '
                   'Held-out cases run only after every repair has finished. No normalization or new exclusions.',
        characterization=dict(repeats=3, max_rounds=2, line_target=90, branch_target=90,
            limitation='CP5 mutation sanity evidence remains separately archived; mutations are not rerun by this pipeline.'),
        anti_gaming_review=dict(status='needs_human_review', automatic={n: read(output / n / 'review.json') for n in run['projects']},
            limitation='Heuristic scan only; fresh diffs require human review.'),
        totals=totals, projects=reports)
    if run.get('comparison', 'strict') != 'strict':
        if run['comparison'] != cross_runtime.NAME:
            raise ValueError('unknown comparison policy')
        policy_hash = digest(Path(cross_runtime.__file__).read_bytes())
        if run['comparison_sha256'] != policy_hash:
            raise ValueError('comparison implementation changed since execution')
        source_review = read(output / 'source-review.json')
        if run['source_review_sha256'] != digest((output / 'source-review.json').read_bytes()):
            raise ValueError('source review changed since execution')
        for project in reports:
            name = project['project']
            store = output / name
            training = read(store / 'characterization/training' / (name + '.json'))
            heldout = read(store / 'characterization/sealed' / (name + '.json'))
            fixtures = training + heldout
            final = read(store / 'repair/training-final.json') + read(store / 'heldout.json')
            raw = {r['id']: r for r in final}
            policy = metrics(fixtures, final, cross_runtime.equal)
            policy['training'] = metrics(training, read(store / 'repair/training-final.json'), cross_runtime.equal)
            policy['heldout'] = metrics(heldout, read(store / 'heldout.json'), cross_runtime.equal)
            source = {p: digest(b) for p, b in snapshot(store / 'repair/source').items()}
            assessment = source_review['projects'][name]
            reviewed = ({p:review_hash(b) for p,b in snapshot(store / 'repair/source').items() if p.endswith('.py')} ==
                        assessment['executable_sha256']) if 'executable_sha256' in assessment else source == assessment['source_sha256']
            policy['source_review_matches'] = reviewed
            policy['failures'] = [dict(case=f['case'], expected=f['expected'], actual=raw[f['case']['id']]['actual'])
                                  for f in fixtures if f['case']['id'] in policy['unresolved']]
            project['policy'] = policy
            project['status'] = 'passed' if not policy['unresolved'] and reviewed else 'needs_human_review'
            if 'evaluation_profile' in run:
                if any(f['case']['id'] in exposed_ids(name) for f in heldout):
                    raise ValueError('exposed regression case was reused as final held-out input')
        count = sum(p['policy']['tests'] for p in reports)
        passed = sum(p['policy']['passed'] for p in reports)
        report['policy'] = dict(name=cross_runtime.NAME, implementation_sha256=policy_hash,
            tests=count, passed=passed, pass_rate_percent=100 * passed / count,
            heldout_tests=sum(p['policy']['heldout']['tests'] for p in reports),
            heldout_passed=sum(p['policy']['heldout']['passed'] for p in reports),
            source_review=source_review, source_review_sha256=run['source_review_sha256'])
        report['status'] = 'passed' if all(p['status'] == 'passed' for p in reports) else 'needs_human_review'
        report['anti_gaming_review']['source_review'] = source_review
        report['anti_gaming_review']['status'] = 'recorded_source_review_matches' if all(
            p['policy']['source_review_matches'] for p in reports) else 'needs_human_review'
        report['comparison'] += ' Versioned policy results are separate; raw rates above remain exact. '
        report['comparison'] += 'Policy status requires every eligible case and the independently recorded source review to match.'
        if 'evaluation_profile' in run:
            report['evaluation_profile'] = run['evaluation_profile']
            report['comparison'] += ' Prior exposed cases are retained as training regressions; final held-out results use fresh inputs only.'
    return report


def verify(output):
    report = summarize_run(output)
    if read(output / 'report.json') != report or (output / 'report.md').read_text() != markdown(report):
        raise ValueError('report differs from recomputed raw run records')
    return report


def execute(output, project='all', analysis='sequential', workers=2, config=None, comparison='strict'):
    config = config or load_config(None)
    names = project_names(project)
    output = output.resolve()
    if any(output == p.resolve() or p.resolve() in output.parents for p in PROTECTED + [ROOT / '.git', ROOT / '.venv']):
        raise ValueError('pipeline output cannot overwrite protected inputs')
    output.mkdir(parents=True, exist_ok=False)
    before = fingerprint(PROTECTED)
    write_json(output / 'inputs-before.json', before)
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout
    run = dict(status='running', projects=names, revision=revision, tracked_changes=dirty,
               config=config.to_dict(), analysis=analysis, workers=workers, stage='analysis')
    if comparison != 'strict':
        if comparison != cross_runtime.NAME:
            raise ValueError('unknown comparison policy')
        review = ROOT / 'docs/evidence/cp11-policy-source-review.v2.json'
        (output / 'source-review.json').write_bytes(review.read_bytes())
        run.update(comparison=comparison, comparison_sha256=digest(Path(cross_runtime.__file__).read_bytes()),
                   source_review_sha256=digest(review.read_bytes()),
                   evaluation_profile=dict(name='fresh-revalidation.v2', fresh_inputs_sha256=digest(FRESH.read_bytes()),
                       disposition='All previously exposed proposal IDs remain eligible regression/training cases; only fresh IDs may be sealed.'))
    write_json(output / 'run.json', run)
    legacy, modern = SandboxRunner(config.legacy_image), SandboxRunner(config.modern_image)
    try:
        print('analysis', flush=True)
        adapter = Python2Adapter(config.legacy_image, analysis, workers)
        facts = scan(ROOT / 'corpus', adapter)
        write_json(output / 'facts.json', facts)
        write_json(output / 'analysis-run.json', dict(image_id=adapter.image_id, parses=adapter.records))
        for name in names:
            store = output / name
            original = store / 'original'
            stage(snapshot(ROOT / 'corpus' / name), original)
            run['stage'] = name + ':characterization'
            write_json(output / 'run.json', run)
            print(run['stage'], flush=True)
            exclusions = () if comparison == 'strict' else exposed_ids(name)
            characterizer = Characterizer(legacy, None, store / 'characterization', heldout_exclude_ids=exclusions)
            proposal_client = RecordedProposalClient() if comparison == 'strict' else RevalidationProposalClient()
            characterizer.llm = mock_run(proposal_client, store / 'characterization/private/llm')
            characterized = characterizer.generate(original, name)
            if characterized['uncovered_functions']:
                raise ValueError('characterization left functions uncovered')
            seal(store / 'characterization')
            training_root = export_training(store / 'characterization', store / 'training-export')
            training = read(training_root / (name + '.json'))
            # The trusted baseline controller reads sealed fixtures; later LLMs receive only the export.
            fixtures = training + read(store / 'characterization/sealed' / (name + '.json'))
            run['stage'] = name + ':baseline'
            write_json(output / 'run.json', run)
            print(run['stage'], flush=True)
            write_json(store / 'baseline-modern.json', replay(modern, original, fixtures))
            run['stage'] = name + ':documentation'
            write_json(output / 'run.json', run)
            print(run['stage'], flush=True)
            report = generate(original, name, facts, training, mock_run(RecordedDocumentationClient(), store / 'documentation/llm'),
                              legacy, store / 'documentation')
            write_json(store / 'documentation/report.json', report)
            observed = {f['path'] + '::' + fn['qualname']: observed_claims(training, f['path'][len(name)+1:], fn['qualname'])
                        for f in facts['files'] if f['path'].startswith(name + '/') for fn in f['functions']
                        if '<lambda@' not in fn['qualname']}
            files = [f for f in facts['files'] if f['path'].startswith(name + '/')]
            project_facts = dict(files=[{k: v for k, v in f.items() if k not in ('references', 'symbols')} for f in files],
                calls=[c for c in facts['index']['calls'] if c['path'].startswith(name + '/')],
                imports=[i for i in facts['index']['imports'] if i['source'].startswith(name + '/')])
            for label in ('conversion', 'repair'):
                run['stage'] = name + ':' + label
                write_json(output / 'run.json', run)
                print(run['stage'], flush=True)
                if label == 'conversion':
                    transform(store / 'documentation/source', name, project_facts, observed,
                        mock_run(RecordedTransformationClient(), store / 'conversion/llm'), legacy, modern, store / 'conversion')
                else:
                    client = RecordedRepairClient() if comparison == 'strict' else PolicyRepairClient()
                    repair(store / 'conversion/source', name, dict(files=files), training,
                        mock_run(client, store / 'repair-llm'), modern, store / 'repair',
                        comparison=None if comparison == 'strict' else cross_runtime.equal)
            final = snapshot(store / 'repair/source')
            write_json(store / 'final-source-lock.json', {p: digest(b) for p, b in final.items()})
            save_diffs(snapshot(store / 'documentation/source'), final, store / 'diffs')
            write_json(store / 'review.json', review_changes(snapshot(store / 'conversion/mechanical'), final))
        for name in names:
            store = output / name
            run['stage'] = name + ':heldout'
            write_json(output / 'run.json', run)
            print(run['stage'], flush=True)
            verify_seal(store / 'characterization')
            heldout = read(store / 'characterization/sealed' / (name + '.json'))
            write_json(store / 'heldout.json', replay_repaired(modern, snapshot(store / 'repair/source'), heldout))
    except Exception as error:
        run.update(status='failed', error=str(error))
        raise
    finally:
        after = fingerprint(PROTECTED)
        write_json(output / 'inputs-after.json', after)
        write_json(output / 'run.json', run)
        if before != after:
            raise ValueError('pipeline changed protected inputs')
    report = summarize_run(output)
    write_json(output / 'report.json', report)
    (output / 'report.md').write_text(markdown(report))
    run.update(status=report['status'], stage='report')
    write_json(output / 'run.json', run)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    group.add_argument('--compare', nargs=2, type=Path, metavar=('FIRST', 'SECOND'))
    parser.add_argument('--project', default='all')
    parser.add_argument('--analysis', choices=('sequential', 'parallel'), default='sequential')
    parser.add_argument('--workers', type=int, choices=range(1, 5), default=2)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--comparison', choices=('strict', cross_runtime.NAME), default='strict')
    args = parser.parse_args(argv)
    try:
        if args.compare:
            first, second = [verify(p) for p in args.compare]
            def rates(report):
                return {p['project']: dict(rates=p['rates'], heldout=p['heldout'], **(
                    dict(policy={k:p['policy'][k] for k in ('tests', 'passed', 'pass_rate_percent', 'heldout')}) if 'policy' in p else {}))
                    for p in report['projects']}
            same = rates(first) == rates(second)
            print(json.dumps(dict(pass_rates_reproduced=same, first=rates(first), second=rates(second)), indent=2))
            return 0 if same else 1
        report = verify(args.verify) if args.verify else execute(args.output, args.project, args.analysis, args.workers, load_config(args.config), args.comparison)
        print(json.dumps(dict(status=report['status'], totals=report['totals']), sort_keys=True, indent=2))
        if 'policy' in report:
            print(json.dumps(dict(policy={k:v for k,v in report['policy'].items() if k != 'source_review'}), sort_keys=True, indent=2))
        print('Report: ' + str((args.verify or args.output) / 'report.md'), flush=True)
        return 0 if args.verify or report['status'] == 'passed' else 3
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print('pipeline error: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
