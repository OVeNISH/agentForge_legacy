"""Container-only execution with bounded captures and recorded cleanup."""

import base64
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
import uuid

from modernize.analysis import EXCLUDED
from modernize.sandbox_codec import pack_input

MAX_WIRE = 8 * 1024 * 1024


@dataclass(frozen=True)
class Limits:
    timeout_seconds: float = 3.0
    cpu_seconds: int = 2
    memory_mb: int = 128

    def __post_init__(self):
        if type(self.timeout_seconds) not in (int, float) or not 0.1 <= self.timeout_seconds <= 30:
            raise ValueError('timeout_seconds must be 0.1..30')
        if type(self.cpu_seconds) is not int or not 1 <= self.cpu_seconds <= 30:
            raise ValueError('cpu_seconds must be 1..30')
        if type(self.memory_mb) is not int or not 64 <= self.memory_mb <= 512:
            raise ValueError('memory_mb must be 64..512')


def snapshot(project):
    root = Path(project).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('project must be a directory')
    files, size = {}, 0
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in sorted(dirs + names):
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError('snapshot symlink is unsupported: ' + str(path.relative_to(root)))
            if name in dirs:
                if name in EXCLUDED:
                    dirs.remove(name)
                continue
            if not path.is_file():
                raise ValueError('snapshot requires regular files')
            with path.open('rb') as stream:
                raw = stream.read(4 * 1024 * 1024 + 1)
            size += len(raw)
            if size > 4 * 1024 * 1024:
                raise ValueError('execution snapshot exceeds 4 MiB')
            files[path.relative_to(root).as_posix()] = raw
    return dict(sorted(files.items()))


