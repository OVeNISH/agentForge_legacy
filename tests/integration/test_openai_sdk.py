"""The real SDK with intercepted HTTP; no live key, network or provider charge."""

from decimal import Decimal
import json
from pathlib import Path
import secrets
import tempfile
import unittest

import httpx2
from openai import OpenAI

from modernize.llm_run import LLMRun, LLMStageFailure, RateCard, RetryPolicy, recompute_usage
from modernize.openai_client import OpenAIClient

ROOT = Path(__file__).resolve().parents[2]
MODEL = 'sdk-fixture-model'


def valid_text(reason='Typical integer arguments.'):
    return json.dumps({'cases': [dict(category='typical', args_json='[1, 2]', kwargs_json='{}', reason=reason)]})


def body(text, status='completed', refusal=False, usage=True):
    content = ([dict(type='refusal', refusal='fixture refusal')] if refusal else
               [dict(type='output_text', text=text, annotations=[], logprobs=[])])
    result = dict(id='resp_fixture', object='response', created_at=0, status=status, model=MODEL,
                  output=[dict(id='msg_fixture', type='message', role='assistant', status='completed', content=content)])
    if usage:
        result['usage'] = dict(input_tokens=100, output_tokens=20, total_tokens=120,
                               input_tokens_details=dict(cached_tokens=40, cache_write_tokens=0),
                               output_tokens_details=dict(reasoning_tokens=0))
    return result


class OpenAISDKTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = []

    @classmethod
    def tearDownClass(cls):
        path = ROOT / 'artifacts/cp4-sdk.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(dict(kind='sdk_http_fixture', paid_provider_calls=0,
                                        scenarios=cls.evidence), sort_keys=True, indent=2) + '\n')

    def scenario(self, name, replies, *, expect_failure=False, context=None):
        key = 'sk-' + secrets.token_hex(24)
        requests = []
        timeouts = []
        def handler(request):
            self.assertEqual(request.url.host, 'api.openai.com')
            self.assertEqual(request.headers['authorization'], 'Bearer ' + key)
            self.assertTrue(0 < request.extensions['timeout']['read'] <= 1.25)
            timeouts.append(request.extensions['timeout'])
            requests.append(json.loads(request.content))
            index = len(requests) - 1
            response = replies[min(index, len(replies) - 1)]
            if response == 'timeout':
                raise httpx2.ReadTimeout('fixture read timeout', request=request)
            if response == 'key_echo':
                return httpx2.Response(200, json=body(valid_text(key)))
            if isinstance(response, tuple):
                code, headers = response
                return httpx2.Response(code, headers=headers,
                                      json={'error': {'message': 'fixture error ' + key, 'type': 'fixture'}})
            return httpx2.Response(200, json=response)
        with tempfile.TemporaryDirectory() as root, \
                httpx2.Client(transport=httpx2.MockTransport(handler), trust_env=False) as http, \
                OpenAI(api_key=key, http_client=http, max_retries=2) as sdk:
            client = OpenAIClient(MODEL, sdk=sdk, max_output_tokens=1000)
            rates = RateCard(MODEL, Decimal('2'), Decimal('0.5'), Decimal('6'),
                             'synthetic HTTP fixture tariff; not provider pricing', '2026-11-19')
            run = LLMRun(client, Path(root) / 'run', rates,
                         RetryPolicy(call_timeout_seconds=1.25, backoff_seconds=0),
                         evidence_kind='sdk_http_fixture')
            with self.assertLogs('openai', level='DEBUG') as sdk_logs:
                if expect_failure:
                    with self.assertRaises(LLMStageFailure) as error:
                        run.generate('input_proposals.v1', context or {})
                    self.assertNotIn(key, str(error.exception))
                else:
                    run.generate('input_proposals.v1', context or {})
            self.assertTrue(all(key not in message for message in sdk_logs.output),
                            'credential appeared in SDK debug logs')
            self.assertEqual(len(requests), len(run.records), 'SDK retries must be disabled')
            self.assertTrue(all(r['store'] is False and r['tools'] == [] for r in requests))
            self.assertTrue(all(r['text']['format']['strict'] for r in requests))
            self.assertTrue(all(r['max_output_tokens'] == 1000 for r in requests))
            for path in run.output.iterdir():
                self.assertNotIn(key, path.read_text())
            summary = json.loads((run.output / 'summary.json').read_text())
            recomputed = recompute_usage(run.output)
            self.assertTrue(all(summary[k] == v for k, v in recomputed.items()))
            self.evidence.append(dict(name=name, attempts=run.records, summary=summary,
                                      intercepted_requests=len(requests), timeout_options=timeouts,
                                      actual_provider_calls=0))
            return run.records, summary

    def test_success_uses_sdk_and_reports_usage(self):
        records, summary = self.scenario('success', [body(valid_text())])
        self.assertEqual(summary['known_total_tokens'], 120)
        self.assertEqual(Decimal(summary['known_estimated_usd']), Decimal('0.00026'))
        self.assertEqual(records[0]['validation']['status'], 'passed')

    def test_malformed_response_is_bounded_and_logged(self):
        records, summary = self.scenario('malformed_failure', [body('not JSON')], expect_failure=True)
        self.assertEqual(len(records), 3)
        self.assertEqual(summary['status'], 'failed')
        self.assertTrue(all(r['validation']['status'] == 'failed' for r in records))
        self.assertIn('Previous response failed validation', records[1]['prompt'])

    def test_invalid_schema_gets_feedback_then_recovers(self):
        records, summary = self.scenario('schema_recovery', [body('{}'), body(valid_text())])
        self.assertEqual([r['validation']['status'] for r in records], ['failed', 'passed'])
        self.assertEqual(summary['attempts'], 2)

    def test_timeout_and_rate_limit_retry_without_hidden_sdk_retries(self):
        records, summary = self.scenario('timeout_rate_limit_recovery',
                                         ['timeout', (429, {'Retry-After': '0'}), body(valid_text())])
        self.assertEqual([r['error_code'] for r in records], ['timeout', 'http_429', None])
        self.assertEqual(summary['unknown_usage_attempts'], 2)
        self.assertFalse(summary['cost_complete'])

    def test_auth_failure_is_fatal_and_redacted(self):
        records, summary = self.scenario('auth_failure', [(401, {})], expect_failure=True)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['error_code'], 'http_401')

    def test_refusal_is_logged_without_schema_acceptance(self):
        records, summary = self.scenario('refusal', [body('', refusal=True)], expect_failure=True)
        self.assertEqual(records[0]['error_code'], 'refusal')
        self.assertEqual(summary['known_total_tokens'], 120)

    def test_truncated_response_retries_and_accounts_for_usage(self):
        records, summary = self.scenario('incomplete_recovery', [body('{', status='incomplete'), body(valid_text())])
        self.assertEqual(records[0]['error_code'], 'incomplete')
        self.assertEqual(summary['known_total_tokens'], 240)

    def test_key_echo_cannot_leak_to_artifacts(self):
        records, summary = self.scenario('key_echo_redaction', ['key_echo'])
        self.assertIn('[REDACTED]', records[0]['response'])
