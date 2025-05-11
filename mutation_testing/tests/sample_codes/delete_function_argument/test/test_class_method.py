import unittest

from mutation_testing.tests.sample_codes.delete_function_argument.code.class_method import call_some_method


class TestClassMethod(unittest.TestCase):
    def test_call_some_method(self):
        self.assertEqual(call_some_method(), (8, 3, 3))
