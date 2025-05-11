import unittest
from mutation_testing.tests.sample_codes.change_used_attribute.code.attribute_dynamic import func


class TestAttributeDynamic(unittest.TestCase):
    def test_attribute_dynamic(self):
        self.assertEqual(func(), 90)
