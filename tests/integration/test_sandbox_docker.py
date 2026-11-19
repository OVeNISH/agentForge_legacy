"""Opt-in live isolation tests; records are generated from actual Docker runs."""

import base64
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from modernize.config import Config
from modernize.sandbox import Limits, SandboxRunner

ROOT = Path(__file__).resolve().parents[2]
PROBE = b'''import os
import socket
import time

def deterministic(raw, text):
    os.write(1, raw)
    os.write(2, b'error stream\\n')
    with open('created.bin', 'wb') as stream:
        stream.write(raw)
    return {'raw': raw, 'text': text, 'tuple': (1, True, None)}

def exception():
    raise ValueError('probe exception')

def network():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect(('198.51.100.1', 9))

def filesystem():
    errors = []
    for path in ('/outside-cp3', '/tmp/outside-cp3', '/sandbox_worker.py'):
        try:
            with open(path, 'wb') as stream:
                stream.write(b'forbidden')
        except IOError as error:
            errors.append(error.errno)
    with open('/scratch/allowed.bin', 'wb') as stream:
        stream.write(b'allowed')
    os.symlink('/etc/passwd', 'link')
    return os.getuid(), errors

def fresh():
    return os.path.exists('/scratch/allowed.bin')

def sleep():
    os.write(1, b'partial output\\n')
    with open('before-timeout', 'wb') as stream:
        stream.write(b'partial file')
    time.sleep(60)

def cpu():
    while True:
        pass

def memory():
    return bytearray(512 * 1024 * 1024)

def unsupported():
    return object()

def exit_without_outcome():
    os._exit(0)
'''

TEST_SCRIPT = b'''import unittest
class IsolationTest(unittest.TestCase):
    def test_root_is_read_only(self):
        with self.assertRaises(IOError):
            open('/outside-test', 'wb')
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IsolationTest))
if not result.wasSuccessful():
    raise SystemExit(1)
'''


