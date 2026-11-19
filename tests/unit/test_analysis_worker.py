"""Fact extraction tests runnable under both Python 2.7 and Python 3.12."""

import base64
import sys
import unittest

from modernize.analyzer_worker import parse_file


def facts(source):
    return parse_file(('fixture.py', base64.b64encode(source).decode('ascii')))


class WorkerTests(unittest.TestCase):
    def test_functions_classes_signatures_and_docstrings(self):
        result = facts(b'''"""module docs"""
class Box(object):
    """box docs"""
    def method(self, value=3, *args, **kwargs):
        """method docs"""
        return value
''')
        self.assertEqual(result['docstring'], 'module docs')
        self.assertEqual(result['classes'][0]['bases'], ['object'])
        self.assertEqual(result['classes'][0]['docstring'], 'box docs')
        fn = result['functions'][0]
        self.assertEqual(fn['qualname'], 'Box.method')
        self.assertEqual(fn['signature']['parameters'], ['self', 'value'])
        self.assertEqual(fn['signature']['vararg'], 'args')
        self.assertEqual(fn['signature']['kwarg'], 'kwargs')
        self.assertEqual(len(fn['signature']['defaults']), 1)
        self.assertEqual(fn['docstring'], 'method docs')

    def test_comments_and_encoding(self):
        result = facts(b'# coding: latin-1\n# caf\xe9\nx = "# not a comment"\n')
        self.assertEqual(result['comments'][1]['text'], u'# caf\xe9')
        self.assertEqual(result['comments'][1]['line'], 2)
        self.assertEqual(len(result['comments']), 2)

    def test_imports_calls_scopes_and_references(self):
        result = facts(b'''import os as system
from .util import helper as h
def outer(x):
    def inner(y):
        return h(y)
    return inner(x)
''')
        self.assertEqual(result['imports'][0]['alias'], 'system')
        self.assertEqual(result['imports'][1]['level'], 1)
        self.assertEqual(result['calls'][0]['scope'], 'outer.inner')
        self.assertEqual(result['calls'][0]['callee'], 'h')
        self.assertTrue(any(r['name'] == 'y' for r in result['references']))
        self.assertTrue(any(s['kind'] == 'parameter' and s['scope'] == 'outer.inner'
                            for s in result['symbols']))

    def test_global_mutable_markers(self):
        result = facts(b'cache = {}\ndef reset():\n    global cache\n    cache = []\n')
        self.assertEqual([e['kind'] for e in result['side_effects']],
                         ['global_mutable', 'global_mutable'])

    def test_lambda_parameters_have_a_separate_scope(self):
        result = facts(b'f = lambda value=3: value\n')
        fn = result['functions'][0]
        self.assertTrue(fn['name'].startswith('<lambda@'))
        self.assertEqual(fn['signature']['parameters'], ['value'])
        self.assertEqual(result['references'][-1]['scope'], fn['qualname'])

    def test_parsing_does_not_execute_code(self):
        result = facts(b'raise RuntimeError("must never execute")\n')
        self.assertEqual(result['functions'], [])

    def test_invalid_source_is_not_skipped(self):
        self.assertRaises(SyntaxError, facts, b'def broken(:\n')

    def test_python2_specific_nodes(self):
        if sys.version_info[0] != 2:
            self.skipTest('requires the recorded Python 2.7 worker test run')
        result = facts(b'def f((a, b), *rest):\n    try:\n        print a\n    except ValueError, err:\n        return b\n')
        self.assertEqual(result['functions'][0]['signature']['vararg'], 'rest')
        self.assertEqual(len(result['functions'][0]['signature']['parameters']), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
