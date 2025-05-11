import ast
import copy
import random

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus
from mutation_testing.mutation_exceptions import OperatorMutateError, MutationException, OperatorIsStaticError

SIMILAR_LIST = [
    ('zip', 'zip_longest'),  # add "from itertools import zip_longest" before
    ('map', 'filter'),
    ('remove', 'pop'),  # list.pop(index) -> list.remove(value)
    ('sort', 'sorted'),  # a.sort(arg) -> sorted(a, arg)
    ('extend', 'append'),  # if the function is 'append' then the arg should be iterable
    ('copy', 'deepcopy'),  # from copy import deepcopy
    ('isinstance', 'issubclass'),
    ('isdigit', 'isnumeric', 'isdecimal')
]

ITERABLE_TYPES = (ast.List, ast.Tuple, ast.Set, ast.Dict)


class SwitchSimilarFunctions(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            static_analysis=True,
            dynamic_analysis=False,
            node_type=ast.Call
        )

    @staticmethod
    def _is_static_pattern(node):
        if is_node_call(node):
            node_name = get_node_name(node)
            if node_name is None:
                raise OperatorIsStaticError("Node name is None", SwitchSimilarFunctions)
            for similar_pair in SIMILAR_LIST:
                if node_name in similar_pair:
                    if node_name == 'pop' and len(node.args) == 0:
                        return PatternStatus.NOT_FOUND
                    return PatternStatus.STATIC
        return PatternStatus.NOT_FOUND

    @staticmethod
    def mutate(node, **kwargs):
        mutated_node = copy.deepcopy(node)
        if is_node_call(mutated_node):
            node_name = get_node_name(mutated_node)
            if node_name is None:
                raise OperatorMutateError("Node name is None", SwitchSimilarFunctions, node)
            for similar_pair in SIMILAR_LIST:
                if node_name in similar_pair:
                    candidates_list = [x for x in similar_pair if x != node_name]
                    candidate = random.choice(candidates_list)
                    return create_new_node(mutated_node, candidate, **kwargs)

        raise OperatorMutateError("Error in SwitchSimilarFunctions.mutate", SwitchSimilarFunctions, node)


def get_node_name(node):
    if hasattr(node, 'func') and hasattr(node.func, 'id'):
        node_name = node.func.id
    elif hasattr(node, 'func') and hasattr(node.func, 'attr'):
        node_name = node.func.attr
    elif hasattr(node, 'name'):
        node_name = node.name
    else:
        node_name = None
    return node_name


def is_node_call(node):
    return isinstance(node, ast.Call)


def get_last_future_import_index(file_ast):
    last_future_import_index = -1
    for idx, stmt in enumerate(file_ast.body):
        if isinstance(stmt, ast.ImportFrom) and stmt.module == '__future__':
            last_future_import_index = idx
    return last_future_import_index


def add_import_to_file_ast(file_ast, module_name, import_name, alias_name=None):
    last_index = get_last_future_import_index(file_ast)
    file_ast.body.insert(last_index + 1, ast.ImportFrom(
        module=module_name, names=[ast.alias(name=import_name, asname=alias_name)], level=0))


def create_simple_call_node(node, candidate):
    return ast.Call(
        func=ast.Name(id=candidate), args=node.args, keywords=node.keywords)


def create_new_node(node, candidate, **kwargs):
    if candidate == 'zip':  # zip_longest -> zip
        return create_simple_call_node(node, candidate)

    elif candidate == 'zip_longest':  # zip -> zip_longest
        file_ast = kwargs.get('pattern_data').get('file_ast')
        add_import_to_file_ast(file_ast, 'itertools', 'zip_longest')
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='itertools'), attr='zip_longest'), args=node.args, keywords=node.keywords)

    elif candidate == 'map':  # filter -> map
        return create_simple_call_node(node, candidate)
    elif candidate == 'filter':  # map -> filter
        return create_simple_call_node(node, candidate)

    elif candidate == 'remove':  # pop -> remove
        if len(node.args) == 0:
            raise OperatorMutateError("pop should have an argument to mutate to 'remove", SwitchSimilarFunctions, node)
        return create_simple_call_node(node, candidate)

    elif candidate == 'pop':  # remove -> pop
        return create_simple_call_node(node, candidate)
    elif candidate == 'sort':  # sorted -> sort
        """
        Examples:
            - sorted(a) -> a.sort()
            - sorted(a, key=func) -> a.sort(key=func)
            - sorted(a, key=func, reverse=True) -> a.sort(key=func, reverse=True)
        """
        if len(node.args) > 0:
            return ast.Call(
                func=ast.Attribute(value=node.args[0], attr='sort'), args=node.args[1:],
                keywords=node.keywords)
        else:  # sorted(a) -> a.sort()
            return ast.Call(
                func=ast.Attribute(value=node.args[0], attr='sort'), args=[],
                keywords=node.keywords)

    elif candidate == 'sorted':  # sort -> sorted
        base = node.func.value
        return ast.Call(
            func=ast.Name(id='sorted'), args=[base] + node.args, keywords=node.keywords)
    elif candidate == 'extend':  # append -> extend
        return create_simple_call_node(node, candidate)
    elif candidate == 'append':  # extend -> append
        return create_simple_call_node(node, candidate)
    elif candidate == 'copy':  # deepcopy -> copy
        return create_simple_call_node(node, candidate)
    elif candidate == 'deepcopy':
        file_ast = kwargs.get('pattern_data').get('file_ast')
        add_import_to_file_ast(file_ast, 'copy', 'deepcopy', 'mutation_testing_copy')
        return ast.Call(
            func=ast.Attribute(value=ast.Name(id='mutation_testing_copy'), attr='deepcopy'),
            args=node.args,
            keywords=node.keywords
        )
    elif candidate == 'isinstance':  # issubclass -> isinstance
        return create_simple_call_node(node, candidate)
    elif candidate == 'issubclass':  # isinstance -> issubclass
        return create_simple_call_node(node, candidate)
    elif candidate == 'isdigit':
        return create_simple_call_node(node, candidate)
    elif candidate == 'isnumeric':
        return create_simple_call_node(node, candidate)
    elif candidate == 'isdecimal':
        return create_simple_call_node(node, candidate)
    else:
        raise OperatorMutateError(f"Unknown candidate {candidate}", SwitchSimilarFunctions, node)