import unittest

from mutation_testing.tests.sample_codes.delete_expressions_if.code.multiple_mix_exp import condition_stmt


class TestMultipleMixExp(unittest.TestCase):
    def test_condition_stmt(self):
        self.assertTrue(condition_stmt(True, True, False))
        self.assertFalse(condition_stmt(False, False, True))
        self.assertFalse(condition_stmt(False, False, False))
        self.assertTrue(condition_stmt(True, True, True))