@unittest.skipUnless(os.environ.get('MODERNIZE_DOCKER_TESTS') == '1', 'live Docker tests require MODERNIZE_DOCKER_TESTS=1')
class DockerSandboxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.project = Path(cls.directory.name)
        (cls.project / 'probe.py').write_bytes(PROBE)
        (cls.project / 'tests.py').write_bytes(TEST_SCRIPT)
        (cls.project / 'package').mkdir()
        (cls.project / 'package/__init__.py').write_bytes(b'from .helper import echo\n')
        (cls.project / 'package/helper.py').write_bytes(b'def echo(value):\n    return value\n')
        cls.records = []
        config = Config()
        cls.images = (config.legacy_image, config.modern_image)

    @classmethod
    def tearDownClass(cls):
        modules = ['sandbox.py', 'sandbox_worker.py', 'sandbox_codec.py']
        evidence = dict(records=cls.records, implementation_sha256={
            'src/modernize/' + name: hashlib.sha256((ROOT / 'src/modernize' / name).read_bytes()).hexdigest()
            for name in modules}, probe_base64=base64.b64encode(PROBE).decode(),
            test_script_base64=base64.b64encode(TEST_SCRIPT).decode())
        path = ROOT / 'artifacts/cp3-live.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(evidence, sort_keys=True, indent=2) + '\n')
        cls.directory.cleanup()

    def run_probe(self, image, function, limits=None, args=()):
        record = SandboxRunner(image, limits).run(self.project, 'probe.py', function, args=args)
        self.records.append(dict(case=function, image=image, record=record))
        self.assertTrue(record['container_removed'])
        self.assertIsNone(record['protocol_error'], record)
        self.assertFalse(record['container_state']['Running'])
        isolation = record['isolation']
        self.assertEqual(isolation['NetworkMode'], 'none')
        self.assertTrue(isolation['ReadonlyRootfs'])
        self.assertEqual(isolation['User'], '65534:65534')
        self.assertEqual(isolation['Memory'], (limits or Limits()).memory_mb * 1024 * 1024)
        self.assertEqual(isolation['Memory'], isolation['MemorySwap'])
        self.assertEqual(isolation['NanoCpus'], 1000000000)
        self.assertEqual(isolation['PidsLimit'], 32)
        self.assertEqual(isolation['LogConfig']['Type'], 'none')
        self.assertIn('ALL', isolation['CapDrop'])
        self.assertTrue(any(s.startswith('no-new-privileges') for s in isolation['SecurityOpt']))
        self.assertTrue(all(m['type'] == 'tmpfs' or (m['type'] == 'bind' and not m['rw'])
                            for m in isolation['Mounts']))
        self.assertEqual(hashlib.sha256((self.project / 'probe.py').read_bytes()).hexdigest(),
                         record['source_sha256']['probe.py'])
        return record['result']

    def test_deterministic_values_streams_and_files(self):
        for image in self.images:
            with self.subTest(image=image):
                first = self.run_probe(image, 'deterministic', args=(b'\x00\xff\n', 'caf\u00e9'))
                second = self.run_probe(image, 'deterministic', args=(b'\x00\xff\n', 'caf\u00e9'))
                self.assertEqual(first, second)
                self.assertEqual(first['status'], 'completed')
                self.assertEqual(base64.b64decode(first['stdout_base64']), b'\x00\xff\n')
                self.assertEqual(base64.b64decode(first['stderr_base64']), b'error stream\n')
                self.assertEqual(base64.b64decode(first['files'][0]['base64']), b'\x00\xff\n')

    def test_network_call_is_denied(self):
        for image in self.images:
            with self.subTest(image=image):
                result = self.run_probe(image, 'network')
                self.assertEqual(result['status'], 'exception')
                self.assertIn(result['exception']['name'], ('error', 'OSError'))
                self.assertIn(result['exception']['args']['items'][0]['value'], ('101', '113'))

    def test_filesystem_protection_and_discard(self):
        for image in self.images:
            with self.subTest(image=image):
                result = self.run_probe(image, 'filesystem')
                self.assertEqual(result['status'], 'completed')
                uid, errors = result['value']['items']
                self.assertEqual(uid['value'], '65534')
                self.assertEqual([v['value'] for v in errors['items']], ['30', '30', '30'])
                self.assertEqual([f['path'] for f in result['files']], ['allowed.bin', 'work/link'])
                self.assertEqual(result['files'][1]['kind'], 'symlink')
                self.assertEqual(self.run_probe(image, 'fresh')['value'], {'type': 'bool', 'value': False})

    def test_wall_timeout_keeps_partial_capture(self):
        for image in self.images:
            with self.subTest(image=image):
                result = self.run_probe(image, 'sleep', Limits(timeout_seconds=0.2))
                self.assertEqual(result['status'], 'timeout')
                self.assertEqual(result['target_exit_code'], -9)
                self.assertEqual(base64.b64decode(result['stdout_base64']), b'partial output\n')
                self.assertEqual(result['files'][0]['path'], 'work/before-timeout')

    def test_cpu_limit_stops_a_runaway_loop(self):
        for image in self.images:
            with self.subTest(image=image):
                result = self.run_probe(image, 'cpu', Limits(timeout_seconds=5, cpu_seconds=1))
                self.assertEqual(result['status'], 'resource_limit')
                self.assertEqual(result['target_exit_code'], -9)

    def test_excessive_memory_request_is_stopped(self):
        for image in self.images:
            with self.subTest(image=image):
                result = self.run_probe(image, 'memory', Limits(memory_mb=64))
                self.assertEqual(result['status'], 'exception')
                self.assertEqual(result['exception']['name'], 'MemoryError')

    def test_exceptions_and_unsupported_returns(self):
        for image in self.images:
            with self.subTest(image=image):
                result = self.run_probe(image, 'exception')
                self.assertEqual(result['exception']['name'], 'ValueError')
                self.assertTrue(result['exception']['traceback'])
                unsupported = self.run_probe(image, 'unsupported')
                self.assertEqual(unsupported['status'], 'capture_error')
                self.assertIn('unsupported return', unsupported['capture_error'])

    def test_supplied_test_script_runs_in_both_runtimes(self):
        for image in self.images:
            with self.subTest(image=image):
                record = SandboxRunner(image).run_tests(self.project, 'tests.py')
                self.records.append(dict(case='supplied_tests', image=image, record=record))
                self.assertIsNone(record['protocol_error'], record)
                self.assertEqual(record['result']['status'], 'completed')
                self.assertIn(b'Ran 1 test', base64.b64decode(record['result']['stderr_base64']))

    def test_package_relative_imports_keep_function_globals(self):
        for image in self.images:
            with self.subTest(image=image):
                record = SandboxRunner(image).run(self.project, 'package/__init__.py', 'echo', args=(123,))
                self.records.append(dict(case='relative_import', image=image, record=record))
                self.assertIsNone(record['protocol_error'], record)
                self.assertEqual(record['result']['status'], 'completed')
                self.assertEqual(record['result']['value'], {'type': 'int', 'value': '123'})

    def test_bypassed_outcome_is_reported_as_protocol_failure(self):
        for image in self.images:
            with self.subTest(image=image):
                record = SandboxRunner(image).run(self.project, 'probe.py', 'exit_without_outcome')
                self.records.append(dict(case='missing_outcome', image=image, record=record))
                self.assertTrue(record['container_removed'])
                self.assertIsNone(record['result'])
                self.assertTrue(record['protocol_error'])
