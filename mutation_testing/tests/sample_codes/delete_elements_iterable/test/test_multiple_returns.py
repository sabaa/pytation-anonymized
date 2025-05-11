import unittest

from mutation_testing.tests.sample_codes.delete_elements_iterable.code.multiple_returns import caller


class TestMultipleReturns(unittest.TestCase):
    def test_caller(self):
        self.assertEqual(caller(), (5, 'hello', [2, 3]))
