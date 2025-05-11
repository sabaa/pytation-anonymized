import ast

class ASTExtractor(ast.NodeTransformer):
    """
    This class is used to extract all the nodes from the AST and also set the parent of each node
    It also removes type annotations from the AST
    usage:
        ast_tree = ast.parse(code)
        extractor = ASTExtractorParents()
        extractor.visit(ast_tree)
        nodes = extractor.get_nodes()

    """
    parent = None

    def __init__(self):
        self.nodes = []

    @staticmethod
    def remove_type_annotations(node):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                arg.annotation = None
            node.returns = None

        if isinstance(node, ast.AnnAssign):
            node = ast.Assign(
                targets=[node.target],
                value=node.value,
                lineno=node.lineno,
                col_offset=node.col_offset,
                end_lineno=node.end_lineno,
                end_col_offset=node.end_col_offset
            )

        return node

    def visit(self, node):
        node = ASTExtractor.remove_type_annotations(node)

        self.nodes.append(node)
        node.parent = self.parent
        self.parent = node
        node = super().visit(node)
        if isinstance(node, ast.AST):
            self.parent = node.parent

        return node

    def get_nodes(self):
        return self.nodes
