import unittest

from mutation_testing.tests.sample_codes.delete_expressions_if.code.multiple_or_exp import condition_stmt


class TestMultipleOrExp(unittest.TestCase):
    def test_condition_stmt(self):
        self.assertTrue(condition_stmt(True, True, False))
        self.assertFalse(condition_stmt(False, False, False))
        self.assertTrue(condition_stmt(False, False, True))
