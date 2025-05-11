import unittest
from mutation_testing.tests.sample_codes.switch_similar_functions.code.all_similars import *


class TestAllSimilars(unittest.TestCase):
    def test_zip_longest_func(self):
        self.assertEqual(zip_longest_func(), [(1, 4), (2, 5), (3, None)])

    def test_zip_func(self):
        self.assertEqual(zip_func(), [(1, 4), (2, 5)])

    def test_filter_func(self):
        self.assertEqual(filter_func(), [2, 3])

    def test_map_func(self):
        self.assertEqual(map_func(), [2, 3, 4])

    def test_remove_func(self):
        self.assertEqual(remove_func(), [1, 3])

    def test_pop_func(self):
        self.assertEqual(pop_func(), [1, 3])

    def test_sort_func(self):
        self.assertEqual(sort_func(), [1, 2, 3])

    def test_sorted_func(self):
        self.assertEqual(sorted_func(), [1, 2, 3])

    def test_extend_func(self):
        self.assertEqual(extend_func(), [1, 2, 3, 4, 5])

    def test_append_func(self):
        self.assertEqual(append_func(), [1, 2, 3, 4])

    def test_deep_copy_func(self):
        self.assertEqual(deep_copy_func(), [1, 2, 3])

    def test_copy_func(self):
        self.assertEqual(copy_func(), [1, 2, 3])

    def test_isinstance_func(self):
        self.assertEqual(isinstance_func(), True)

    def test_issubclass_func(self):
        self.assertEqual(issubclass_func(), True)

    def test_isnumeric_func(self):
        self.assertEqual(isnumeric_func(), True)

    def test_isdecimal_func(self):
        self.assertEqual(isdecimal_func(), True)

    def test_isdigit_func(self):
        self.assertEqual(isdigit_func(), True)
