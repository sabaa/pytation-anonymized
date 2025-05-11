import unittest

from ..code.multi_level_inheritance import func


class TestMultiLevelInheritance(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), "Method 3 from Parent 2. Attribute: Attribute from Parent 1.")
