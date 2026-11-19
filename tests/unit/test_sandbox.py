import base64
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from modernize.sandbox import Limits, SandboxRunner, bounded_start, snapshot, validate_result
from modernize.sandbox_codec import pack_input, unpack_input, outcome_value


class SandboxTests(unittest.TestCase):
    def test_limits_and_input_boundaries(self):
        for values in ({'timeout_seconds': 0}, {'cpu_seconds': True}, {'memory_mb': 1}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                Limits(**values)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'main.py').write_bytes(b'pass\n')
            (root / 'data.bin').write_bytes(b'\x00\xff')
            self.assertEqual(snapshot(root)['data.bin'], b'\x00\xff')
            with patch('modernize.sandbox.subprocess.run') as docker:
                for options in ({'script': '../main.py'}, {'script': 'main.py', 'kwargs': []},
                                {'script': 'main.py', 'function': 'f()'}):
                    with self.subTest(options=options), self.assertRaises(ValueError):
                        SandboxRunner('legacy').run(root, **options)
                docker.assert_not_called()
            (root / 'link').symlink_to('/tmp')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                snapshot(root)

    def test_input_values_round_trip_and_output_types_are_retained(self):
        values = (b'\x00\xff', 'caf\u00e9', [1, True, None], {2: ('x',)})
        self.assertEqual(unpack_input(pack_input(values)), values)
        self.assertEqual(outcome_value(b'\xff'), {'type': 'bytes', 'base64': '/w=='})
        self.assertEqual(outcome_value('x'), {'type': 'str', 'value': 'x'})
        self.assertNotEqual(outcome_value([1]), outcome_value((1,)))
        with self.assertRaisesRegex(ValueError, 'unsupported return'):
            outcome_value(object())
        loop = []
        loop.append(loop)
        with self.assertRaisesRegex(ValueError, 'nesting'):
            outcome_value(loop)
        with self.assertRaisesRegex(ValueError, 'nesting'):
            pack_input(loop)

    def test_schema_validates_bytes_hashes_and_typed_values(self):
        result = dict(status='completed', value=outcome_value(3), exception=None,
                      target_exit_code=0, stdout_base64='', stderr_base64='',
                      files=[dict(path='work/data', kind='file', base64='YQ==',
                                  sha256=hashlib.sha256(b'a').hexdigest())], capture_error=None)
        validate_result(result)
        for kind in ('unknown_type', 'path_escape', 'wrong_hash', 'missing_field'):
            broken = deepcopy(result)
            if kind == 'unknown_type':
                broken['value'] = {'type': 'invented', 'value': 3}
            elif kind == 'path_escape':
                broken['files'][0]['path'] = '../data'
            elif kind == 'wrong_hash':
                broken['files'][0]['sha256'] = 'wrong'
            else:
                del broken['stdout_base64']
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                validate_result(broken)

    def test_docker_wire_output_is_bounded(self):
        with patch('modernize.sandbox.MAX_WIRE', 1024):
            output, error, code, failure = bounded_start(
                [sys.executable, '-c', 'import sys; sys.stdout.write("x" * 8192)'], b'', 2)
        self.assertEqual(len(output), 1024)
        self.assertEqual(failure, 'wire_capture_limit')

    def test_declared_image_volumes_are_rejected_before_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'main.py').write_text('pass\n')
            metadata = [dict(Id='sha256:' + 'a' * 64, Os='linux', Config={'Volumes': {'/data': {}}})]
            process = subprocess.CompletedProcess([], 0, json.dumps(metadata), '')
            with patch('modernize.sandbox.subprocess.run', return_value=process) as docker:
                with self.assertRaisesRegex(ValueError, 'volumes'):
                    SandboxRunner('image').run(directory, 'main.py')
                self.assertEqual(docker.call_count, 1)

    def test_protocol_errors_still_remove_container_and_cleanup_errors_surface(self):
        image = dict(Id='sha256:' + 'a' * 64, Os='linux', Config={})
        state = dict(HostConfig=dict(NetworkMode='none', ReadonlyRootfs=True,
                     Memory=134217728, MemorySwap=134217728, NanoCpus=1000000000,
                     PidsLimit=32, CapDrop=['ALL'], SecurityOpt=['no-new-privileges'], LogConfig={'Type': 'none'}),
                     State=dict(Running=False, OOMKilled=False), Config={'User': '65534:65534'}, Mounts=[])
        def process(code=0, output='', error=''):
            return subprocess.CompletedProcess([], code, output, error)
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'main.py').write_text('pass\n')
            for cleanup_fails in (False, True):
                commands = [process(output=json.dumps([image])), process(output='container-id'),
                            process(output=json.dumps([state])),
                            process(1, error='daemon unavailable') if cleanup_fails else process()]
                with patch('modernize.sandbox.subprocess.run', side_effect=commands) as docker, \
                        patch('modernize.sandbox.bounded_start', return_value=(b'bad json', b'', 0, None)):
                    if cleanup_fails:
                        with self.assertRaisesRegex(ValueError, 'cleanup failed'):
                            SandboxRunner('image').run(directory, 'main.py')
                    else:
                        record = SandboxRunner('image').run(directory, 'main.py')
                        self.assertIsNone(record['result'])
                        self.assertTrue(record['protocol_error'])
                        self.assertTrue(record['container_removed'])
                    self.assertEqual(docker.call_args.args[0][:3], ['docker', 'rm', '-f'])
