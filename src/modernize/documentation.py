"""Bottom-up documentation with training-only observation claims and frozen inputs."""

import base64
from importlib import resources
import json
from pathlib import Path
import tempfile

from pydantic import BaseModel, ConfigDict, Field

from modernize.characterize import digest, read_observation, write_json
from modernize.facts_schema import PROJECT, validate, validate_files
from modernize.llm_prompts import Prompt, strict_json
from modernize.sandbox import snapshot

MARKER = '[Machine-generated]'
WORKER = '__cp7__.py'


class DocumentationResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    summary: str = Field(min_length=1, max_length=4000)
    observed_return_types: list[str] = Field(max_length=32)
    observed_exceptions: list[str] = Field(max_length=32)
    limitations: str = Field(min_length=1, max_length=2000)


def load_documentation_prompt():
    directory = resources.files('modernize').joinpath('prompts/documentation')
    schema = strict_json(directory.joinpath('documentation.v1.schema.json').read_text())
    if schema != DocumentationResponse.model_json_schema():
        raise ValueError('documentation schema differs from response model')
    return Prompt('documentation.v1', directory.joinpath('documentation.v1.txt').read_text(),
                  schema, DocumentationResponse)


def observed_claims(fixtures, path, target):
    outcomes = [f['expected']['outcome'] for f in fixtures
                if f['case']['path'] == path and f['case']['target'] == target]
    return dict(cases=len(outcomes),
        return_types=sorted({o['value']['type'] for o in outcomes if o['status'] == 'completed'}),
        exceptions=sorted({o['module'] + '.' + o['name'] for o in outcomes if o['status'] == 'exception'}))


def cross_check(response, observed):
    return [dict(field=field, claimed=sorted(set(claimed)), observed=observed[key])
            for field, claimed, key in (
                ('observed_return_types', response.observed_return_types, 'return_types'),
                ('observed_exceptions', response.observed_exceptions, 'exceptions'))
            if set(claimed) != set(observed[key])]


def render(response):
    return (MARKER + '\n' + response.summary + '\n\nObserved return types: ' +
        ', '.join(response.observed_return_types) + '\nObserved exceptions: ' +
        ', '.join(response.observed_exceptions) + '\nLimitations: ' + response.limitations)


def fingerprint(paths):
    return {str(p): digest(p.read_bytes()) for root in paths for p in sorted(Path(root).rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def generate(project, project_id, facts, fixtures, llm, runner, output):
    """fixtures must be CP5's training-only export; never pass sealed records here."""
    validate(facts, PROJECT)
    validate_files(facts['files'])
    output = Path(output)
    if output.resolve() == Path(project).resolve() or Path(project).resolve() in output.resolve().parents:
        raise ValueError('documentation output must be outside original source')
    source = snapshot(project)
    if WORKER in source:
        raise ValueError('reserved documentation worker path exists')
    files = [f for f in facts['files'] if f['path'].startswith(project_id + '/')]
    if {f['path'][len(project_id)+1:]: f['sha256'] for f in files} != {
            p: digest(raw) for p, raw in source.items() if p.endswith('.py')}:
        raise ValueError('documentation facts do not match source snapshot')
    original_hashes = {p: digest(raw) for p, raw in source.items()}
    prompt = load_documentation_prompt()
    entries, omitted, insertion = [], [], {}
    functions = {f['path'] + '::' + fn['qualname']: (f, fn)
                 for f in files for fn in f['functions']}
    calls = facts['index']['calls']
    seen, order = set(), []

    def visit(key):
        if key in seen:
            return
        seen.add(key)
        for call in calls:
            if call['path'] + '::' + call['scope'] == key and call['target'] in functions:
                visit(call['target'])
        order.append(key)
    for key in sorted(functions):
        visit(key)

    def document(kind, key, context, observed=None):
        context = dict(context, kind=kind, key=key)
        response = llm.generate(prompt, context)
        entry = dict(kind=kind, key=key, response=response.model_dump(), text=render(response),
                     cross_check=cross_check(response, observed) if observed is not None else [],
                     observed=observed, prose_validation='source-grounded description; prose not mechanically proven')
        entries.append(entry)
        return entry['text']

    for key in order:
        file, function = functions[key]
        path = file['path'][len(project_id)+1:]
        if '<lambda@' in function['qualname']:
            omitted.append(dict(key=key, reason='lambda expressions have no writable docstring suite; documented by enclosing function'))
            continue
        observed = observed_claims(fixtures, path, function['qualname'])
        text = document('function', key, dict(facts=function, source=source[path].decode('utf-8'),
            callers=[c for c in calls if c['target'] == key],
            callees=[c for c in calls if c['path'] == file['path'] and c['scope'] == function['qualname']],
            callee_docs=[e for e in entries if any(c['target'] == e['key'] for c in calls
                if c['path'] == file['path'] and c['scope'] == function['qualname'])],
            side_effects=[s for s in file['side_effects'] if s['scope'] == function['qualname']],
            observed=observed), observed)
        insertion.setdefault(path, {})[function['qualname']] = text
    for file in files:
        path = file['path'][len(project_id)+1:]
        for cls in file['classes']:
            key = file['path'] + '::' + cls['qualname']
            text = document('class', key, dict(facts=cls, methods=[e for e in entries
                if e['key'].startswith(key + '.')], source=source[path].decode('utf-8')))
            insertion.setdefault(path, {})[cls['qualname']] = text
    for file in files:
        path = file['path'][len(project_id)+1:]
        text = document('module', file['path'], dict(facts=file,
            definitions=[e for e in entries if e['key'].startswith(file['path'] + '::')]))
        insertion.setdefault(path, {})['<module>'] = text
    architecture = document('package', project_id, dict(modules=[e for e in entries if e['kind'] == 'module'],
        imports=[i for i in facts['index']['imports'] if i['source'].startswith(project_id + '/')]))
    with tempfile.TemporaryDirectory() as directory:
        staged = Path(directory)
        for path, raw in source.items():
            target = staged / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        (staged / WORKER).write_bytes(Path(__file__).with_name('documentation_worker.py').read_bytes())
        record = runner.run(staged, WORKER, 'run', args=(insertion,))
        write_json(output / 'validation-run.json', record)
        validated = read_observation(record)
    if set(validated) != set(insertion):
        raise ValueError('documentation validator returned unexpected paths')
    if original_hashes != {p: digest(raw) for p, raw in snapshot(project).items()}:
        raise ValueError('original source changed during documentation')
    for path, result in validated.items():
        if not result['ast_equivalent'] or not result['compiled']:
            raise ValueError('documentation validation failed')
        for target, reason in result['omitted'].items():
            omitted.append(dict(key=project_id + '/' + path + '::' + target, reason=reason))
        source[path] = base64.b64decode(result['source_base64'], validate=True)
    for path, raw in source.items():
        target = output / 'source' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    write_json(output / 'documentation.json', dict(project=project_id, entries=entries, omitted=omitted))
    (output / 'architecture.md').write_text(architecture + '\n')
    for entry in entries:
        if entry['kind'] == 'module':
            target = output / 'modules' / (entry['key'][len(project_id)+1:] + '.md')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(entry['text'] + '\n')
    return dict(project=project_id, counts={k: sum(e['kind'] == k for e in entries)
        for k in ('function', 'class', 'module', 'package')}, omitted=omitted,
        mismatches=[dict(key=e['key'], differences=e['cross_check']) for e in entries if e['cross_check']])
