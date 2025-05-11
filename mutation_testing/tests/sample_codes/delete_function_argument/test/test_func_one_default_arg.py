import unittest

from mutation_testing.tests.sample_codes.delete_function_argument.code.func_one_default_arg import call_func


class TestFuncOneDefaultArg(unittest.TestCase):
    def test_func(self):
        res1, res2, res3, res4 = call_func()
        self.assertEqual(res1, 3)
        self.assertEqual(res2, 3)
        self.assertEqual(res3, 3)
        self.assertEqual(res4, 2)
