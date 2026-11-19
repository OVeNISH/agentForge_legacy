import base64
from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from modernize.characterize import digest
from modernize.llm import MockLLMClient
from modernize.llm_run import LLMRun, RateCard, RetryPolicy
from modernize.transformation import (SourceChanges, SourcePatch, apply_changes,
    check_public_api, load_transformation_prompt, transform)


def change(path='m.py', source='def f(x):\n    return x\n', original=b'def f(x):\n    return x / 2\n'):
    return dict(path=path, source=source, base_sha256=digest(original) if original is not None else None,
                reason='Preserve numeric behavior.', hazards=['division'])


class TransformationTests(unittest.TestCase):
    def test_versioned_schema_mock_retry_and_extra_field_rejection(self):
        prompt = load_transformation_prompt()
        response = dict(patches=[change()], needs_human_review=[])
        client = MockLLMClient(replies=('{}', json.dumps(response)))
        with tempfile.TemporaryDirectory() as directory:
            rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0), 'mock', '2026-11-19')
            run = LLMRun(client, Path(directory) / 'llm', rates, RetryPolicy(backoff_seconds=0))
            self.assertEqual(run.generate(prompt, {}).model_dump(), response)
            self.assertEqual(run.records[0]['validation']['status'], 'failed')
        with self.assertRaises(ValidationError):
            SourceChanges.model_validate(dict(response, fixtures=[]))

    def test_safe_paths_base_hashes_duplicates_and_compile_rejection(self):
        original = b'def f(x):\n    return x / 2\n'
        for path in ('../m.py', '/m.py', 'tests/t.py', 'fixtures/f.py', 'sealed/s.py',
                     '.git/hooks/x.py', 'a/../m.py', '__cp8_validate__.py'):
            with self.subTest(path=path), self.assertRaises(ValidationError):
                SourcePatch.model_validate(change(path=path))
        valid = SourcePatch.model_validate(change())
        files = {'m.py': original}
        changes = SourceChanges(patches=[valid], needs_human_review=[])
        self.assertEqual(apply_changes(files, changes)['m.py'], valid.source.encode())
        self.assertEqual(files['m.py'], original)
        for patches in ([valid, valid], [valid.model_copy(update={'base_sha256': '0'*64})],
                        [SourcePatch.model_validate(change(path='new/unsafe.py', original=None))]):
            with self.assertRaises(ValueError):
                apply_changes(files, SourceChanges(patches=patches, needs_human_review=[]))
        with self.assertRaises(SyntaxError):
            apply_changes(files, SourceChanges(patches=[valid.model_copy(update={'source': 'def broken('})],
                                               needs_human_review=[]))

    def test_changed_public_signature_is_rejected(self):
        facts = dict(files=[dict(path='p/m.py', functions=[dict(qualname='f', signature=dict(
            parameters=['x'], defaults=[], vararg=None, kwarg=None))], classes=[])])
        validation = dict(files=[dict(path='m.py', definitions=[dict(name='f', signature=dict(
            parameters=['x'], defaults=0, vararg=None, kwarg=None))])])
        check_public_api(validation, facts, 'p')
        validation['files'][0]['definitions'][0]['signature']['parameters'] = ['renamed']
        with self.assertRaisesRegex(ValueError, 'signature'):
            check_public_api(validation, facts, 'p')

    def test_failed_candidate_is_retried_without_partial_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project, output = root / 'project', root / 'output'
            project.mkdir()
            output.mkdir()
            raw = b'def f(x):\n    return x / 2\n'
            (project / 'm.py').write_bytes(raw)
            responses = [SourceChanges(patches=[SourcePatch.model_validate(change(source='def bad('))],
                                      needs_human_review=[]),
                         SourceChanges(patches=[SourcePatch.model_validate(change())], needs_human_review=[])]
            class Proposer:
                def __init__(self): self.contexts = []
                def generate(self, prompt, context):
                    self.contexts.append(context)
                    return responses[len(self.contexts)-1]
            proposer = Proposer()
            def sandbox(*args):
                self.assertFalse((output / 'source').exists())
                if args[4] == 'run' and args[2] == '__cp8_mechanical__.py':
                    return dict(files={'m.py': base64.b64encode(raw).decode()}, fixers=[])
                return dict(files=[dict(path='m.py', compiled=True, imported=True, definitions=[])])
            with patch('modernize.transformation.sandbox_call', side_effect=sandbox):
                report = transform(project, 'p', dict(files=[]), {}, proposer, None, None, output)
            self.assertEqual([a['accepted'] for a in report['attempts']], [False, True])
            self.assertTrue(proposer.contexts[1]['validation_error'])
            self.assertEqual((project / 'm.py').read_bytes(), raw)
            self.assertEqual((output / 'source/m.py').read_text(), responses[1].patches[0].source)


if __name__ == '__main__':
    unittest.main()
