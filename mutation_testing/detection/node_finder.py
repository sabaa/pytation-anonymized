import ast


class LocationVisitor(ast.NodeVisitor):
    def __init__(self, location, node_type=None, node_type_name=None, node_condition=None):
        self.location = location
        self.node_type = node_type
        self.node_type_name = node_type_name
        self.node_condition = node_condition
        self.found_node = None

    def visit(self, node):
        if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
            start_location = (node.lineno, node.col_offset)
            end_location = (node.end_lineno, node.end_col_offset)

            if start_location <= self.location <= end_location:
                if self.node_condition is not None:
                    if self.node_condition(node):
                        self.found_node = node
                elif self.node_type is None or isinstance(node, self.node_type):
                    if self.node_type_name is not None:
                        if self.is_node_name_type(node, self.node_type_name):
                            self.found_node = node
                    elif self.node_type_name is None:
                        self.found_node = node

        self.generic_visit(node)

    @staticmethod
    def is_node_name_type(node, node_type_name):
        return hasattr(node, 'func') and hasattr(node.func, 'attr') and node.func.attr == node_type_name


class MultipleCallVisitor(ast.NodeVisitor):
    def __init__(self, location, node_type=None, node_type_name=None,):
        self.location = location
        self.node_type = node_type
        self.node_type_name = node_type_name
        self.found_node = []


    def visit(self, node):
        if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
            start_location = (node.lineno, node.col_offset)
            end_location = (node.end_lineno, node.end_col_offset)
            if start_location <= self.location <= end_location:
                if self.node_type is None or isinstance(node, self.node_type):
                    if self.node_type_name is not None:
                        if self.is_node_name_type(node, self.node_type_name):
                            self.found_node.append(node)
                    elif self.node_type_name is None:
                        self.found_node.append(node)

        self.generic_visit(node)

    @staticmethod
    def is_node_name_type(node, node_type_name):
        return hasattr(node, 'func') and hasattr(node.func, 'attr') and node.func.attr == node_type_name


def get_ast_node_multiple_calls(pattern_location, node_type=None, node_type_name=None, node_name=None):
    filename = pattern_location.filename
    start_line = pattern_location.start_line
    start_col = pattern_location.start_col
    with open(filename) as f:
        source_code = f.read()
    source_code_tree = ast.parse(source_code)
    visitor = MultipleCallVisitor((start_line, start_col), node_type=node_type, node_type_name=node_type_name)
    visitor.visit(source_code_tree)
    found_nodes = visitor.found_node
    if len(found_nodes) == 0:
        return None

    candidate = None
    for found_node in found_nodes:
        if hasattr(found_node, 'func') and ((hasattr(found_node.func, 'attr') and found_node.func.attr == node_name) or (
                hasattr(found_node.func, 'id') and found_node.func.id == node_name)):
            candidate = found_node
            break

    if candidate is not None:
        return candidate
    return found_nodes[-1]


class NameVisitor(ast.NodeVisitor):
    def __init__(self, node_name, node_type):
        self.node_name = node_name
        self.node_type = node_type
        self.found_node = None

    def visit(self, node):
        if hasattr(node, 'name') and node.name == self.node_name:
            if self.node_type is None or isinstance(node, self.node_type):
                self.found_node = node

        self.generic_visit(node)


def get_ast_node_by_location(pattern_location, node_type=None, node_type_name=None, node_condition=None):
    filename = pattern_location.filename
    start_line = pattern_location.start_line
    start_col = pattern_location.start_col
    with open(filename) as f:
        source_code = f.read()
    source_code_tree = ast.parse(source_code)
    visitor = LocationVisitor(
        (start_line, start_col), node_type=node_type, node_type_name=node_type_name, node_condition=node_condition)
    visitor.visit(source_code_tree)
    found_node = visitor.found_node
    return found_node


def get_ast_node_by_name(node_name, filename, node_type):
    with open(filename) as f:
        source_code = f.read()
    source_code_tree = ast.parse(source_code)
    visitor = NameVisitor(node_name, node_type)
    visitor.visit(source_code_tree)
    found_node = visitor.found_node
    return found_node
