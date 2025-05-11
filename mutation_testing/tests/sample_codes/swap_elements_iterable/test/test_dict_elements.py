import unittest

from mutation_testing.tests.sample_codes.swap_elements_iterable.code.dict_elements import func


class TestDictElements(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), 4)
