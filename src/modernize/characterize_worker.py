"""Trusted Python 2/3 observation harness, executed only inside SandboxRunner."""

import ast
import base64
import importlib
import json
import os
import sys

from sandbox_codec import outcome_value

ROOT = '/scratch/source/'


def inventory(paths):
    functions, lines, branches, exclusions = [], set(), set(), []
    for path in paths:
        with open(ROOT + path, 'rb') as stream:
            tree = ast.parse(stream.read(), filename=path)

        def statements(body, successor, function_line):
            for index, node in enumerate(body):
                following = body[index + 1].lineno if index + 1 < len(body) else successor
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    continue
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                    continue
                lines.add('%s:%s' % (path, node.lineno))
                if isinstance(node, (ast.If, ast.For, ast.While)):
                    yes = node.body[0].lineno
                    no = node.orelse[0].lineno if node.orelse else following
                    branches.update('%s:%s:%s' % (path, node.lineno, end) for end in (yes, no))
                for field in ('body', 'orelse', 'finalbody'):
                    children = getattr(node, field, [])
                    if children:
                        end = node.lineno if isinstance(node, (ast.For, ast.While)) and field == 'body' else following
                        statements(children, end, function_line)
                for handler in getattr(node, 'handlers', []):
                    # The except header itself does not always emit a line event.
                    statements(handler.body, following, function_line)

        def definitions(body, scope=''):
            for node in body:
                if isinstance(node, ast.ClassDef):
                    definitions(node.body, node.name)
                elif isinstance(node, ast.FunctionDef):
                    name = scope + '.' + node.name if scope else node.name
                    functions.append(dict(path=path, target=name, line=node.lineno,
                                          signature=ast.dump(node.args)))
                    statements(node.body, -node.lineno, node.lineno)
                    for child in ast.walk(node):
                        if isinstance(child, (ast.Lambda, ast.FunctionDef)) and child is not node:
                            exclusions.append(dict(path=path, line=child.lineno,
                                reason='nested callable exercised through enclosing function; not independently addressable'))
        definitions(tree.body)
    return dict(functions=functions, lines=sorted(lines), branches=sorted(branches), exclusions=exclusions)


def decode(value):
    if isinstance(value, dict):
        if set(value) == set(['$bytes']):
            return base64.b64decode(value['$bytes'])
        return dict((k, decode(v)) for k, v in value.items())
    if isinstance(value, list):
        return [decode(v) for v in value]
    return value


def observe(case):
    lines, arcs, previous = set(), set(), {}

    def trace(frame, event, arg):
        filename = frame.f_code.co_filename
        if filename.startswith(ROOT) and not filename.endswith('/__cp5__.py'):
            path = filename[len(ROOT):]
            key = id(frame)
            if event in ('line', 'return'):
                line = frame.f_lineno if event == 'line' else -frame.f_code.co_firstlineno
                if event == 'line':
                    lines.add('%s:%s' % (path, line))
                if key in previous:
                    arcs.add('%s:%s:%s' % (path, previous[key], line))
                previous[key] = line
                if event == 'return':
                    previous.pop(key, None)
        return trace

    for path, raw in json.loads(case['files_json']).items():
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)
        with open(path, 'wb') as stream:
            stream.write(base64.b64decode(raw))
    sys.settrace(trace)
    try:
        path = case['path']
        module = path[:-3].replace('/', '.')
        if module.endswith('.__init__'):
            module = module[:-9]
        target = importlib.import_module(module)
        names = case['target'].split('.')
        instance = None
        if len(names) == 2:
            cls = getattr(target, names[0])
            # __init__ is called exactly once and its resulting state is observed.
            if names[1] == '__init__':
                instance = cls(*decode(json.loads(case['args_json'])),
                               **decode(json.loads(case['kwargs_json'])))
                value = None
            else:
                instance = cls()
                for call in json.loads(case['setup_json']):
                    getattr(instance, call['method'])(*decode(call['args']), **decode(call['kwargs']))
                value = getattr(instance, names[1])(*decode(json.loads(case['args_json'])),
                                                   **decode(json.loads(case['kwargs_json'])))
        else:
            value = getattr(target, names[0])(*decode(json.loads(case['args_json'])),
                                              **decode(json.loads(case['kwargs_json'])))
    except BaseException as error:
        result = dict(status='exception', module=type(error).__module__, name=type(error).__name__,
                      args=outcome_value(error.args), message=str(error))
    else:
        result = dict(status='completed', value=outcome_value(value),
                      state=outcome_value(instance.__dict__) if instance is not None else None)
    finally:
        sys.settrace(None)
    return dict(outcome=result, lines=sorted(lines), branches=sorted(arcs))


def run(operation, value):
    result = inventory(value) if operation == 'inventory' else observe(value)
    return json.dumps(result, sort_keys=True, ensure_ascii=True)
