import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.same_type_conversion import (
    same_type_conversion_str,
    same_type_conversion_int,
    same_type_conversion_float,
    same_type_conversion_list,
    same_type_conversion_bool
)


class TestIntToStrConversion(unittest.TestCase):
    def test_same_type_conversion_str(self):
        self.assertEqual(same_type_conversion_str('1'), '1')

    def test_same_type_conversion_int(self):
        self.assertEqual(same_type_conversion_int(1), 1)

    def test_same_type_conversion_float(self):
        self.assertEqual(same_type_conversion_float(1.0), 1.0)

    def test_same_type_conversion_list(self):
        self.assertEqual(same_type_conversion_list([1, 2, 3]), [1, 2, 3])

    def test_same_type_conversion_bool(self):
        self.assertEqual(same_type_conversion_bool(True), True)
        self.assertEqual(same_type_conversion_bool(False), False)
