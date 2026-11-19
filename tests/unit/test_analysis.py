import base64
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from modernize.analysis import inventory, project_index, Python2Adapter, scan
from modernize.analyzer_worker import parse_file
from modernize.facts_schema import FILE, validate, validate_files


def parsed(path, source):
    return parse_file((path, base64.b64encode(source).decode('ascii')))


class AnalysisTests(unittest.TestCase):
    def test_inventory_extensions_exclusions_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'main.py').write_bytes(b'pass\n')
            (root / 'tool').write_bytes(b'#!/usr/bin/env python2\npass\n')
            (root / 'asset.txt').write_text('asset')
            (root / '.git').mkdir()
            (root / '.git' / 'ignored.py').write_text('broken syntax')
            sources, excluded, unsupported = inventory(root)
            self.assertEqual(list(sources), ['main.py', 'tool'])
            self.assertEqual(excluded, ['.git'])
            self.assertEqual(unsupported, ['asset.txt'])
            (root / 'escape.py').symlink_to('/tmp')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                inventory(root)

    def test_schema_rejects_missing_extra_and_wrong_types(self):
        file = parsed('main.py', b'def f():\n    pass\n')
        validate([file], [FILE])
        for mutation in ('missing', 'extra', 'wrong_type'):
            broken = deepcopy(file)
            if mutation == 'missing':
                del broken['imports']
            elif mutation == 'extra':
                broken['surprise'] = 1
            else:
                broken['functions'][0]['line'] = True
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate([broken], [FILE])

    def test_schema_rejects_invalid_positions_and_marker_kinds(self):
        file = parsed('main.py', b'cache = []\n')
        for key, value in (('line', 0), ('kind', 'invented')):
            broken = deepcopy(file)
            broken['side_effects'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_files([broken])

    def test_cross_file_import_call_graph_and_shadowing(self):
        files = [parsed('pkg/__init__.py', b'from .util import helper\n'),
                 parsed('pkg/util.py', b'def helper(x):\n    return x\n'),
                 parsed('main.py', b'''from pkg import helper as h
def run(x):
    return h(x)
def shadow(h):
    return h(1)
''')]
        index = project_index(files)
        self.assertEqual(index['imports'][0]['target'], 'pkg/util.py')
        self.assertEqual(index['calls'][0]['target'], 'pkg/util.py::helper')
        self.assertIsNone(index['calls'][1]['target'])
        shadow_ref = [r for r in index['references'] if r['scope'] == 'shadow' and r['name'] == 'h'][0]
        self.assertEqual(shadow_ref['binding'], 'main.py::shadow::h')

    def test_side_effect_categories_with_aliases_and_shadowed_builtins(self):
        file = parsed('effects.py', b'''import os as system
import socket as net
import sqlite3 as db
from time import time as clock
from random import Random as rng
def work():
    open('data')
    net.socket()
    db.connect(':memory:')
    system.getenv('HOME')
    value = system.environ['HOME']
    clock()
    rng()
cache = []
def shadow(open):
    return open('not a file')
''')
        project_index([file])
        self.assertEqual({e['kind'] for e in file['side_effects']}, {
            'file_io', 'network', 'database', 'environment', 'time', 'randomness', 'global_mutable'})
        self.assertFalse(any(e['scope'] == 'shadow' for e in file['side_effects']))

    def test_method_cannot_resolve_a_class_local_as_a_lexical_variable(self):
        file = parsed('main.py', b'''def helper():
    pass
class Box:
    helper = 3
    def method(self):
        return helper()
''')
        self.assertEqual(project_index([file])['calls'][0]['target'], 'main.py::helper')

    def test_future_absolute_import_and_ambiguous_imports_remain_distinct(self):
        files = [parsed('pkg/sibling.py', b'def work():\n    pass\n'),
                 parsed('pkg/main.py', b'''from __future__ import absolute_import
import sibling
sibling.work()
import time as source
import random as source
source.random()
''')]
        index = project_index(files)
        self.assertIsNone(index['imports'][1]['target'])
        self.assertIsNone(index['calls'][0]['target'])
        self.assertIsNone(index['calls'][1]['resolved_name'])

    def test_adapter_validates_worker_and_snapshot(self):
        valid = parsed('main.py', b'pass\n')
        image = subprocess.CompletedProcess([], 0, 'sha256:test\n', '')
        for response in ('not json', '[]', json.dumps([dict(valid, sha256='wrong')])):
            process = subprocess.CompletedProcess([], 0, response, '')
            with patch('modernize.analysis.subprocess.run', side_effect=[image, process]):
                with self.assertRaises(ValueError):
                    Python2Adapter('legacy').parse({'main.py': b'pass\n'})

    def test_parse_failure_names_file_and_timeout_removes_container(self):
        image = subprocess.CompletedProcess([], 0, 'sha256:test\n', '')
        failed = subprocess.CompletedProcess([], 1, '', 'SyntaxError: broken')
        with patch('modernize.analysis.subprocess.run', side_effect=[image, failed]):
            with self.assertRaisesRegex(ValueError, 'main.py.*SyntaxError'):
                Python2Adapter('legacy').parse({'main.py': b'broken'})
        with patch('modernize.analysis.subprocess.run', side_effect=[
                image, subprocess.TimeoutExpired('docker', 30), failed]) as run:
            with self.assertRaisesRegex(ValueError, 'timed out'):
                Python2Adapter('legacy').parse({'main.py': b'pass'})
            self.assertEqual(run.call_args_list[-1].args[0][:3], ['docker', 'rm', '-f'])

    def test_sequential_and_parallel_merge_identically(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'b.py').write_bytes(b'def b():\n    pass\n')
            (root / 'a.py').write_bytes(b'from b import b\nb()\n')
            def fake_worker(item):
                return parsed(*item)
            image = subprocess.CompletedProcess([], 0, 'sha256:test\n', '')
            with patch('modernize.analysis.subprocess.run', return_value=image), \
                    patch.object(Python2Adapter, '_parse_one', side_effect=fake_worker):
                sequential = scan(root, Python2Adapter('legacy'))
                parallel = scan(root, Python2Adapter('legacy', 'parallel', 2))
            self.assertEqual(sequential, parallel)
