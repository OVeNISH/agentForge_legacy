"""Trusted Python 2 parser/editor; executed inside SandboxRunner, never on host source."""

import ast
import base64
import copy
import json
from StringIO import StringIO
import tokenize

ROOT = '/scratch/source/'


def definitions(tree):
    found = {'<module>': tree}

    def walk(body, scope=''):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                name = scope + '.' + node.name if scope else node.name
                found[name] = node
                walk(node.body, name)
    walk(tree.body)
    return found


def without_docs(tree):
    tree = copy.deepcopy(tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Str):
                node.body.pop(0)
    return ast.dump(tree)


def annotate(source, docs):
    tree = ast.parse(source)
    nodes = definitions(tree)
    lines = source.splitlines(True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    tokens = list(tokenize.generate_tokens(StringIO(source).readline))
    edits, omitted = [], {}
    for name, text in sorted(docs.items()):
        if name not in nodes:
            raise ValueError('documentation target does not exist: ' + name)
        if not text.startswith('[Machine-generated]'):
            raise ValueError('missing generated-text marker')
        node = nodes[name]
        first = node.body[0] if node.body else None
        if first is not None and isinstance(first, ast.Expr) and isinstance(first.value, ast.Str):
            candidates = [t for t in tokens if t[0] == tokenize.STRING and
                          t[2][0] <= first.lineno <= t[3][0] and ast.literal_eval(t[1]) == first.value.s]
            if len(candidates) != 1:
                omitted[name] = 'ambiguous existing string tokens; generated documentation retained in sidecar only'
                continue
            token = candidates[0]
            start, end = token[2], token[3]
            edits.append((offsets[start[0]-1] + start[1], offsets[end[0]-1] + end[1], repr(text)))
        elif first is not None and getattr(node, 'lineno', 0) == first.lineno:
            omitted[name] = 'inline suite needs source restructuring; docstring retained in sidecar only'
        else:
            line = min([first.lineno] + [d.lineno for d in getattr(first, 'decorator_list', [])]) if first else len(lines) + 1
            indentation = lines[line-1][:len(lines[line-1])-len(lines[line-1].lstrip())] if first else ''
            position = offsets[line-1]
            edits.append((position, position, indentation + repr(text) + '\n'))
    for start, end, text in sorted(edits, reverse=True):
        source = source[:start] + text + source[end:]
    changed = ast.parse(source)
    compile(changed, '<documented>', 'exec')
    if without_docs(tree) != without_docs(changed):
        raise ValueError('documentation changed executable AST')
    for name, text in docs.items():
        if name not in omitted and ast.get_docstring(definitions(changed)[name], clean=False) != text:
            raise ValueError('docstring insertion mismatch: ' + name)
    return dict(source_base64=base64.b64encode(source), omitted=omitted,
                ast_equivalent=True, compiled=True)


def run(documents):
    results = {}
    for path, docs in sorted(documents.items()):
        if path.startswith('/') or '..' in path.split('/'):
            raise ValueError('unsafe source path')
        with open(ROOT + path, 'rb') as stream:
            results[path] = annotate(stream.read(), docs)
    return json.dumps(results, sort_keys=True)


def self_check():
    text = u'[Machine-generated]\nQuotes: " \' and \\n; snow: \u96ea'
    sources = [
        ('# keep\ndef f(\n    value=1):\n    # keep too\n    return value\n', 'f'),
        ('def f():\n    """old\n    docs"""\n    return 1\n', 'f'),
        ('class C:\n    @staticmethod\n    def f():\n        return 1\n', 'C'),
        ('"old module"\nx = 1\n', '<module>'),
    ]
    for source, name in sources:
        result = annotate(source, {name: text})
        assert result['ast_equivalent'] and result['compiled'] and not result['omitted']
        assert ast.get_docstring(definitions(ast.parse(base64.b64decode(result['source_base64'])))[name], clean=False) == text
    assert annotate('def f(): return 1\n', {'f': text})['omitted']['f']
    try:
        annotate('x = 1\n', {'missing': text})
    except ValueError:
        pass
    else:
        raise AssertionError('unknown target accepted')
    return json.dumps(dict(passed=True, checks=['multiline signature/comments', 'existing multiline docstring',
        'class/decorator', 'module', 'quotes/unicode', 'inline omission', 'unknown target rejection']))
