"""Python 2/3 wire values. Runtime output types are never normalized."""

import base64
import json
import sys

PY2 = sys.version_info[0] == 2
TEXT = type(u'')


def pack_input(value, depth=0):
    if depth > 30:
        raise ValueError('input nesting exceeds 30')
    if isinstance(value, bytes):
        return dict(kind='bytes', value=base64.b64encode(value).decode('ascii'))
    if isinstance(value, TEXT):
        return dict(kind='text', value=value)
    if value is None or type(value) in (bool, int, float):
        return dict(kind='scalar', value=value)
    if type(value) in (list, tuple):
        return dict(kind=type(value).__name__, value=[pack_input(v, depth + 1) for v in value])
    if type(value) is dict:
        return dict(kind='dict', value=[[pack_input(k, depth + 1), pack_input(v, depth + 1)] for k, v in value.items()])
    raise ValueError('unsupported input type: ' + type(value).__name__)


def unpack_input(value):
    kind, data = value['kind'], value['value']
    if kind == 'bytes':
        return base64.b64decode(data)
    if kind in ('text', 'scalar'):
        return data
    if kind in ('list', 'tuple'):
        items = [unpack_input(v) for v in data]
        return tuple(items) if kind == 'tuple' else items
    if kind == 'dict':
        return dict((unpack_input(k), unpack_input(v)) for k, v in data)
    raise ValueError('unsupported input kind: ' + kind)


def outcome_value(value, depth=0):
    if depth > 30:
        raise ValueError('return value nesting exceeds 30')
    kind = type(value).__name__
    if value is None:
        return dict(type=kind)
    if type(value) is bool:
        return dict(type=kind, value=value)
    if type(value) in ((int, long) if PY2 else (int,)):  # noqa: F821
        return dict(type=kind, value=str(value))
    if type(value) is float:
        return dict(type=kind, value=value.hex())
    if type(value) is bytes:
        return dict(type=kind, base64=base64.b64encode(value).decode('ascii'))
    if type(value) is TEXT:
        return dict(type=kind, value=value)
    if type(value) in (list, tuple, set, frozenset):
        items = [outcome_value(v, depth + 1) for v in value]
        if type(value) in (set, frozenset):
            items.sort(key=lambda v: json.dumps(v, sort_keys=True))
        return dict(type=kind, items=items)
    if type(value) is dict:
        items = [[outcome_value(k, depth + 1), outcome_value(v, depth + 1)]
                 for k, v in value.items()]
        items.sort(key=lambda v: json.dumps(v[0], sort_keys=True))
        return dict(type=kind, items=items)
    raise ValueError('unsupported return type: ' + type(value).__module__ + '.' + kind)
