import unittest

from mutation_testing.tests.sample_codes.delete_function_argument.code.func_args import call_func


class TestFuncArgs(unittest.TestCase):
    def test_func(self):
        self.assertEqual(call_func(), 15)
