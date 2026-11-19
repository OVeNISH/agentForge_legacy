"""Trusted AST worker; compatible with Python 2.7. Never imports input code."""

from __future__ import print_function

import ast
import base64
import hashlib
import io
import json
import re
import sys
import tokenize


def expression(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return expression(node.value) + '.' + node.attr
    return ast.dump(node)


def argument(node):
    if isinstance(node, str):
        return node
    return getattr(node, 'arg', None) or expression(node)


class Facts(ast.NodeVisitor):
    def __init__(self, path):
        self.path = path
        self.scope = '<module>'
        self.functions = []
        self.classes = []
        self.imports = []
        self.calls = []
        self.symbols = []
        self.references = []
        self.effects = []

    def bind(self, name, kind, line, target=None):
        self.symbols.append(dict(scope=self.scope, name=name, kind=kind,
                                 line=line, target=target))

    def effect(self, kind, node, detail):
        item = dict(kind=kind, scope=self.scope, line=node.lineno, detail=detail)
        if item not in self.effects:
            self.effects.append(item)

    def visit_FunctionDef(self, node):
        qualified = node.name if self.scope == '<module>' else self.scope + '.' + node.name
        self.bind(node.name, 'function', node.lineno, qualified)
        args = node.args
        self.functions.append(dict(
            name=node.name, qualname=qualified, scope=self.scope, line=node.lineno,
            signature=dict(parameters=[argument(a) for a in args.args],
                           defaults=[expression(a) for a in args.defaults],
                           vararg=argument(args.vararg) if args.vararg else None,
                           kwarg=argument(args.kwarg) if args.kwarg else None),
            decorators=[expression(d) for d in node.decorator_list],
            docstring=ast.get_docstring(node)))
        # Defaults and decorators execute in the enclosing scope.
        for item in node.decorator_list + args.defaults:
            self.visit(item)
        previous = self.scope
        self.scope = qualified
        for arg in args.args:
            for item in ast.walk(arg):
                if isinstance(item, ast.Name) or hasattr(item, 'arg'):
                    self.bind(argument(item), 'parameter', node.lineno)
        for arg in (args.vararg, args.kwarg):
            if arg:
                self.bind(argument(arg), 'parameter', node.lineno)
        for item in node.body:
            self.visit(item)
        self.scope = previous

    def visit_ClassDef(self, node):
        qualified = node.name if self.scope == '<module>' else self.scope + '.' + node.name
        self.bind(node.name, 'class', node.lineno, qualified)
        self.classes.append(dict(name=node.name, qualname=qualified, scope=self.scope,
                                 line=node.lineno, bases=[expression(b) for b in node.bases],
                                 docstring=ast.get_docstring(node)))
        for item in node.bases + node.decorator_list:
            self.visit(item)
        previous = self.scope
        self.scope = qualified
        for item in node.body:
            self.visit(item)
        self.scope = previous

    def visit_Lambda(self, node):
        name = '<lambda@%s:%s>' % (node.lineno, node.col_offset)
        qualified = name if self.scope == '<module>' else self.scope + '.' + name
        args = node.args
        self.functions.append(dict(
            name=name, qualname=qualified, scope=self.scope, line=node.lineno,
            signature=dict(parameters=[argument(a) for a in args.args],
                           defaults=[expression(a) for a in args.defaults],
                           vararg=argument(args.vararg) if args.vararg else None,
                           kwarg=argument(args.kwarg) if args.kwarg else None),
            decorators=[], docstring=None))
        for item in args.defaults:
            self.visit(item)
        previous = self.scope
        self.scope = qualified
        for arg in args.args:
            for item in ast.walk(arg):
                if isinstance(item, ast.Name) or hasattr(item, 'arg'):
                    self.bind(argument(item), 'parameter', node.lineno)
        for arg in (args.vararg, args.kwarg):
            if arg:
                self.bind(argument(arg), 'parameter', node.lineno)
        self.visit(node.body)
        self.scope = previous

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split('.')[0]
            self.imports.append(dict(scope=self.scope, line=node.lineno,
                                     module=alias.name, name=None, alias=name, level=0))
            self.bind(name, 'import', node.lineno, alias.name if alias.asname else name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imports.append(dict(scope=self.scope, line=node.lineno,
                                     module=node.module or '', name=alias.name,
                                     alias=name, level=node.level))
            target = '.' * node.level + (node.module or '') + '.' + alias.name
            self.bind(name, 'import', node.lineno, target)

    def visit_Name(self, node):
        self.references.append(dict(scope=self.scope, name=node.id, line=node.lineno,
                                    column=node.col_offset, context=type(node.ctx).__name__))
        if isinstance(node.ctx, ast.Store):
            self.bind(node.id, 'variable', node.lineno)

    def visit_Attribute(self, node):
        self.references.append(dict(scope=self.scope, name=expression(node),
                                    line=node.lineno, column=node.col_offset,
                                    context=type(node.ctx).__name__))
        self.generic_visit(node)

    def visit_Call(self, node):
        self.calls.append(dict(scope=self.scope, line=node.lineno,
                               callee=expression(node.func)))
        self.generic_visit(node)

    def visit_Assign(self, node):
        mutable = isinstance(node.value, (ast.List, ast.Dict, ast.Set, ast.ListComp,
                                          ast.DictComp, ast.SetComp))
        # Unknown constructor results may be mutable; this is a conservative marker.
        mutable = mutable or isinstance(node.value, ast.Call)
        mutable = mutable or any(isinstance(t, (ast.Subscript, ast.Attribute)) for t in node.targets)
        if self.scope == '<module>' and mutable:
            self.effect('global_mutable', node, ', '.join(expression(t) for t in node.targets))
        self.generic_visit(node)

    def visit_Global(self, node):
        for name in node.names:
            self.bind(name, 'global', node.lineno)
        self.effect('global_mutable', node, 'global ' + ', '.join(node.names))


def parse_file(item):
    path, encoded = item
    raw = base64.b64decode(encoded)
    tree = ast.parse(raw, filename=path)
    facts = Facts(path)
    facts.visit(tree)
    encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'ascii'
    for line in raw.splitlines()[:2]:
        match = re.search(br'coding[:=]\s*([-\w.]+)', line)
        if match:
            encoding = match.group(1).decode('ascii')
    text = raw.decode(encoding)
    comments = [dict(line=start[0], column=start[1], text=token)
                for kind, token, start, end, source in
                tokenize.generate_tokens(io.StringIO(text).readline)
                if kind == tokenize.COMMENT]
    return dict(path=path, sha256=hashlib.sha256(raw).hexdigest(),
                functions=facts.functions, classes=facts.classes,
                comments=comments, imports=facts.imports, calls=facts.calls,
                symbols=facts.symbols, references=facts.references,
                side_effects=facts.effects, docstring=ast.get_docstring(tree))


def main():
    payload = json.load(sys.stdin)
    items = sorted(payload['files'].items())
    files = [parse_file(item) for item in items]
    print(json.dumps(files, sort_keys=True))


if __name__ == '__main__':
    main()
