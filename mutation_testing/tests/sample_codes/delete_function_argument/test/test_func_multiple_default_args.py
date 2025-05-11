import unittest

from mutation_testing.tests.sample_codes.delete_function_argument.code.func_multiple_default_args import call_func


class TestFuncMultipleArgs(unittest.TestCase):
    def test_func(self):
        res1, res2, res3 = call_func()
        self.assertEqual(res1, 3)
        self.assertEqual(res2, 6)
        self.assertEqual(res3, 8)
