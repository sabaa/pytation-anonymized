import unittest

from mutation_testing.tests.sample_codes.delete_expressions_if.code.two_or_exp import condition_stmt


class TestTwoOrExp(unittest.TestCase):
    def test_condition_stmt(self):
        self.assertTrue(condition_stmt(True, True))
        self.assertTrue(condition_stmt(True, False))
        self.assertTrue(condition_stmt(False, True))
        self.assertFalse(condition_stmt(False, False))
