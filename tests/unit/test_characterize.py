import base64
import json
from pathlib import Path
import tempfile
import unittest

from pydantic import ValidationError

from modernize.characterize import (Characterizer, comparable, coverage, export_training,
                                    read_observation, seal, verify_seal, write_json)
from modernize.llm import MockLLMClient
from modernize.llm_prompts import CharacterizationInput, load_prompt
from modernize.llm_run import LLMRun, RateCard
from decimal import Decimal


def record(observed):
    return dict(protocol_error=None, container_removed=True, result=dict(status='completed',
        value=dict(type='str', base64=base64.b64encode(json.dumps(observed).encode()).decode()),
        exception=None, target_exit_code=0, stdout_base64='', stderr_base64='', files=[], capture_error=None))


class CharacterizationTests(unittest.TestCase):
    def test_prompt_mock_and_input_trust_boundary(self):
        case = dict(category='typical', args_json='[]', kwargs_json='{}', reason='input only')
        with tempfile.TemporaryDirectory() as directory:
            client = MockLLMClient(response=json.dumps(dict(cases=[case])))
            rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0), 'mock', '2026-11-19')
            run = LLMRun(client, Path(directory) / 'llm', rates)
            result = run.generate('characterization_inputs.v1', {'function': 'probe'})
            self.assertEqual(result.cases[0].args_json, '[]')
            self.assertEqual(load_prompt('characterization_inputs.v1').schema,
                             type(result).model_json_schema())
        for extra in ({'files_json': '{"../escape":""}'},
                      {'files_json': '{"safe":"!"}'},
                      {'setup_json': '[{"method":"__class__","args":[],"kwargs":{}}]'},
                      {'expected': 1}, {'args_json': '[{"$bytes":"!"}]'}):
            with self.subTest(extra=extra), self.assertRaises((ValidationError, ValueError)):
                CharacterizationInput.model_validate(dict(case, **extra))

    def test_exact_observation_and_infrastructure_rejection(self):
        first = record(dict(outcome=dict(status='completed', value={'type':'int','value':'1'}),
                            lines=['m.py:2'], branches=[]))
        second = json.loads(json.dumps(first))
        self.assertEqual(comparable(first), comparable(second))
        second['result']['stdout_base64'] = base64.b64encode(b' ').decode()
        self.assertNotEqual(comparable(first), comparable(second))
        second['protocol_error'] = 'killed'
        with self.assertRaisesRegex(ValueError, 'infrastructure'):
            read_observation(second)

    def test_coverage_denominator_is_static_not_observed(self):
        result = coverage(dict(lines=['m:1','m:2'], branches=['m:1:2','m:1:3']),
                          [dict(lines=['m:1','ignored:99'], branches=['m:1:2'])])
        self.assertEqual(result['lines']['percent'], 50)
        self.assertEqual(result['branches']['missing'], ['m:1:3'])

    def test_seal_detects_changes_and_export_excludes_heldout_and_logs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'store'
            write_json(root / 'training/p.json', [{'input':1}])
            write_json(root / 'sealed/p.json', [{'secret':2}])
            write_json(root / 'private/prompts.json', {'secret':2})
            manifest = seal(root)
            self.assertEqual(verify_seal(root), manifest)
            exported = export_training(root, Path(directory) / 'repair')
            self.assertEqual([p.name for p in exported.iterdir()], ['p.json'])
            with self.assertRaises(ValueError):
                export_training(root, root / 'repair')
            path = root / 'training/p.json'
            path.chmod(0o600)
            path.write_text('[]')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                verify_seal(root)

    def test_flaky_cases_quarantine_and_bounded_coverage_feedback(self):
        class Runner:
            def __init__(self):
                self.count = 0
            def run(self, project, script, function, args):
                operation, value = args
                if operation == 'inventory':
                    return record(dict(functions=[dict(path='m.py',target='f',line=1)],
                                       lines=['m.py:2','m.py:3'], branches=[], exclusions=[]))
                self.count += 1
                return record(dict(outcome=dict(status='completed', value=self.count),
                                   lines=['m.py:2'], branches=[]))
        class Proposer:
            def __init__(self):
                self.contexts = []
            def generate(self, name, context):
                self.contexts.append(context)
                return load_prompt(name).response_model.model_validate(dict(cases=[dict(
                    category='typical',args_json='[]',kwargs_json='{}',reason='probe')]))
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'project'
            project.mkdir()
            (project / 'm.py').write_text('def f():\n    return 1\n')
            runner, proposer = Runner(), Proposer()
            stage = Characterizer(runner, proposer, Path(directory)/'store')
            report = stage.generate(project, 'p')
            self.assertEqual(report['quarantined'], 1)
            self.assertEqual(report['accepted'], 0)
            self.assertEqual(runner.count, 3)
            self.assertEqual(len(proposer.contexts), 2)
            self.assertEqual(proposer.contexts[1]['uncovered']['lines'], ['m.py:2','m.py:3'])


if __name__ == '__main__':
    unittest.main()
