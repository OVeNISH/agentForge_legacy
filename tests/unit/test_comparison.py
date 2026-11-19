import base64
import copy
import unittest

from modernize.comparison import equal, normalize
from modernize.repair import metrics


def binary(raw, legacy=False):
    return dict(type='str' if legacy else 'bytes', base64=base64.b64encode(raw).decode())


def observation(item):
    return dict(outcome=dict(status='completed', value=item, state=None), stdout_base64='', stderr_base64='', files=[], target_exit_code=0)


class ComparisonTests(unittest.TestCase):
    def test_policy_metrics_do_not_rewrite_raw_pass_flags(self):
        import json
        expected = observation(dict(type='unicode', value='sample'))
        actual = observation(dict(type='str', value='sample'))
        record = dict(container_removed=True, result=dict(status='completed',
            value=dict(type='str', value=json.dumps(dict(outcome=actual['outcome']))), exception=None,
            target_exit_code=0, stdout_base64='', stderr_base64='', files=[], capture_error=None))
        fixtures = [dict(case=dict(id='visible'), expected=expected)]
        results = [dict(id='visible', actual=actual, record=record, passed=False)]
        self.assertEqual(metrics(fixtures, results)['passed'], 0)
        self.assertEqual(metrics(fixtures, results, equal)['passed'], 1)
        self.assertFalse(results[0]['passed'])

    def test_diagnostics_do_not_hide_arity_or_unknown_message_changes(self):
        from modernize.comparison import diagnostic
        self.assertEqual(diagnostic('__init__() takes exactly 1 argument (2 given)', 'TypeError', True),
                         diagnostic('Board.__init__() takes 1 positional argument but 2 were given', 'TypeError', False))
        self.assertNotEqual(diagnostic('__init__() takes exactly 1 argument (3 given)', 'TypeError', True),
                            diagnostic('Board.__init__() takes 1 positional argument but 2 were given', 'TypeError', False))
        self.assertNotEqual(diagnostic('unexpected error one', 'ValueError', True),
                            diagnostic('unexpected error two', 'ValueError', False))

    def test_representation_aliases_preserve_types_data_and_raw_evidence(self):
        old = observation(dict(type='unicode', value='é'))
        new = observation(dict(type='str', value='é'))
        before = copy.deepcopy(old)
        self.assertTrue(equal(old, new))
        self.assertEqual(old, before)
        self.assertTrue(equal(observation(binary(b'abc', True)), observation(binary(b'abc'))))
        for wrong in (binary(b'abc'), dict(type='str', value='e'), dict(type='int', value='1')):
            self.assertFalse(equal(old, observation(wrong)))
        for field, wrong in [('stdout_base64', 'IA=='), ('stderr_base64', 'IA=='), ('files', [{'path': 'x'}]), ('target_exit_code', 1)]:
            changed = copy.deepcopy(new)
            changed[field] = wrong
            self.assertFalse(equal(old, changed))

    def test_builtin_diagnostics_preserve_class_operator_and_payload(self):
        old = observation(None)
        message = "unsupported operand type(s) for /: 'unicode' and 'int'"
        old['outcome'] = dict(status='exception', module='exceptions', name='TypeError', message=message,
                              args=dict(type='tuple', items=[binary(message.encode(), True)]))
        new = copy.deepcopy(old)
        message = "unsupported operand type(s) for /: 'str' and 'int'"
        new['outcome'].update(module='builtins', message=message, args=dict(type='tuple', items=[dict(type='str', value=message)]))
        self.assertTrue(equal(old, new))
        for key, wrong in [('name', 'ValueError'), ('module', 'custom_errors'), ('message', 'different error')]:
            changed = copy.deepcopy(new)
            changed['outcome'][key] = wrong
            self.assertFalse(equal(old, changed))
        # Returned strings do not receive diagnostic rewriting.
        self.assertFalse(equal(observation(binary(b"invalid literal for int() with base 10: 'x'", True)),
                               observation(binary(b"invalid literal for int() with base 10: b'x'"))))

    def test_unicode_error_offsets_encoding_and_data_are_not_ignored(self):
        old = observation(None)
        old['outcome'] = dict(status='exception', module='exceptions', name='UnicodeDecodeError', message='legacy rendering',
            args=dict(type='tuple', items=[binary(b'utf8', True), binary(b'\xff', True),
                dict(type='int', value='0'), dict(type='int', value='1'), binary(b'invalid start byte', True)]))
        new = copy.deepcopy(old)
        new['outcome'].update(module='builtins', message='modern rendering')
        new['outcome']['args']['items'] = [dict(type='str', value='utf-8'), binary(b'\xff'),
            dict(type='int', value='0'), dict(type='int', value='1'), dict(type='str', value='invalid start byte')]
        self.assertTrue(equal(old, new))
        for index, wrong in [(0, dict(type='str', value='ascii')), (1, binary(b'\xfe')), (2, dict(type='int', value='1')),
                             (4, dict(type='str', value='different reason'))]:
            changed = copy.deepcopy(new)
            changed['outcome']['args']['items'][index] = wrong
            self.assertFalse(equal(old, changed))
