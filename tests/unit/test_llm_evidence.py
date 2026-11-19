from pathlib import Path
import json
import re
import unittest

from modernize.llm_prompts import load_prompt, strict_json
from modernize.llm_run import usage_summary

ROOT = Path(__file__).resolve().parents[2]


class LLMEvidenceTests(unittest.TestCase):
    def test_recorded_retries_usage_and_redaction_recompute(self):
        path = ROOT / 'docs/evidence/cp4.json'
        evidence = json.loads(path.read_text())
        self.assertIsNone(re.search(r'\bsk-[A-Za-z0-9_-]{20,}', path.read_text()))
        self.assertEqual(evidence['sdk']['paid_provider_calls'], 0)
        scenarios = evidence['sdk']['scenarios']
        self.assertEqual(len(scenarios), 8)
        for scenario in scenarios + [evidence['mock_failure']]:
            summary = usage_summary(scenario['attempts'])
            self.assertTrue(all(scenario['summary'][key] == value for key, value in summary.items()))
            if 'intercepted_requests' in scenario:
                self.assertEqual(scenario['intercepted_requests'], summary['attempts'])
            for attempt in scenario['attempts']:
                prompt = load_prompt(attempt['prompt_version'])
                if attempt['validation']['status'] == 'passed':
                    prompt.response_model.model_validate(strict_json(attempt['response']), strict=True)
        malformed = next(s for s in scenarios if s['name'] == 'malformed_failure')
        self.assertEqual(malformed['summary']['status'], 'failed')
        self.assertEqual(len(malformed['attempts']), 3)
        self.assertIn('Previous response failed validation', malformed['attempts'][1]['prompt'])
        self.assertEqual(evidence['mock_failure']['summary']['evidence_kind'], 'mock')
        transient = next(s for s in scenarios if s['name'] == 'timeout_rate_limit_recovery')
        self.assertEqual(transient['summary']['unknown_usage_attempts'], 2)
        self.assertFalse(transient['summary']['cost_complete'])
