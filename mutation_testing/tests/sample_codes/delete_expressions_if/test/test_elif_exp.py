import unittest

from mutation_testing.tests.sample_codes.delete_expressions_if.code.elif_exp import condition_stmt


class TestElifExp(unittest.TestCase):
    def test_condition_stmt(self):
        self.assertTrue(condition_stmt(True, True, False))
        self.assertFalse(condition_stmt(True, False, True))
        self.assertFalse(condition_stmt(False, False, False))
