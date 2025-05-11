import unittest

from ..code.init_inheritance import func


class TestInitInheritance(unittest.TestCase):
    def test_func(self):
        self.assertEqual(func(), "Initializing Parent 1")
