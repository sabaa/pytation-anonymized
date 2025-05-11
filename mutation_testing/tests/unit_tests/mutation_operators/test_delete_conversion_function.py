import unittest
import ast

from mutation_testing.mutation_operators import PatternStatus, DeleteConversionFunctions
from mutation_testing.mutation_exceptions import OperatorMutateError


class TestDeleteConversionFunctions(unittest.TestCase):
    def setUp(self):
        self.operator = DeleteConversionFunctions()

    def test_is_pattern_with_valid_dynamic_data(self):
        dynamic_data = {"call": ast.Call(func=ast.Name(id="int", ctx=ast.Load()), args=[ast.Num(n=42)], keywords=[])}
        result = self.operator.get_pattern_status(dynamic_data)
        self.assertEqual(result, PatternStatus.DYNAMIC)

    def test_is_pattern_with_equivalent_dynamic_data(self):
        dynamic_data = {"call": ast.Call(func=ast.Name(id="str", ctx=ast.Load()), args=[ast.Str(s="42")], keywords=[])}
        result = self.operator.get_pattern_status(dynamic_data)
        self.assertEqual(result, PatternStatus.EQUIVALENT)

    def test_is_pattern_with_non_conversion_function_call(self):
        dynamic_data = {
            "call": ast.Call(func=ast.Name(id="len", ctx=ast.Load()), args=[ast.Str(s="hello")], keywords=[])}
        result = self.operator.get_pattern_status(dynamic_data)
        self.assertEqual(result, PatternStatus.NOT_FOUND)

    def test_mutate_with_valid_node(self):
        code = ast.parse("result = int(42)")
        result = self.operator.mutate(code.body[0].value)
        self.assertEqual(ast.dump(result), '42')

    def test_mutate_with_invalid_node(self):
        code = ast.parse("result = len('hello')")
        with self.assertRaises(OperatorMutateError):
            self.operator.mutate(code.body[0].value)

    def test_is_equivalent_pattern_with_matching_argument_type(self):
        result = self.operator._is_equivalent_pattern("int", ast.Num(n=42))
        self.assertTrue(result)

    def test_is_equivalent_pattern_with_non_matching_argument_type(self):
        result = self.operator._is_equivalent_pattern("int", ast.Str(s="42"))
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
