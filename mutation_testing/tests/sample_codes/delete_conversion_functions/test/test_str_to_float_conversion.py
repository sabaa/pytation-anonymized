import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.str_to_float_conversion import (
    str_to_float_conversion)


class TestStrToFloatConversion(unittest.TestCase):
    def test_str_to_float_conversion(self):
        self.assertEqual(str_to_float_conversion('1.5'), 1.5)
