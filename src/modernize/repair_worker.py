"""CP9 replay with diagnostic tracebacks; CP5's frozen comparator stays exact."""

import base64
import importlib
import json
import os
import sys
import traceback

from __cp5__ import decode
from sandbox_codec import outcome_value


def run(case):
    for path, raw in json.loads(case['files_json']).items():
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)
        with open(path, 'wb') as stream:
            stream.write(base64.b64decode(raw))
    diagnostic = []
    try:
        module = case['path'][:-3].replace('/', '.')
        if module.endswith('.__init__'):
            module = module[:-9]
        target = importlib.import_module(module)
        names = case['target'].split('.')
        instance = None
        if len(names) == 2:
            cls = getattr(target, names[0])
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
        diagnostic = [dict(file=f.filename, line=f.lineno, function=f.name)
                      for f in traceback.extract_tb(sys.exc_info()[2])]
        result = dict(status='exception', module=type(error).__module__, name=type(error).__name__,
                      args=outcome_value(error.args), message=str(error))
    else:
        result = dict(status='completed', value=outcome_value(value),
                      state=outcome_value(instance.__dict__) if instance is not None else None)
    return json.dumps(dict(outcome=result, traceback=diagnostic), sort_keys=True, ensure_ascii=True)
