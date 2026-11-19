"""Exact structural schema for the trusted worker's untrusted JSON response."""

POSITION = dict(scope=str, line=int)
FILE = dict(
    path=str, sha256=str, docstring=(str, type(None)),
    functions=[dict(name=str, qualname=str, **POSITION,
                    signature=dict(parameters=[str], defaults=[str],
                                   vararg=(str, type(None)), kwarg=(str, type(None))),
                    decorators=[str], docstring=(str, type(None)))],
    classes=[dict(name=str, qualname=str, **POSITION, bases=[str],
                  docstring=(str, type(None)))],
    comments=[dict(line=int, column=int, text=str)],
    imports=[dict(**POSITION, module=str, name=(str, type(None)), alias=str, level=int)],
    calls=[dict(**POSITION, callee=str)],
    symbols=[dict(**POSITION, name=str, kind=str, target=(str, type(None)))],
    references=[dict(**POSITION, name=str, column=int, context=str)],
    side_effects=[dict(**POSITION, kind=str, detail=str)],
)
INDEX = dict(
    modules=dict,
    imports=[dict(source=str, target=(str, type(None)), **POSITION,
                  module=str, name=(str, type(None)), alias=str, level=int)],
    calls=[dict(path=str, target=(str, type(None)), resolved_name=(str, type(None)),
                **POSITION, callee=str)],
    symbols=[dict(id=str, path=str, scope=str, name=str, kinds=[str], lines=[int])],
    references=[dict(path=str, binding=(str, type(None)), **POSITION,
                     name=str, column=int, context=str)],
)
PROJECT = dict(schema_version=int, files=[FILE], index=INDEX,
               inventory=dict(excluded=[str], unsupported=[str]), entry_points=[str])


def validate(value, shape, location='facts'):
    if isinstance(shape, dict):
        if not isinstance(value, dict) or value.keys() != shape.keys():
            raise ValueError(f'{location}: expected exact keys {sorted(shape)}')
        for key, field in shape.items():
            validate(value[key], field, f'{location}.{key}')
    elif isinstance(shape, list):
        if not isinstance(value, list):
            raise ValueError(f'{location}: expected array')
        for index, item in enumerate(value):
            validate(item, shape[0], f'{location}[{index}]')
    elif type(value) not in (shape if isinstance(shape, tuple) else (shape,)):
        raise ValueError(f'{location}: wrong type')


def validate_files(files):
    validate(files, [FILE])
    enums = {
        'symbols': {'variable', 'function', 'class', 'parameter', 'import', 'global'},
        'side_effects': {'file_io', 'network', 'database', 'environment', 'time',
                         'randomness', 'global_mutable'},
    }
    for file in files:
        for group in ('functions', 'classes', 'comments', 'imports', 'calls',
                      'symbols', 'references', 'side_effects'):
            for record in file[group]:
                if record['line'] < 1 or ('column' in record and record['column'] < 0):
                    raise ValueError('invalid source position')
                if group in enums and record['kind'] not in enums[group]:
                    raise ValueError('invalid ' + group + ' kind')
        if any(r['context'] not in ('Load', 'Store', 'Del') for r in file['references']):
            raise ValueError('invalid reference context')
        if any(i['level'] < 0 for i in file['imports']):
            raise ValueError('invalid relative import level')
