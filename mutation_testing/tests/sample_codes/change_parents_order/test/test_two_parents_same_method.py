import unittest

from ..code.two_parents_same_method import func


class TestTwoParentsSameMethod(unittest.TestCase):
    def test_func(self):
        result = func()
        self.assertEqual(result, "Method from Parent 1 parameter: 1.")
