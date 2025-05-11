import unittest

from mutation_testing.tests.sample_codes.delete_expressions_if.code.two_and_exp import condition_stmt


class TestTwoAndExp(unittest.TestCase):
    def test_condition_stmt(self):
        self.assertTrue(condition_stmt(True, True))
        self.assertFalse(condition_stmt(True, False))
        self.assertFalse(condition_stmt(False, False))
