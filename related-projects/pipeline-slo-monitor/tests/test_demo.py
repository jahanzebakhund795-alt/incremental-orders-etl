import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertAlmostEqual(result['good_event_ratio'],1/3)
        self.assertEqual(result['p95_ms'],700)
        self.assertEqual(result['freshness_seconds'],100)
        self.assertFalse(result['freshness_alert'])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['runs'] = [{'ok':False,'latency_ms':10,'completed_at':1000}]
        self.assertTrue(run(data)['freshness_alert'])
        self.assertIsNone(run(data)['freshness_seconds'])
        data['target'] = 1
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
