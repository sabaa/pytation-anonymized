import unittest
from mutation_testing.tests.sample_codes.delete_method_call.code.dynamic_method import func


class TestDynamicMethod(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), "John")
