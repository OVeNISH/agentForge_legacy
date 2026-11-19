"""Versioned cross-runtime comparison; raw observations are never modified."""

import base64
import codecs
import copy
import json
import re

NAME = 'python2-python3.v1'


def kind(name, legacy):
    return {'unicode': 'text', 'str': 'binary' if legacy else 'text',
            'bytes': 'binary', 'long': 'int'}.get(name, name)


def value(item):
    if item is None:
        return None
    result = copy.deepcopy(item)
    if result['type'] in ('str', 'bytes', 'unicode'):
        result['type'] = 'binary' if 'base64' in result else 'text'
    elif result['type'] == 'long':
        result['type'] = 'int'
    elif result['type'] == 'dict':
        result['items'] = [[value(k), value(v)] for k, v in result['items']]
        result['items'].sort(key=lambda pair: json.dumps(pair[0], sort_keys=True))
    elif 'items' in result:
        result['items'] = [value(v) for v in result['items']]
        if result['type'] in ('set', 'frozenset'):
            result['items'].sort(key=lambda v: json.dumps(v, sort_keys=True))
    return result


def text(item):
    if 'base64' in item:
        return base64.b64decode(item['base64'], validate=True).decode('ascii')
    return item['value']


def diagnostic(message, name, legacy):
    """Recognize complete interpreter diagnostic grammars; unknown text stays exact."""
    if name == 'TypeError':
        match = re.fullmatch(r"unsupported operand type\(s\) for (.+): '([^']+)' and '([^']+)'", message)
        if match:
            op, left, right = match.groups()
            return dict(operator=op, left=kind(left, legacy), right=kind(right, legacy))
        match = re.fullmatch(r"int\(\) argument must be (?:a string or a number|a string, a bytes-like object or a real number), not '([^']+)'", message)
        if match:
            return dict(operation='int', invalid_argument_type=kind(match[1], legacy))
        old = re.fullmatch(r'(\w+)\(\) takes exactly (\d+) arguments? \((\d+) given\)', message)
        new = re.fullmatch(r'(?:\w+\.)*(\w+)\(\) takes (\d+) positional arguments? but (\d+) (?:was|were) given', message)
        if old or new:
            function, required, given = (old or new).groups()
            return dict(function=function, required=int(required), given=int(given))
    if name == 'AttributeError':
        match = re.fullmatch(r"'([^']+)' object has no attribute '([^']+)'", message)
        if match:
            return dict(type=kind(match[1], legacy), missing_attribute=match[2])
    if name == 'ValueError':
        match = re.fullmatch(r"(invalid literal for int\(\) with base \d+: )[bu]?(('.*')|(\".*\"))", message)
        if match:
            return match[1] + match[2]
    return message


def normalize(observation):
    result = copy.deepcopy(observation)
    outcome = result['outcome']
    if outcome['status'] == 'completed':
        outcome['value'] = value(outcome['value'])
        state = value(outcome['state'])
        if state is not None:
            # __dict__ keys are attribute identifiers; nested user dict keys retain their types.
            for pair in state['items']:
                if pair[0]['type'] == 'binary':
                    pair[0] = dict(type='text', value=text(pair[0]))
            state['items'].sort(key=lambda pair: json.dumps(pair[0], sort_keys=True))
        outcome['state'] = state
        return result
    legacy = outcome['module'] == 'exceptions'
    if outcome['module'] not in ('exceptions', 'builtins'):
        outcome['args'] = value(outcome['args'])
        return result
    outcome['module'] = 'python.builtins'
    arguments = outcome['args']['items']
    if outcome['name'] in ('UnicodeEncodeError', 'UnicodeDecodeError') and len(arguments) == 5:
        encoding, payload, start, end, reason = arguments
        encoding = codecs.lookup(text(encoding)).name
        # All structured error data is retained; the runtime's redundant rendering varies.
        outcome['args'] = dict(type='tuple', items=[dict(type='text', value=encoding), value(payload),
            value(start), value(end), dict(type='text', value=text(reason))])
        outcome['message'] = dict(unicode_error=outcome['name'], encoding=encoding,
                                  start=value(start), end=value(end), reason=text(reason))
    elif len(arguments) == 1 and arguments[0]['type'] in ('str', 'unicode') and text(arguments[0]) == outcome['message']:
        message = diagnostic(outcome['message'], outcome['name'], legacy)
        outcome['args'] = dict(type='tuple', items=[dict(type='diagnostic', value=message)])
        outcome['message'] = message
    else:
        outcome['args'] = value(outcome['args'])
    return result


def equal(expected, actual):
    return normalize(expected) == normalize(actual)
