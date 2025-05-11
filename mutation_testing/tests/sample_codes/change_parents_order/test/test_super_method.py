import unittest

from ..code.super_method import func


class TestSuperMethod(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), "Method from Parent 2 (Child)")
