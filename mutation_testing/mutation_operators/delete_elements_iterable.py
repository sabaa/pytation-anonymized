import ast
from copy import deepcopy
import random

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus
from mutation_testing.mutation_exceptions import OperatorMutateError

ITERABLE_TYPES = (ast.List, ast.Tuple, ast.Set, ast.Dict)


class DeleteElementsIterable(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            static_analysis=True,
            dynamic_analysis=False,
            node_type=ITERABLE_TYPES,
        )

    @staticmethod
    def _is_static_pattern(node):
        if isinstance(node, ITERABLE_TYPES):
            if hasattr(node, 'elts'):
                if len(node.elts) > 0:
                    return PatternStatus.STATIC
            elif hasattr(node, 'keys') and hasattr(node, 'values'):
                if len(node.keys) > 0 and len(node.values) > 0:
                    return PatternStatus.STATIC
            else:
                print('Error: Unknown iterable type')
                return PatternStatus.NOT_FOUND
        return PatternStatus.NOT_FOUND

    @staticmethod
    def mutate(node, **kwargs):
        mutated_node = deepcopy(node)
        try:
            if isinstance(mutated_node, ast.Dict):
                idx = random.randint(0, len(mutated_node.keys) - 1)
                mutated_node.keys.pop(idx)
                mutated_node.values.pop(idx)
                return mutated_node
            if isinstance(mutated_node, ast.Set):
                mutated_node.elts.pop()
                return mutated_node
            if isinstance(mutated_node, ast.List) or isinstance(mutated_node, ast.Tuple):
                idx = random.randint(0, len(mutated_node.elts) - 1)
                mutated_node.elts.pop(idx)
                return mutated_node
        except Exception as e:
            raise OperatorMutateError(e, DeleteElementsIterable, node)
