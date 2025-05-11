import unittest

from mutation_testing.tests.sample_codes.delete_function_argument.code.func_kwargs import call_func


class TestFuncKwargs(unittest.TestCase):
    def test_func(self):
        res1, res2, res3, res4, res5 = call_func()
        self.assertEqual(res1, 'a is found')
        self.assertEqual(res2, 'b is found')
        self.assertEqual(res3, 'neither a nor b is found')
        self.assertEqual(res4, 'a is found')
        self.assertEqual(res5, 'a is found')
