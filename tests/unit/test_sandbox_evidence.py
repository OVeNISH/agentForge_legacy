"""Recompute CP3 assertions from committed live records without Docker."""

import base64
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import unittest

from modernize.sandbox import validate_result

ROOT = Path(__file__).resolve().parents[2]


class SandboxEvidenceTests(unittest.TestCase):
    def test_recorded_isolation_and_deterministic_replay(self):
        evidence = json.loads((ROOT / 'docs/evidence/cp3.json').read_text())
        by_image = defaultdict(lambda: defaultdict(list))
        probe_hash = hashlib.sha256(base64.b64decode(evidence['probe_base64'])).hexdigest()
        for item in evidence['records']:
            record = item['record']
            by_image[item['image']][item['case']].append(record)
            self.assertTrue(record['container_removed'])
            self.assertFalse(record['container_state']['Running'])
            self.assertEqual(record['source_sha256']['probe.py'], probe_hash)
            policy = record['isolation']
            self.assertEqual(policy['NetworkMode'], 'none')
            self.assertTrue(policy['ReadonlyRootfs'])
            self.assertEqual(policy['LogConfig']['Type'], 'none')
            self.assertTrue(all(m['type'] == 'tmpfs' or (m['type'] == 'bind' and not m['rw'])
                                for m in policy['Mounts']))
            if record['result'] is not None:
                validate_result(record['result'])
        self.assertEqual(len(by_image), 2)
        for image, cases in by_image.items():
            with self.subTest(image=image):
                first, second = cases['deterministic']
                self.assertEqual(first['result'], second['result'])
                self.assertEqual(cases['network'][0]['result']['status'], 'exception')
                self.assertEqual(cases['memory'][0]['result']['exception']['name'], 'MemoryError')
                self.assertEqual(cases['cpu'][0]['result']['target_exit_code'], -9)
                self.assertEqual(cases['sleep'][0]['result']['status'], 'timeout')
                denied = cases['filesystem'][0]['result']['value']['items'][1]['items']
                self.assertEqual([v['value'] for v in denied], ['30', '30', '30'])
                self.assertEqual(cases['fresh'][0]['result']['value'], {'type': 'bool', 'value': False})
                self.assertIsNone(cases['missing_outcome'][0]['result'])
                self.assertTrue(cases['missing_outcome'][0]['protocol_error'])
                self.assertEqual(cases['unsupported'][0]['result']['status'], 'capture_error')
