"""Layered conversion, validated source-only change sets, atomic publication."""

import ast
import base64
import difflib
from importlib import resources
import json
from pathlib import Path, PurePosixPath
import tempfile
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from modernize.characterize import digest, read_observation, write_json
from modernize.llm_prompts import Prompt, strict_json
from modernize.sandbox import snapshot

MECHANICAL_WORKER = '__cp8_mechanical__.py'
VALIDATE_WORKER = '__cp8_validate__.py'


class SourcePatch(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    path: str
    base_sha256: str | None
    source: str = Field(min_length=1, max_length=64000)
    reason: str = Field(min_length=1, max_length=2000)
    hazards: list[Literal['division', 'bytes_unicode', 'comparison_sort', 'iterators']] = Field(min_length=1)

    @field_validator('path')
    @classmethod
    def source_path(cls, value):
        path = PurePosixPath(value)
        if path.is_absolute() or path.as_posix() != value or path.suffix != '.py' or any(
                p in ('..', '.', 'tests', 'fixtures', 'sealed', 'private', '__pycache__') or p.startswith('.')
                for p in path.parts) or value in (MECHANICAL_WORKER, VALIDATE_WORKER):
            raise ValueError('patches must name safe source-only Python paths')
        return value


class SourceChanges(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    patches: list[SourcePatch] = Field(max_length=16)
    needs_human_review: list[str] = Field(max_length=32)


def load_transformation_prompt():
    directory = resources.files('modernize').joinpath('prompts/transformation')
    schema = strict_json(directory.joinpath('transformation.v1.schema.json').read_text())
    if schema != SourceChanges.model_json_schema():
        raise ValueError('transformation schema differs from response model')
    return Prompt('transformation.v1', directory.joinpath('transformation.v1.txt').read_text(), schema, SourceChanges)


def apply_changes(files, changes):
    candidate = dict(files)
    seen = set()
    for patch in changes.patches:
        if patch.path in seen:
            raise ValueError('duplicate patch path')
        seen.add(patch.path)
        previous = files.get(patch.path)
        if patch.base_sha256 != (digest(previous) if previous is not None else None):
            raise ValueError('patch base hash differs from working snapshot: ' + patch.path)
        if previous is None and str(PurePosixPath(patch.path).parent) not in {
                str(PurePosixPath(p).parent) for p in files if p.endswith('.py')}:
            raise ValueError('new helper must be in an existing source directory')
        raw = patch.source.encode('utf-8')
        # Only mechanically converted candidates are parsed by the host Python 3 AST.
        ast.parse(raw, filename=patch.path)
        candidate[patch.path] = raw
    return candidate


def stage(files, directory):
    for path, raw in files.items():
        target = Path(directory) / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)


def sandbox_call(runner, files, worker_name, module, function, args, record_path):
    if worker_name in files:
        raise ValueError('reserved conversion worker path exists')
    with tempfile.TemporaryDirectory() as directory:
        stage(files, directory)
        (Path(directory) / worker_name).write_bytes(Path(__file__).with_name(module).read_bytes())
        record = runner.run(directory, worker_name, function, args=args)
        write_json(record_path, record)
        return read_observation(record)


def save_diffs(before, after, directory):
    changed = []
    for path in sorted(set(before) | set(after)):
        if before.get(path) == after.get(path):
            continue
        diff = ''.join(difflib.unified_diff(before.get(path, b'').decode('utf-8').splitlines(True),
            after[path].decode('utf-8').splitlines(True),
            fromfile='a/' + path if path in before else '/dev/null', tofile='b/' + path))
        target = Path(directory) / (path + '.diff')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(diff)
        changed.append(path)
    return changed


def check_public_api(validation, facts, project_id):
    actual = {(file['path'], d['name']): d for file in validation['files'] for d in file['definitions']}
    for file in facts['files']:
        path = file['path'][len(project_id)+1:]
        for definition in file['functions'] + file['classes']:
            if '<lambda@' in definition['qualname']:
                continue
            key = (path, definition['qualname'])
            if key not in actual:
                raise ValueError('conversion removed existing definition: ' + str(key))
            if 'signature' in definition:
                signature = dict(definition['signature'], defaults=len(definition['signature']['defaults']))
                if actual[key].get('signature') != signature:
                    raise ValueError('conversion changed existing signature: ' + str(key))


def transform(project, project_id, facts, observed, llm, legacy_runner, modern_runner, output):
    output = Path(output).resolve()
    project = Path(project).resolve()
    if output == project or project in output.parents:
        raise ValueError('conversion output must be outside input source')
    files = snapshot(project)
    original_hashes = {p: digest(raw) for p, raw in files.items()}
    paths = [p for p in files if p.endswith('.py')]
    mechanical = sandbox_call(legacy_runner, files, MECHANICAL_WORKER, 'conversion_worker.py',
        'run', (paths,), output / 'mechanical-run.json')
    if set(mechanical['files']) != set(paths):
        raise ValueError('mechanical conversion returned unexpected paths')
    base = dict(files, **{p: base64.b64decode(raw, validate=True) for p, raw in mechanical['files'].items()})
    stage(base, output / 'mechanical')
    save_diffs(files, base, output / 'mechanical-diffs')
    attempts = []
    error = None
    for attempt in range(2):
        response = llm.generate(load_transformation_prompt(), dict(project=project_id,
            source={p: raw.decode('utf-8') for p, raw in base.items() if p.endswith('.py')},
            source_sha256={p: digest(raw) for p, raw in base.items() if p.endswith('.py')},
            facts=facts, observed_training_types=observed, validation_error=error))
        write_json(output / ('changes-%s.json' % attempt), response.model_dump())
        try:
            candidate = apply_changes(base, response)
            validation = sandbox_call(modern_runner, candidate, VALIDATE_WORKER, 'conversion_validate_worker.py',
                'run', (sorted(p for p in candidate if p.endswith('.py')),),
                output / ('validation-%s.json' % attempt))
            if {f['path'] for f in validation['files']} != {p for p in candidate if p.endswith('.py')} or any(
                    not f['compiled'] or not f['imported'] for f in validation['files']):
                raise ValueError('modern validation is incomplete')
            check_public_api(validation, facts, project_id)
            attempts.append(dict(attempt=attempt, accepted=True, error=None))
        except (ValueError, SyntaxError) as invalid:
            error = str(invalid)[:2000]
            attempts.append(dict(attempt=attempt, accepted=False, error=error))
            write_json(output / 'attempts.json', attempts)
            continue
        if original_hashes != {p: digest(raw) for p, raw in snapshot(project).items()}:
            raise ValueError('input source changed during conversion')
        with tempfile.TemporaryDirectory(dir=output) as directory:
            pending = Path(directory) / 'source'
            stage(candidate, pending)
            pending.rename(output / 'source')
        changed = save_diffs(files, candidate, output / 'diffs')
        write_json(output / 'attempts.json', attempts)
        report = dict(project=project_id, changed_files=changed, compile_import_files=len(validation['files']),
            semantic_changed_files=[p.path for p in response.patches], attempts=attempts,
            needs_human_review=response.needs_human_review,
            original_sha256=original_hashes, converted_sha256={p: digest(raw) for p, raw in candidate.items()})
        write_json(output / 'report.json', report)
        return report
    raise ValueError('conversion validation cap reached; no source published')
