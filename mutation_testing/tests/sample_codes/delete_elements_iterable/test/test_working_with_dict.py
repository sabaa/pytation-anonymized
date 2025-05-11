import unittest

from mutation_testing.tests.sample_codes.delete_elements_iterable.code.working_with_dict import func


class TestWorkingWithDict(unittest.TestCase):
    def test_working_with_dict(self):
        self.assertEqual(func(), {'b': 5, 'd': 4, 'c': 3})
