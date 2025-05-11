import unittest
from mutation_testing.tests.sample_codes.delete_method_call.code.simple_method import func


class TestSimpleMethod(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), 20)
