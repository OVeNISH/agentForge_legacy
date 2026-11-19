from dataclasses import replace
from decimal import Decimal
from importlib import resources
import json
from pathlib import Path
import secrets
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from pydantic import ValidationError

from modernize.llm import LLMResponse, MockLLMClient, ProviderError, TokenUsage
from modernize.llm_prompts import InputProposals, PROMPTS, load_prompt, strict_json
from modernize.llm_run import LLMRun, LLMStageFailure, RateCard, RetryPolicy, recompute_usage
from modernize.openai_client import OpenAIClient


def proposal():
    return {'cases': [dict(category='typical', args_json='[1, 2]', kwargs_json='{}', reason='Two integer inputs.')]}


def rates(model='deterministic-mock'):
    return RateCard(model, Decimal('2'), Decimal('0.5'), Decimal('6'),
                    'synthetic unit-test tariff; not live provider pricing', '2026-11-19')


class LLMLayerTests(unittest.TestCase):
    def test_every_template_has_schema_and_mock_validation(self):
        directory = resources.files('modernize').joinpath('prompts')
        self.assertEqual({p.name[:-4] for p in directory.iterdir() if p.name.endswith('.txt')}, set(PROMPTS))
        for name in PROMPTS:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as root:
                prompt = load_prompt(name)
                self.assertEqual(prompt.schema, prompt.response_model.model_json_schema())
                mock = MockLLMClient(response=json.dumps(proposal()))
                run = LLMRun(mock, Path(root) / 'run', rates())
                value = run.generate(name, {'function': 'example(a, b)'})
                self.assertEqual(value.cases[0].args_json, '[1, 2]')
                self.assertIn('$bytes', mock.calls[0])
                self.assertNotIn('$context', mock.calls[0])
                self.assertEqual(recompute_usage(run.output)['attempts'], 1)
                self.assertEqual(json.loads((run.output / 'summary.json').read_text())['evidence_kind'], 'mock')

    def test_malformed_response_retries_then_logged_failure(self):
        with tempfile.TemporaryDirectory() as root:
            mock = MockLLMClient(response='not JSON')
            run = LLMRun(mock, Path(root) / 'run', rates(), RetryPolicy(backoff_seconds=0), evidence_kind='mock')
            with self.assertRaises(LLMStageFailure):
                run.generate('input_proposals.v1', {})
            records = [json.loads(line) for line in run.log.read_text().splitlines()]
            self.assertEqual(len(mock.calls), 3)
            self.assertTrue(all(r['validation']['status'] == 'failed' for r in records))
            self.assertIn('Previous response failed validation', mock.calls[1])
            self.assertFalse(records[-1]['will_retry'])
            self.assertEqual(json.loads((run.output / 'summary.json').read_text())['status'], 'failed')

    def test_validation_feedback_recovers_and_all_attempt_tokens_are_charged(self):
        with tempfile.TemporaryDirectory() as root:
            usage = TokenUsage(100, 20, 40)
            mock = MockLLMClient(replies=(LLMResponse('{}', 'deterministic-mock', usage),
                                          LLMResponse(json.dumps(proposal()), 'deterministic-mock', usage)))
            run = LLMRun(mock, Path(root) / 'run', rates(), RetryPolicy(backoff_seconds=0), evidence_kind='mock')
            run.generate('input_proposals.v1', {})
            summary = recompute_usage(run.output)
            self.assertEqual(summary['known_total_tokens'], 240)
            self.assertEqual(Decimal(summary['known_estimated_usd']), Decimal('0.00052'))
            self.assertEqual(summary['attempts'], 2)

    def test_schema_rejects_expected_outputs_wrong_types_and_bad_argument_json(self):
        for bad in ('[]', '{"cases":[],"expected":3}', '{"cases":"wrong"}'):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                InputProposals.model_validate(strict_json(bad))
        for args in ('{}', '[NaN]', '[1e9999]', '[{"x":1,"x":2}]', '[{"$bytes":"%%%"}]'):
            data = proposal()
            data['cases'][0]['args_json'] = args
            with self.subTest(args=args), self.assertRaises(ValidationError):
                InputProposals.model_validate(data)
        data = proposal()
        data['cases'][0]['expected_output'] = 3
        with self.assertRaises(ValidationError):
            InputProposals.model_validate(data)

    def test_unknown_usage_and_unpriced_cache_write_are_not_claimed_as_zero(self):
        for usage in (None, TokenUsage(100, 20, 0, 50)):
            with self.subTest(usage=usage), tempfile.TemporaryDirectory() as root:
                mock = MockLLMClient(replies=(LLMResponse(json.dumps(proposal()), 'deterministic-mock', usage),))
                run = LLMRun(mock, Path(root) / 'run', rates(), evidence_kind='mock')
                run.generate('input_proposals.v1', {})
                summary = recompute_usage(run.output)
                self.assertEqual(summary['unknown_cost_attempts'], 1)
                self.assertFalse(summary['cost_complete'])

    def test_rate_limit_delay_over_budget_stops_without_early_retry(self):
        with tempfile.TemporaryDirectory() as root:
            mock = MockLLMClient(replies=(ProviderError('slow down', code='http_429', retryable=True, retry_after=60),))
            run = LLMRun(mock, Path(root) / 'run', rates(), evidence_kind='mock')
            with patch('modernize.llm_run.time.sleep') as sleep, self.assertRaises(LLMStageFailure):
                run.generate('input_proposals.v1', {})
            sleep.assert_not_called()
            self.assertEqual(len(mock.calls), 1)
            self.assertEqual(run.records[0]['retry_after_seconds'], 60)

    def test_retry_window_stops_a_late_response(self):
        with tempfile.TemporaryDirectory() as root:
            run = LLMRun(MockLLMClient(response=json.dumps(proposal())), Path(root) / 'run', rates(),
                         RetryPolicy(retry_window_seconds=1), evidence_kind='mock')
            with patch('modernize.llm_run.time.monotonic', side_effect=[0, 0, 0, 2, 2]), \
                    self.assertRaises(LLMStageFailure):
                run.generate('input_proposals.v1', {})
            self.assertEqual(run.records[0]['error_code'], 'deadline')

    def test_secrets_are_redacted_from_requests_errors_and_serialized_logs(self):
        key = 'sk-' + secrets.token_hex(24)
        with tempfile.TemporaryDirectory() as root, patch.dict('os.environ', {'OPENAI_API_KEY': key}):
            mock = MockLLMClient(response=key)
            run = LLMRun(mock, Path(root) / 'run', rates(), RetryPolicy(max_attempts=1), evidence_kind='mock')
            with self.assertRaises(LLMStageFailure) as error:
                run.generate('input_proposals.v1', {'accidental_secret': key})
            self.assertNotIn(key, str(error.exception))
            self.assertNotIn(key, mock.calls[0])
            for path in run.output.iterdir():
                self.assertNotIn(key, path.read_text())
            self.assertIn('[REDACTED]', run.log.read_text())

    def test_configuration_and_metadata_validation(self):
        for usage in ((True, 0), (-1, 0), (1, 0, 2), (100, 0, 90, 90)):
            with self.subTest(usage=usage), self.assertRaises(ValueError):
                TokenUsage(*usage)
        with self.assertRaises(ValueError):
            RetryPolicy(max_attempts=0)
        with self.assertRaises(ValueError):
            replace(rates(), input_per_million=Decimal('NaN'))
        with self.assertRaises(ValueError):
            load_prompt('../../escape')
        sdk = Mock(api_key=None)
        sdk.with_options.return_value.responses.create.return_value = SimpleNamespace(usage=SimpleNamespace(
            input_tokens=1, output_tokens=1, total_tokens=2,
            input_tokens_details=SimpleNamespace(cached_tokens=0)))
        with self.assertRaises(ProviderError) as missing_usage:
            OpenAIClient('fixture', sdk=sdk).complete('Return JSON')
        self.assertEqual(missing_usage.exception.code, 'usage_invalid')
