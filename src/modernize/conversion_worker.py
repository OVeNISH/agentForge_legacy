"""Deterministic Python 2 syntax conversion, run only in the legacy sandbox."""

import ast
import base64
import json
from lib2to3.refactor import RefactoringTool
from lib2to3.fixer_util import touch_import
from lib2to3.pygram import python_symbols as symbols
from lib2to3.pgen2 import token

FIXERS = ['print', 'except', 'dict', 'map', 'filter', 'zip', 'xrange',
          'has_key', 'ne', 'numliterals', 'repr', 'raise', 'exec', 'tuple_params']


def mechanical(source, path):
    original = ast.parse(source, filename=path)
    tool = RefactoringTool(['lib2to3.fixes.fix_' + name for name in FIXERS])
    current = source if source.endswith('\n') else source + '\n'
    # Shipped fixers can expose another rule site (e.g. iteritems -> iter(items)).
    for iteration in range(4):
        converted = tool.refactor_string(current, path)
        if any(isinstance(node, ast.Print) for node in ast.walk(original)):
            touch_import('__future__', 'print_function', converted)
            future = next(node for node in converted.children if node.type == symbols.simple_stmt and
                node.children[0].type == symbols.import_from and
                node.children[0].children[1].value == '__future__' and
                'print_function' in [leaf.value for leaf in node.leaves()])
            future.remove()
            first = converted.children[0]
            index = 1 if first.type == symbols.simple_stmt and first.children[0].type == token.STRING else 0
            if index == 0:
                future.prefix, first.prefix = first.prefix, ''
            converted.insert_child(index, future)
        result = str(converted)
        if result == current:
            return result
        current = result
    raise ValueError('mechanical conversion did not stabilize within four passes')


def run(paths):
    result = {}
    for path in paths:
        if path.startswith('/') or '..' in path.split('/'):
            raise ValueError('unsafe source path')
        with open('/scratch/source/' + path, 'rb') as stream:
            source = stream.read()
        result[path] = base64.b64encode(mechanical(source, path))
    return json.dumps(dict(files=result, fixers=FIXERS), sort_keys=True)


def self_check():
    source = ('def f(values):\n    print values\n    try:\n        return '
              'map(str, values), filter(None, values), zip(values, values), values.iteritems()\n'
              '    except ValueError, error:\n        raise error\n')
    result = mechanical(source, 'probe.py')
    assert 'print(values)' in result and 'except ValueError as error:' in result
    assert '.items()' in result and 'list(zip(' in result
    repeated = mechanical(result, 'probe.py')
    assert repeated == result, repr((result, repeated))
    text = mechanical("label = u'caf\\u00e9'\nratio = a / b\n", 'semantic.py')
    assert "u'caf\\u00e9'" in text and 'a / b' in text
    compile(mechanical("u'docs'\nimport os\nprint 'hello'\n", 'imports.py'), 'imports.py', 'exec')
    return json.dumps(dict(passed=True, checks=['syntax/dict/iterators', 'idempotence',
        'unicode and division deferred to semantic stage', 'future import precedes ordinary imports']))
