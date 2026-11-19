import json
from pathlib import Path
import sys
import tempfile
import unittest

from modernize.characterize import Characterizer, digest
from modernize.llm_prompts import CharacterizationInput, load_prompt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from pipeline_repair_client import review_hash
from revalidation_inputs import FRESH, exposed_ids
from test_characterize import record


class RevalidationTests(unittest.TestCase):
    def test_exposed_cases_remain_training_and_only_new_inputs_are_sealed(self):
        proposals = [CharacterizationInput(category='typical', args_json=json.dumps([v]),
            kwargs_json='{}', reason='input only').model_dump() for v in (0, 1, 2)]
        identity = dict(path='m.py', target='f', **{k:v for k,v in proposals[0].items() if k not in ('category','reason')})
        exposed = digest(json.dumps(identity, sort_keys=True).encode())[:20]
        class Runner:
            def run(self, project, script, function, args):
                operation, case = args
                if operation == 'inventory':
                    return record(dict(functions=[dict(path='m.py', target='f', line=1)], lines=['m.py:2'], branches=[], exclusions=[]))
                return record(dict(outcome=dict(status='completed', value=dict(type='int', value='1'), state=None),
                                   lines=['m.py:2'], branches=[]))
        class Proposer:
            def generate(self, name, context):
                return load_prompt(name).response_model.model_validate(dict(cases=proposals))
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / 'source'
            source.mkdir()
            (source / 'm.py').write_text('def f(x):\n    return x\n')
            stage = Characterizer(Runner(), Proposer(), root / 'run', heldout_exclude_ids=[exposed])
            stage.generate(source, 'p')
            training = json.loads((root / 'run/training/p.json').read_text())
            heldout = json.loads((root / 'run/sealed/p.json').read_text())
            self.assertIn(exposed, {f['case']['id'] for f in training})
            self.assertNotIn(exposed, {f['case']['id'] for f in heldout})
            self.assertEqual((len(training), len(heldout)), (2, 1))

    def test_fresh_input_pool_is_disjoint_and_contains_no_expected_outcomes(self):
        for key, proposals in json.loads(FRESH.read_text()).items():
            project, path = key.split('/', 1)
            path, target = path.split('::')
            for proposal in proposals:
                validated = CharacterizationInput.model_validate(proposal, strict=True)
                identity = dict(path=path, target=target, **{k:v for k,v in validated.model_dump().items() if k not in ('category','reason')})
                case_id = digest(json.dumps(identity, sort_keys=True).encode())[:20]
                self.assertNotIn(case_id, exposed_ids(project))

    def test_code_review_ignores_docs_but_not_payloads_or_control_flow(self):
        original = b'def f():\n    """Generated docs."""\n    return "payload"\n'
        self.assertEqual(review_hash(original), review_hash(original.replace(b'Generated docs.', b'Updated docs.')))
        self.assertNotEqual(review_hash(original), review_hash(original.replace(b'payload', b'changed')))
        self.assertNotEqual(review_hash(original), review_hash(b'def f():\n    return None\n'))
