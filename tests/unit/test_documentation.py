from decimal import Decimal
import json
from pathlib import Path
import tempfile
import unittest

from modernize.documentation import (DocumentationResponse, cross_check, fingerprint,
                                     load_documentation_prompt, observed_claims, render)
from modernize.llm import MockLLMClient
from modernize.llm_run import LLMRun, RateCard, RetryPolicy


class DocumentationTests(unittest.TestCase):
    def test_versioned_prompt_validates_retries_and_logs(self):
        prompt = load_documentation_prompt()
        response = dict(summary='Divide using legacy semantics.', observed_return_types=['int'],
                        observed_exceptions=[], limitations='Training observations only.')
        client = MockLLMClient(replies=('{}', json.dumps(response)))
        rates = RateCard(client.model, Decimal(0), Decimal(0), Decimal(0), 'mock', '2026-11-19')
        with tempfile.TemporaryDirectory() as directory:
            llm = LLMRun(client, Path(directory) / 'llm', rates, RetryPolicy(backoff_seconds=0))
            result = llm.generate(prompt, {'kind': 'function', 'observed': {'return_types': ['int']}})
            self.assertEqual(result.model_dump(), response)
            self.assertEqual(llm.records[0]['validation']['status'], 'failed')
            self.assertEqual(llm.records[1]['prompt_version'], 'documentation.v1')
            self.assertTrue(render(result).startswith('[Machine-generated]'))
            self.assertIn('Previous response failed validation', client.calls[1])

    def test_observed_claims_filter_target_and_list_mismatches(self):
        fixtures = [dict(case=dict(path='m.py', target='f'), expected=dict(outcome=dict(
            status='completed', value=dict(type='int', value='3')))),
            dict(case=dict(path='other.py', target='f'), expected=dict(outcome=dict(
                status='completed', value=dict(type='str', base64=''))))]
        observed = observed_claims(fixtures, 'm.py', 'f')
        self.assertEqual(observed, dict(cases=1, return_types=['int'], exceptions=[]))
        false_claim = DocumentationResponse(summary='Claims a floating return.',
            observed_return_types=['float'], observed_exceptions=['exceptions.TypeError'],
            limitations='Deliberately wrong for calibration.')
        self.assertEqual(len(cross_check(false_claim, observed)), 2)
        self.assertEqual(cross_check(false_claim, observed)[0]['observed'], ['int'])

    def test_checksums_detect_fixture_edit_addition_and_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / 'fixture.json'
            fixture.write_text('[]')
            original = fingerprint([root])
            fixture.write_text('[1]')
            self.assertNotEqual(fingerprint([root]), original)
            fixture.write_text('[]')
            extra = root / 'extra.json'
            extra.write_text('[]')
            self.assertNotEqual(fingerprint([root]), original)
            extra.unlink()
            fixture.unlink()
            self.assertNotEqual(fingerprint([root]), original)


if __name__ == '__main__':
    unittest.main()
