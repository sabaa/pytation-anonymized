import unittest

from mutation_testing.tests.sample_codes.delete_elements_iterable.code.multiple_iterator import multiple_iterator


class TestMultipleIterator(unittest.TestCase):
    def test_multiple_iterator(self):
        self.assertEqual(multiple_iterator(), {'a': 1, 'b': 4, 'c': 9})