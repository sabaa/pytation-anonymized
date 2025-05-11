import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.float_to_str_conversion import (
    float_to_str_conversion)


class TestFloatToStrConversion(unittest.TestCase):
    def test_float_to_str_conversion(self):
        self.assertEqual(float_to_str_conversion(1.5), '1.5')
