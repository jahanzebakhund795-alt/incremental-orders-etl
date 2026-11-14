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
        self.assertEqual(result['orders'], [['o1', 1500, 2], ['o2', 700, 1]])
        self.assertEqual(result['revenue_cents'], 2200)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['batches'] += copy.deepcopy(data['batches'])
        self.assertEqual(run(data)['revenue_cents'], 2200)
        data['batches'].append([{'id':'bad','amount_cents':-1,'version':1}])
        with self.assertRaises(Exception):
            run(data)


if __name__ == '__main__':
    unittest.main()
