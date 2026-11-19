"""Snapshot inventory, isolated Python 2 parsing, and deterministic project facts."""

import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Protocol
import uuid

from modernize.facts_schema import PROJECT, validate, validate_files


EXCLUDED = {'.git', '.venv', '__pycache__', '.pytest_cache'}
EFFECTS = {
    'file_io': ('open', 'file', 'io.open', 'os.open', 'os.remove', 'os.rename', 'os.listdir', 'pathlib'),
    'network': ('socket', 'urllib', 'urllib2', 'httplib', 'requests', 'http'),
    'database': ('sqlite3', 'psycopg2', 'MySQLdb', 'pymysql', 'sqlalchemy'),
    'environment': ('os.getenv', 'os.putenv', 'os.unsetenv', 'os.environ'),
    'time': ('time', 'datetime'),
    'randomness': ('random', 'secrets', 'os.urandom'),
}


def inventory(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('project must be a directory')
    sources, excluded, unsupported = {}, [], []
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in sorted(dirs + names):
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                raise ValueError(f'symlink is unsupported: {relative}')
            if name in dirs:
                if name in EXCLUDED:
                    dirs.remove(name)
                    excluded.append(relative)
                continue
            if not path.is_file():
                raise ValueError(f'non-regular file is unsupported: {relative}')
            with path.open('rb') as stream:
                head = stream.read(256)
                python = path.suffix in ('.py', '.pyw') or (
                    not path.suffix and head.startswith(b'#!') and b'python' in head.splitlines()[0])
                if python:
                    stream.seek(0)
                    raw = stream.read(16 * 1024 * 1024 + 1)
                    if sum(map(len, sources.values())) + len(raw) > 16 * 1024 * 1024:
                        raise ValueError('source snapshot exceeds 16 MiB')
                    sources[relative] = raw
                else:
                    unsupported.append(relative)
    if not sources:
        raise ValueError('no Python source files found')
    return dict(sorted(sources.items())), sorted(excluded), sorted(unsupported)


class LanguageAdapter(Protocol):
    def parse(self, sources: dict[str, bytes]) -> list[dict]: ...
    def list_entry_points(self, facts: list[dict]) -> list[str]: ...
    def convert(self, *args, **kwargs): ...
    def run_tests(self, *args, **kwargs): ...


class Python2Adapter:
    def __init__(self, image, mode='sequential', workers=2):
        if mode not in ('sequential', 'parallel') or type(workers) is not int or not 1 <= workers <= 4:
            raise ValueError('analysis mode must be sequential/parallel and workers must be 1..4')
        self.image, self.mode, self.workers = image, mode, workers
        self.records = []

    def parse(self, sources):
        image = subprocess.run(['docker', 'image', 'inspect', '--format', '{{.Id}}', self.image],
                               capture_output=True, text=True, timeout=10)
        if image.returncode:
            raise ValueError('cannot inspect legacy image: ' + image.stderr.strip())
        self.image_id = image.stdout.strip()
        if not self.image_id.startswith('sha256:'):
            raise ValueError('Docker returned an invalid image identity')
        # Bound concurrency in the controller; each container parses one immutable file.
        items = list(sorted(sources.items()))
        if self.mode == 'parallel':
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                chunks = list(pool.map(self._parse_one, items))
        else:
            chunks = [self._parse_one(item) for item in items]
        files = [chunk for chunk in chunks]
        validate_files(files)
        expected = {path: hashlib.sha256(raw).hexdigest() for path, raw in sources.items()}
        if {f['path']: f['sha256'] for f in files} != expected or len(files) != len(expected):
            raise ValueError('worker paths/hashes do not match immutable snapshot')
        return files

    def _parse_one(self, item):
        path, raw = item
        name = 'modernize-parse-' + uuid.uuid4().hex
        worker = Path(__file__).with_name('analyzer_worker.py').resolve()
        if ',' in str(worker):
            raise ValueError('worker mount path cannot contain commas')
        command = ['docker', 'run', '--rm', '-i', '--name', name, '--network', 'none',
                   '--read-only', '--user', '65534:65534', '--cap-drop', 'ALL',
                   '--security-opt', 'no-new-privileges', '--memory', '128m', '--cpus', '1',
                   '--pids-limit', '32', '--ulimit', 'cpu=10:10',
                   '--tmpfs', '/tmp:rw,nosuid,nodev,size=16m',
                   '--mount', f'type=bind,source={worker},target=/analyzer.py,readonly',
                   '--entrypoint', 'python', self.image_id, '-B', '/analyzer.py']
        payload = dict(files={path: base64.b64encode(raw).decode('ascii')})
        try:
            result = subprocess.run(command, input=json.dumps(payload), capture_output=True,
                                    text=True, timeout=30)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            subprocess.run(['docker', 'rm', '-f', name], capture_output=True, timeout=10)
            if isinstance(error, KeyboardInterrupt):
                raise
            raise ValueError(f'parser timed out: {path}') from None
        record = dict(path=path, command=command, returncode=result.returncode, stderr=result.stderr)
        self.records.append(record)
        if result.returncode:
            raise ValueError(f'parse failed for {path}: {result.stderr.strip()}')
        try:
            files = json.loads(result.stdout)
            validate_files(files)
        except (ValueError, TypeError) as error:
            raise ValueError(f'invalid parser response for {path}: {error}') from error
        if len(files) != 1:
            raise ValueError(f'expected one parsed file: {path}')
        return files[0]

    def list_entry_points(self, facts):
        return sorted(f['path'] + '::' + fn['qualname'] for f in facts
                      for fn in f['functions'] if fn['scope'] == '<module>' and not fn['name'].startswith('<'))

    def convert(self, *args, **kwargs):
        raise NotImplementedError('conversion belongs to CP8')

    def run_tests(self, *args, **kwargs):
        raise NotImplementedError('execution runner belongs to CP3')


def project_index(files):
    modules = {}
    for file in files:
        parts = file['path'].rsplit('.', 1)[0].split('/')
        if parts[-1] == '__init__':
            parts.pop()
        module = '.'.join(parts)
        if module in modules:
            raise ValueError(f'ambiguous module name: {module}')
        modules[module] = file['path']
    module_for = {path: name for name, path in modules.items()}
    definitions = {f['path'] + '::' + d['qualname'] for f in files
                   for d in f['functions'] + f['classes']}
    bindings = {}
    imported = {}
    absolute_imports = {f['path'] for f in files if any(
        i['module'] == '__future__' and i['name'] == 'absolute_import' for i in f['imports'])}
    classes = {(f['path'], d['qualname']) for f in files for d in f['classes']}
    for file in files:
        for symbol in file['symbols']:
            key = (file['path'], symbol['scope'], symbol['name'])
            bindings.setdefault(key, []).append(symbol)
        for imp in file['imports']:
            imported[(file['path'], imp['scope'], imp['alias'])] = imp

    def find(path, scope, name):
        current = scope
        while True:
            key = (path, current, name)
            if key in bindings:
                if any(s['kind'] == 'global' for s in bindings[key]) and current != '<module>':
                    return (path, '<module>', name) if (path, '<module>', name) in bindings else None
                return key
            if current == '<module>':
                return None
            current = current.rpartition('.')[0] or '<module>'
            while (path, current) in classes:
                current = current.rpartition('.')[0] or '<module>'

    def import_name(path, imp):
        module = module_for[path]
        package = module if path.endswith('/__init__.py') else module.rpartition('.')[0]
        if imp['level']:
            parts = package.split('.') if package else []
            if imp['level'] > len(parts):
                return None
            prefix = '.'.join(parts[:len(parts) - imp['level'] + 1])
            return '.'.join(p for p in (prefix, imp['module']) if p)
        relative = '.'.join(p for p in (package, imp['module']) if p)
        return relative if relative in modules and path not in absolute_imports else imp['module']

    def canonical(path, scope, name, seen=()):
        root, dot, suffix = name.partition('.')
        key = find(path, scope, root)
        if key is None:
            return name
        if key in seen:
            return None
        symbols = bindings[key]
        kinds = {s['kind'] for s in symbols}
        if kinds == {'import'}:
            if len({s['target'] for s in symbols}) != 1:
                return None
            imp = imported[key]
            module = import_name(path, imp)
            if module is None:
                return None
            member = imp['name'] if imp['name'] not in (None, '*') else ''
            if not imp['name'] and '.' in imp['module'] and imp['alias'] == imp['module'].split('.')[0]:
                module = module.split('.')[0]
            full = '.'.join(p for p in (module, member, suffix) if p)
            parts = full.split('.')
            for cut in range(len(parts), 0, -1):
                prefix = '.'.join(parts[:cut])
                if prefix in modules:
                    rest = '.'.join(parts[cut:])
                    if not rest:
                        return prefix
                    return canonical(modules[prefix], '<module>', rest, seen + (key,))
            return full
        targets = {s['target'] for s in symbols}
        if kinds <= {'function', 'class'} and len(targets) == 1:
            target = path + '::' + next(iter(targets))
            return target + dot + suffix
        return None

    imports, calls, references = [], [], []
    for file in files:
        path = file['path']
        for imp in file['imports']:
            module = import_name(path, imp)
            full = '.'.join(p for p in (module, imp['name']) if p)
            target = modules.get(full) or modules.get(module)
            imports.append(dict(source=path, target=target, **imp))
        for ref in file['references']:
            binding = find(path, ref['scope'], ref['name'].split('.')[0])
            references.append(dict(path=path, binding='::'.join(binding) if binding else None, **ref))
            resolved = canonical(path, ref['scope'], ref['name'])
            if resolved == 'os.environ':
                effect = dict(kind='environment', scope=ref['scope'], line=ref['line'], detail=resolved)
                if effect not in file['side_effects']:
                    file['side_effects'].append(effect)
        for call in file['calls']:
            resolved = canonical(path, call['scope'], call['callee'])
            calls.append(dict(path=path, target=resolved if resolved in definitions else None,
                              resolved_name=resolved, **call))
            for kind, prefixes in EFFECTS.items():
                if resolved and any(resolved == p or resolved.startswith(p + '.') for p in prefixes):
                    effect = dict(kind=kind, scope=call['scope'], line=call['line'], detail=resolved)
                    if effect not in file['side_effects']:
                        file['side_effects'].append(effect)
        file['side_effects'].sort(key=lambda e: (e['line'], e['kind'], e['detail']))
    symbols = [dict(id='::'.join(key), path=key[0], scope=key[1], name=key[2],
                    kinds=sorted({s['kind'] for s in values}),
                    lines=sorted({s['line'] for s in values}))
               for key, values in sorted(bindings.items())]
    return dict(modules=modules, imports=imports, calls=calls, symbols=symbols, references=references)


def scan(root, adapter):
    sources, excluded, unsupported = inventory(root)
    files = adapter.parse(sources)
    index = project_index(files)
    validate_files(files)
    result = dict(schema_version=1, files=files, index=index,
                  inventory=dict(excluded=excluded, unsupported=unsupported),
                  entry_points=adapter.list_entry_points(files))
    validate(result, PROJECT)
    return result
