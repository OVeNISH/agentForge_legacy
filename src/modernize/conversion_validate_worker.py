"""Compile, index and import converted code only inside the modern sandbox."""

import ast
import importlib
import json


def run(paths):
    facts = []
    for path in paths:
        if path.startswith('/') or '..' in path.split('/'):
            raise ValueError('unsafe source path')
        with open('/scratch/source/' + path, 'rb') as stream:
            tree = ast.parse(stream.read(), filename=path)
        compile(tree, path, 'exec')
        definitions = []

        def walk(body, scope=''):
            for node in body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    name = scope + '.' + node.name if scope else node.name
                    definition = dict(name=name, kind=type(node).__name__)
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        definition['signature'] = dict(
                            parameters=[a.arg for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs],
                            defaults=len(node.args.defaults) + len(node.args.kw_defaults),
                            vararg=node.args.vararg.arg if node.args.vararg else None,
                            kwarg=node.args.kwarg.arg if node.args.kwarg else None)
                    definitions.append(definition)
                    walk(node.body, name)
        walk(tree.body)
        facts.append(dict(path=path, compiled=True, definitions=definitions,
            imports=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]))
    for fact in facts:
        module = fact['path'][:-3].replace('/', '.')
        if module.endswith('.__init__'):
            module = module[:-9]
        importlib.import_module(module)
        fact['imported'] = True
    return json.dumps(dict(files=facts), sort_keys=True)
