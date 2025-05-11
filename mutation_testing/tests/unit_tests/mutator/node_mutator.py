import unittest
import ast

from mutation_testing.mutator.node_mutator import NodeReplacer, mutate_source_tree


class TestNodeReplacer(unittest.TestCase):
    def test_replace_node(self):
        source_code = "x = 42"
        source_tree = ast.parse(source_code)
        old_node = source_tree.body[0]
        new_node = ast.parse("y = 10").body[0]
        replacer = NodeReplacer(old_node, new_node)
        modified_tree = replacer.visit(source_tree)
        self.assertEqual(ast.dump(modified_tree), ast.dump(ast.parse("y = 10")))


class TestMutateSourceTree(unittest.TestCase):
    def test_mutate_source_tree(self):
        source_code = "x = 42"
        source_tree = ast.parse(source_code)
        old_node = source_tree.body[0]
        new_node = ast.parse("y = 10").body[0]
        mutated_tree = mutate_source_tree(old_node, new_node, source_tree)
        self.assertEqual(ast.dump(mutated_tree), ast.dump(ast.parse("y = 10")))