def bounded_start(command, payload, timeout):
    """Keep both Docker streams bounded even if the container protocol is broken."""
    process = subprocess.Popen(command, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    buffers = [bytearray(), bytearray()]
    exceeded = threading.Event()

    def read(stream, buffer):
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            remaining = MAX_WIRE - len(buffer)
            buffer.extend(chunk[:remaining])
            if len(chunk) > remaining:
                exceeded.set()

    def write():
        try:
            process.stdin.write(payload)
            process.stdin.close()
        except (BrokenPipeError, OSError):
            pass

    threads = [threading.Thread(target=read, args=(stream, buffer), daemon=True)
               for stream, buffer in zip((process.stdout, process.stderr), buffers)]
    threads.append(threading.Thread(target=write, daemon=True))
    for thread in threads:
        thread.start()
    deadline = time.monotonic() + timeout
    failure = None
    while process.poll() is None:
        if exceeded.is_set() or time.monotonic() >= deadline:
            failure = 'wire_capture_limit' if exceeded.is_set() else 'supervisor_timeout'
            process.kill()
            break
        time.sleep(0.01)
    process.wait(timeout=5)
    for thread in threads:
        thread.join(timeout=5)
    process.stdout.close()
    process.stderr.close()
    if exceeded.is_set():
        failure = 'wire_capture_limit'
    return bytes(buffers[0]), bytes(buffers[1]), process.returncode, failure


def validate_value(value, depth=0):
    if depth > 30 or not isinstance(value, dict) or not isinstance(value.get('type'), str):
        raise ValueError('invalid typed value')
    kind = value['type']
    if kind == 'NoneType' and set(value) == {'type'}:
        return
    if kind in ('str', 'bytes') and set(value) == {'type', 'base64'}:
        base64.b64decode(value['base64'], validate=True)
        return
    if kind in ('str', 'unicode', 'int', 'long', 'float', 'bool') and set(value) == {'type', 'value'}:
        if type(value['value']) is (bool if kind == 'bool' else str):
            return
    if kind in ('list', 'tuple', 'set', 'frozenset', 'dict') and set(value) == {'type', 'items'}:
        if not isinstance(value['items'], list):
            raise ValueError('invalid typed collection')
        for item in value['items']:
            if kind == 'dict':
                if not isinstance(item, list) or len(item) != 2:
                    raise ValueError('invalid typed mapping entry')
                for member in item:
                    validate_value(member, depth + 1)
            else:
                validate_value(item, depth + 1)
        return
    raise ValueError('unsupported typed value')


def validate_result(result):
    expected = {'status', 'value', 'exception', 'target_exit_code', 'stdout_base64',
                'stderr_base64', 'files', 'capture_error'}
    if not isinstance(result, dict) or set(result) != expected:
        raise ValueError('invalid sandbox result fields')
    if result['status'] not in ('completed', 'exception', 'timeout', 'resource_limit',
                                'capture_error', 'infrastructure_error'):
        raise ValueError('invalid sandbox status')
    if type(result['target_exit_code']) is not int or not isinstance(result['files'], list):
        raise ValueError('invalid sandbox process/files result')
    for field in ('stdout_base64', 'stderr_base64'):
        base64.b64decode(result[field], validate=True)
    if result['capture_error'] is not None and not isinstance(result['capture_error'], str):
        raise ValueError('invalid capture error')
    if result['status'] == 'completed' and not isinstance(result['value'], dict):
        raise ValueError('missing typed return value')
    if result['status'] == 'exception' and not isinstance(result['exception'], dict):
        raise ValueError('missing exception')
    if result['value'] is not None:
        validate_value(result['value'])
    if result['exception'] is not None:
        exception = result['exception']
        if not isinstance(exception, dict) or set(exception) != {'module', 'name', 'args', 'message', 'traceback'}:
            raise ValueError('invalid exception fields')
        if any(not isinstance(exception[key], str) for key in ('module', 'name', 'message')):
            raise ValueError('invalid exception strings')
        validate_value(exception['args'])
        if not isinstance(exception['traceback'], list):
            raise ValueError('invalid traceback')
        for frame in exception['traceback']:
            if not isinstance(frame, dict) or set(frame) != {'file', 'line', 'function'} or \
                    type(frame['line']) is not int or frame['line'] < 1 or \
                    any(not isinstance(frame[key], str) for key in ('file', 'function')):
                raise ValueError('invalid traceback frame')
    for file in result['files']:
        if not isinstance(file, dict) or not isinstance(file.get('path'), str):
            raise ValueError('invalid captured file')
        if file['path'].startswith('/') or '..' in file['path'].split('/'):
            raise ValueError('unsafe captured file path')
        if file.get('kind') == 'file':
            raw = base64.b64decode(file['base64'], validate=True)
            if hashlib.sha256(raw).hexdigest() != file['sha256']:
                raise ValueError('captured file hash mismatch')
        elif file.get('kind') != 'symlink' or not isinstance(file.get('target'), str):
            raise ValueError('unsupported captured file kind')


class SandboxRunner:
    def __init__(self, image, limits=None):
        self.image = image
        self.limits = limits or Limits()

    def run(self, project, script, function=None, args=(), kwargs=None):
        if type(args) not in (list, tuple) or (kwargs is not None and (
                type(kwargs) is not dict or any(not isinstance(k, str) for k in kwargs))):
            raise ValueError('args must be a sequence and kwargs must have string keys')
        files = snapshot(project)
        if script not in files or script.startswith('/') or '..' in script.split('/'):
            raise ValueError('script must name a snapshot file')
        if function is not None and (not isinstance(function, str) or not all(
                name.isidentifier() for name in function.split('.'))):
            raise ValueError('function must be a dotted identifier')
        payload = dict(files={p: base64.b64encode(raw).decode('ascii') for p, raw in files.items()},
                       script=script, function=function, args=pack_input(args), kwargs=pack_input(kwargs or {}),
                       timeout_seconds=self.limits.timeout_seconds,
                       cpu_seconds=self.limits.cpu_seconds, memory_mb=self.limits.memory_mb)
        wire = json.dumps(payload, allow_nan=False).encode()
        if len(wire) > MAX_WIRE:
            raise ValueError('execution request exceeds wire limit')
        image = subprocess.run(['docker', 'image', 'inspect', self.image],
                               capture_output=True, text=True, timeout=10)
        if image.returncode:
            raise ValueError('cannot inspect runtime image: ' + image.stderr.strip())
        metadata = json.loads(image.stdout)[0]
        image_id = metadata['Id']
        if not re.fullmatch('sha256:[0-9a-f]{64}', image_id) or metadata.get('Os') != 'linux':
            raise ValueError('expected a Linux runtime image identity')
        if metadata.get('Config', {}).get('Volumes'):
            raise ValueError('runtime images with declared volumes are forbidden')
        name = 'modernize-run-' + uuid.uuid4().hex
        command = ['docker', 'create', '-i', '--name', name, '--network', 'none',
                   '--log-driver', 'none',
                   '--read-only', '--user', '65534:65534', '--cap-drop', 'ALL',
                   '--security-opt', 'no-new-privileges', '--memory', f'{self.limits.memory_mb}m',
                   '--memory-swap', f'{self.limits.memory_mb}m', '--cpus', '1', '--pids-limit', '32',
                   '--ulimit', 'nofile=64:64', '--ulimit', 'core=0:0',
                   '--tmpfs', '/scratch:rw,nosuid,nodev,noexec,size=32m,mode=1777',
                   '--workdir', '/scratch', '--env', 'PYTHONHASHSEED=0',
                   '--env', 'PYTHONDONTWRITEBYTECODE=1']
        for module in ('sandbox_worker.py', 'sandbox_codec.py'):
            path = Path(__file__).with_name(module).resolve()
            if ',' in str(path):
                raise ValueError('trusted mount path cannot contain commas')
            command += ['--mount', f'type=bind,source={path},target=/{module},readonly']
        command += ['--entrypoint', 'python', image_id, '-B', '/sandbox_worker.py']
        created = subprocess.run(command, capture_output=True, text=True, timeout=15)
        if created.returncode:
            raise ValueError('cannot create sandbox: ' + created.stderr.strip())
        record = dict(image_id=image_id, create_command=command,
                      source_sha256={p: hashlib.sha256(raw).hexdigest() for p, raw in files.items()},
                      request=dict(script=script, function=function, args=payload['args'], kwargs=payload['kwargs']),
                      limits=dict(timeout_seconds=self.limits.timeout_seconds,
                                  cpu_seconds=self.limits.cpu_seconds, memory_mb=self.limits.memory_mb))
        try:
            output, error, exit_code, failure = bounded_start(
                ['docker', 'start', '-a', '-i', name], wire, self.limits.timeout_seconds + 10)
            if failure:
                subprocess.run(['docker', 'kill', name], capture_output=True, timeout=10)
            state = subprocess.run(['docker', 'inspect', name],
                                   capture_output=True, text=True, timeout=10)
            if state.returncode:
                raise ValueError('cannot inspect sandbox state: ' + state.stderr.strip())
            observed = json.loads(state.stdout)[0]
            policy = observed['HostConfig']
            isolation = {key: policy[key] for key in ('NetworkMode', 'ReadonlyRootfs',
                         'Memory', 'MemorySwap', 'NanoCpus', 'PidsLimit', 'CapDrop', 'SecurityOpt', 'LogConfig')}
            isolation['User'] = observed['Config']['User']
            isolation['Mounts'] = [dict(type=m['Type'], destination=m['Destination'], rw=m['RW'])
                                   for m in observed['Mounts']]
            record.update(container_state=observed['State'], isolation=isolation, docker_exit_code=exit_code,
                          protocol_error=failure, supervisor_stderr_base64=base64.b64encode(error).decode('ascii'))
            try:
                result = json.loads(output)
                validate_result(result)
                if failure or exit_code != 0 or observed['State']['Running'] or observed['State']['OOMKilled']:
                    raise ValueError(f'supervisor did not finish cleanly: exit={exit_code}')
            except (ValueError, TypeError, KeyError) as invalid:
                result = None
                record['protocol_error'] = failure or str(invalid)
            record['result'] = result
        finally:
            removed = subprocess.run(['docker', 'rm', '-f', name], capture_output=True, text=True, timeout=10)
            if removed.returncode:
                raise ValueError('sandbox cleanup failed: ' + removed.stderr.strip())
        record['container_removed'] = True
        return record

    def run_tests(self, project, script):
        """Run a supplied test script under the same execution policy."""
        return self.run(project, script)
