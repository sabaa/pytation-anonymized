import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.range_to_list_conversion import (
    range_to_list_conversion)


class TestRangeToListConversion(unittest.TestCase):
    def test_range_to_list_conversion(self):
        self.assertEqual(range_to_list_conversion(1, 4), [1, 2, 3])
        self.assertEqual(range_to_list_conversion(1, 4, 2), [1, 3])
