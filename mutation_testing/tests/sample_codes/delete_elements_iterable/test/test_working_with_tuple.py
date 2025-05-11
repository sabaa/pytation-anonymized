import unittest

from mutation_testing.tests.sample_codes.delete_elements_iterable.code.working_with_tuple import working_with_tuples


class TestWorkingWithTuple(unittest.TestCase):
    def test_working_with_tuples(self):
        self.assertEqual(working_with_tuples(), (1, 4, 9, 16, 25))
