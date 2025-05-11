import unittest

from mutation_testing.tests.sample_codes.swap_elements_iterable.code.multiple_return import func


class TestMultipleReturn(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(1), (3, 'hi', [4, 5]))
