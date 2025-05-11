import ast


class NodeReplacer(ast.NodeTransformer):
    def __init__(self, node, new_node):
        self.node = node
        self.new_node = new_node

    def visit(self, node):
        if ast.dump(node) == ast.dump(self.node):
            return self.new_node
        return self.generic_visit(node)


def mutate_source_tree(node, new_node, source_code_tree):
    replacer = NodeReplacer(node, new_node)
    return replacer.visit(source_code_tree)
