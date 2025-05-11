import unittest

from mutation_testing.tests.sample_codes.delete_elements_iterable.code.working_with_list import accessing_list_items


class TestWorkingWithList(unittest.TestCase):
    def test_accessing_list_items(self):
        self.assertEqual(accessing_list_items(), [1, 4, 9, 16, 25])
