"""Python 2/3 supervisor. All project execution stays inside this container."""

from __future__ import print_function

import base64
import hashlib
import importlib
import json
import os
import resource
import runpy
import signal
import stat
import subprocess
import sys
import time
import traceback
import types

from sandbox_codec import outcome_value, unpack_input

MAX_CAPTURE = 1024 * 1024


def child(payload):
    resource.setrlimit(resource.RLIMIT_CPU, (payload['cpu_seconds'], payload['cpu_seconds']))
    memory = payload['memory_mb'] * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_CAPTURE, MAX_CAPTURE))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    script = '/scratch/source/' + payload['script']
    sys.path[:0] = [os.path.dirname(script), '/scratch/source']
    result = dict(status='completed', value=None, exception=None, capture_error=None)
    try:
        if payload['function']:
            directory = os.path.dirname(script)
            parts = [] if os.path.basename(script) == '__init__.py' else [os.path.splitext(os.path.basename(script))[0]]
            while os.path.isfile(os.path.join(directory, '__init__.py')):
                parts.insert(0, os.path.basename(directory))
                directory = os.path.dirname(directory)
            if script.endswith('.py') and parts:
                sys.path.insert(0, directory)
                module = importlib.import_module('.'.join(parts))
            else:
                # Keep the globals alive for extensionless/pyw files on Python 2.
                module = types.ModuleType('__sandbox_target__')
                module.__file__ = script
                module.__package__ = None
                sys.modules[module.__name__] = module
                with open(script, 'rb') as stream:
                    code = compile(stream.read(), script, 'exec')
                eval(code, module.__dict__)
            namespace = module.__dict__
        else:
            namespace = runpy.run_path(script, run_name='__main__')
        value = None
        if payload['function']:
            target = namespace[payload['function'].split('.')[0]]
            for name in payload['function'].split('.')[1:]:
                target = getattr(target, name)
            value = target(*unpack_input(payload['args']), **unpack_input(payload['kwargs']))
    except BaseException as error:
        try:
            frames = [dict(file=f[0], line=f[1], function=f[2])
                      for f in traceback.extract_tb(sys.exc_info()[2])]
            result.update(status='exception', exception=dict(
                module=type(error).__module__, name=type(error).__name__,
                args=outcome_value(error.args), message=str(error), traceback=frames))
        except BaseException:
            result.update(status='capture_error', exception=None,
                          capture_error='could not serialize target exception')
    else:
        try:
            result['value'] = outcome_value(value)
        except (ValueError, TypeError) as error:
            result['status'] = 'capture_error'
            result['capture_error'] = str(error)
    # A capture failure must not masquerade as a legacy exception.
    with open('/scratch/outcome.json', 'w') as stream:
        json.dump(result, stream, sort_keys=True)


def stop_descendants():
    for name in os.listdir('/proc'):
        if name.isdigit() and int(name) != os.getpid():
            try:
                os.kill(int(name), signal.SIGKILL)
            except OSError:
                pass
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except OSError:
            break


def files_created(root, original):
    files = []
    total = 0
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in sorted(dirs + names):
            path = os.path.join(directory, name)
            relative = os.path.relpath(path, root)
            if relative in ('request.json', 'outcome.json', 'stdout', 'stderr'):
                continue
            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                files.append(dict(path=relative, kind='symlink', target=os.readlink(path)))
                if name in dirs:
                    dirs.remove(name)
            elif stat.S_ISREG(mode):
                with open(path, 'rb') as stream:
                    raw = stream.read(4 * MAX_CAPTURE + 1)
                digest = hashlib.sha256(raw).hexdigest()
                if original.get(relative) == digest:
                    continue
                total += len(raw)
                if total > MAX_CAPTURE:
                    raise ValueError('created files exceed capture limit')
                files.append(dict(path=relative, kind='file',
                                  sha256=digest,
                                  base64=base64.b64encode(raw).decode('ascii')))
            elif not stat.S_ISDIR(mode):
                raise ValueError('unsupported created file: ' + relative)
            if len(files) > 128:
                raise ValueError('created file count exceeds 128')
    return sorted(files, key=lambda f: f['path'])


def supervisor(payload):
    os.mkdir('/scratch/source')
    os.mkdir('/scratch/work')
    for name, encoded in sorted(payload['files'].items()):
        if not name or name.startswith('/') or any(p in ('', '.', '..') for p in name.split('/')):
            raise ValueError('invalid snapshot path')
        path = '/scratch/source/' + name
        parent = os.path.dirname(path)
        if not os.path.isdir(parent):
            os.makedirs(parent)
        with open(path, 'wb') as stream:
            stream.write(base64.b64decode(encoded))
    with open('/scratch/request.json', 'w') as stream:
        json.dump(payload, stream)
    with open('/scratch/stdout', 'wb') as stdout, open('/scratch/stderr', 'wb') as stderr:
        process = subprocess.Popen([sys.executable, '-B', '/sandbox_worker.py', '--child'],
                                   cwd='/scratch/work', stdout=stdout, stderr=stderr)
        deadline = time.time() + payload['timeout_seconds']
        timed_out = False
        while process.poll() is None:
            if time.time() >= deadline:
                timed_out = True
                process.kill()
                break
            time.sleep(0.01)
        process.wait()
    stop_descendants()
    result = dict(status='timeout' if timed_out else 'resource_limit',
                  value=None, exception=None, target_exit_code=process.returncode,
                  stdout_base64='', stderr_base64='', files=[], capture_error=None)
    if not timed_out and process.returncode == 0:
        with open('/scratch/outcome.json') as stream:
            result.update(json.load(stream))
    elif not timed_out and process.returncode > 0:
        result['status'] = 'infrastructure_error'
    try:
        for name in ('stdout', 'stderr'):
            with open('/scratch/' + name, 'rb') as stream:
                raw = stream.read(MAX_CAPTURE + 1)
            if len(raw) > MAX_CAPTURE:
                raise ValueError(name + ' exceeds capture limit')
            result[name + '_base64'] = base64.b64encode(raw).decode('ascii')
        original = dict(('source/' + name, hashlib.sha256(base64.b64decode(raw)).hexdigest())
                        for name, raw in payload['files'].items())
        result['files'] = files_created('/scratch', original)
    except (OSError, ValueError) as error:
        result['status'] = 'capture_error'
        result['capture_error'] = str(error)
    return result


if __name__ == '__main__':
    if '--child' in sys.argv:
        with open('/scratch/request.json') as stream:
            child(json.load(stream))
    else:
        print(json.dumps(supervisor(json.load(sys.stdin)), sort_keys=True))
