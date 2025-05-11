import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.int_to_str_conversion import (
    int_to_str_conversion)


class TestIntToStrConversion(unittest.TestCase):
    def test_int_to_str_conversion(self):
        self.assertEqual(int_to_str_conversion(1), '1')
