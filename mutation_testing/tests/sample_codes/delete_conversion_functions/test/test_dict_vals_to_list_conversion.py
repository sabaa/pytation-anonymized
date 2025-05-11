import unittest

from mutation_testing.tests.sample_codes.delete_conversion_functions.code.dict_vals_to_list_conversion import (
    dict_vals_to_list_conversion)


class TestDictValsToListConversion(unittest.TestCase):
    def test_dict_vals_to_list_conversion(self):
        input_dict = {'a': 1, 'b': 2}
        self.assertEqual(dict_vals_to_list_conversion(input_dict), [1, 2])
