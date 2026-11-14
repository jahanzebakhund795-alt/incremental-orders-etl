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
        self.assertEqual(result['attempts']['extract'],2)
        self.assertEqual(result['states']['publish'],'failed')
        self.assertEqual(result['states']['dashboard'],'blocked')
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['tasks']['extract']['depends'] = ['dashboard']
        with self.assertRaises(ValueError):
            run(data)
        with self.assertRaises(ValueError):
            run({'tasks':{'a':{'depends':['missing'],'retries':0,'fail_first':0}}})


if __name__ == '__main__':
    unittest.main()
