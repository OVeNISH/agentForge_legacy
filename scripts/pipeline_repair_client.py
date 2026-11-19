"""Recorded source-only repair; no fixtures or expected values are embedded."""

import json
import ast

from modernize.characterize import digest

from modernize.llm import LLMResponse, MockLLMClient, TokenUsage


def review_hash(raw):
    """Review executable AST separately from CP7-validated generated docstrings."""
    tree = ast.parse(raw)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                node.body.pop(0)
    return digest(ast.dump(tree, include_attributes=False).encode())


def repair_sources(source, project='file_report'):
    source = dict(source)
    if project == 'golden_ledger':
        source['_legacy_compat.py'] += '''

def legacy_int_error(error, value):
    """[Machine-generated] Preserve byte-literal diagnostic rendering returned by the legacy API."""
    message = str(error)
    prefix = 'invalid literal for int() with base 10: '
    if isinstance(value, bytes) and message.startswith(prefix + 'b'):
        message = prefix + message[len(prefix) + 1:]
    return message.encode('ascii')
'''
        text = source['main.py']
        before = "return b'invalid: ' + str(error).encode('ascii')"
        if text.count(before) != 1:
            raise ValueError('int-error repair base differs from reviewed source')
        source['main.py'] = text.replace('from _legacy_compat import legacy_divide',
            'from _legacy_compat import legacy_divide, legacy_int_error').replace(before,
            "return b'invalid: ' + legacy_int_error(error, text)")
        return source
    helper = 'reportkit/_legacy_compat.py'
    source[helper] += '''

def legacy_open(path, mode):
    """[Machine-generated] Reject descriptors as Python 2's path-based open did."""
    if not isinstance(path, (str, bytes)):
        raise TypeError('coercing to Unicode: need string or buffer, %s found' % type(path).__name__)
    return open(path, mode)
'''
    for path, target in [('reportkit/__init__.py', 'build_report'), ('reportkit/storage.py', 'read_numbers')]:
        text = source[path]
        marker = '\ndef ' + target + '('
        if text.count(marker) != 1 or 'with open(' not in text:
            raise ValueError('legacy-open repair base differs from reviewed source')
        text = text.replace(marker, '\nfrom ._legacy_compat import legacy_open\n\n\ndef ' + target + '(')
        source[path] = text.replace('with open(', 'with legacy_open(')
    return source


class PolicyRepairClient(MockLLMClient):
    def complete(self, prompt, **kwargs):
        self.calls.append(prompt)
        context = json.loads(prompt.split('Context JSON:\n', 1)[1])
        if context['project'] not in ('golden_ledger', 'file_report'):
            response = dict(patches=[], needs_human_review=['No reviewed source patch available for this remaining failure.'])
        else:
            changed = repair_sources(context['source'], context['project'])
            response = dict(patches=[dict(path=p, source=changed[p], base_sha256=context['source_sha256'][p],
                reason='Restore legacy API behavior through a shared helper and coordinated caller changes: path-only open or returned byte-literal error formatting. No exception is swallowed or test value special-cased.',
                hazards=['bytes_unicode']) for p in sorted(changed) if changed[p] != context['source'][p]], needs_human_review=[])
        return LLMResponse(json.dumps(response), self.model, TokenUsage())
