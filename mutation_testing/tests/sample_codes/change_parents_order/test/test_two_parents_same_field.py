import unittest

from ..code.two_parents_same_field import func


class TestTwoParentsSameField(unittest.TestCase):
    def test_func(self):
        result = func()
        self.assertEqual(result[0], "Method 1 from parent 1. parameter = parameter 1.")
        self.assertEqual(result[1], "Method 2 from parent 2. parameter = parameter 1.")
