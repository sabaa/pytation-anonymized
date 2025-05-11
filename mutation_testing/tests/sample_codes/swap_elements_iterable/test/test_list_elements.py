import unittest

from mutation_testing.tests.sample_codes.swap_elements_iterable.code.list_elements import func


class TestListElements(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), [2, 3, 4])
