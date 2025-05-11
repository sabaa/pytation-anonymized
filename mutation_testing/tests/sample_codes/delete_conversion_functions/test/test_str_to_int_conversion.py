import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.str_to_int_conversion import (
    str_to_int_conversion)


class TestStrToIntConversion(unittest.TestCase):
    def test_str_to_int_conversion(self):
        self.assertEqual(str_to_int_conversion('1'), 1)
