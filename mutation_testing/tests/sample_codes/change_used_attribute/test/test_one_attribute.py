import unittest
from mutation_testing.tests.sample_codes.change_used_attribute.code.one_attribute import func


class TestOneAttribute(unittest.TestCase):
    def test_attribute_init(self):
        self.assertEqual(func(), "John")
