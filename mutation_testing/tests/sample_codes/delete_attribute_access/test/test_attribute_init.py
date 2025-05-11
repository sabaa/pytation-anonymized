import unittest
from mutation_testing.tests.sample_codes.change_used_attribute.code.attribute_init import func


class TestAttributeInit(unittest.TestCase):
    def test_attribute_init(self):
        self.assertEqual(func(), "John")
