import unittest

from mutation_testing.tests.sample_codes.swap_elements_iterable.code.multiple_iterable import func


class TestMultipleIterable(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), 'a,b')
