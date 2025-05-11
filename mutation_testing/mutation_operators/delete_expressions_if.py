import ast
from copy import deepcopy
import random

from mutation_testing.mutation_exceptions import OperatorMutateError
from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus, HookName


class DeleteExpressionsIf(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            static_analysis=True,
            dynamic_analysis=False,
            node_condition=DeleteExpressionsIf.get_node_condition
        )

    @staticmethod
    def get_node_condition(node):
        if isinstance(node, (ast.If, ast.While)):
            if isinstance(node.test, ast.BoolOp):
                return True
            elif isinstance(node.test, ast.Compare):
                return True
        if hasattr(node, 'value'):
            if isinstance(node.value, ast.BoolOp):
                return True
            elif isinstance(node.value, ast.Compare):
                return True
        return False

    @staticmethod
    def mutate(node, **kwargs):
        mutated_node = deepcopy(node)
        if hasattr(mutated_node, 'test'):
            if isinstance(mutated_node.test, ast.BoolOp):
                idx = random.randint(0, len(mutated_node.test.values) - 1)
                mutated_node.test.values.pop(idx)
            elif isinstance(mutated_node.test, ast.Compare):
                idx = random.randint(0, len(mutated_node.test.ops) - 1)
                mutated_node.test.ops.pop(idx)
            return mutated_node

        if hasattr(mutated_node, 'value'):
            if isinstance(mutated_node.value, ast.BoolOp):
                idx = random.randint(0, len(mutated_node.value.values) - 1)
                mutated_node.value.values.pop(idx)
            elif isinstance(mutated_node.value, ast.Compare):
                idx = random.randint(0, len(mutated_node.value.ops) - 1)
                mutated_node.value.ops.pop(idx)
            return mutated_node

        raise OperatorMutateError("Error in DeleteExpressionsIf.mutate", DeleteExpressionsIf, node)

    @staticmethod
    def _is_static_pattern(node):
        if isinstance(node, (ast.If, ast.While)):
            if isinstance(node.test, ast.BoolOp):
                if len(node.test.values) > 1:
                    return PatternStatus.STATIC
            elif isinstance(node.test, ast.Compare):
                if len(node.test.ops) > 1:
                    return PatternStatus.STATIC
        if hasattr(node, 'value'):
            if isinstance(node.value, ast.BoolOp):
                if len(node.value.values) > 1:
                    return PatternStatus.STATIC
            elif isinstance(node.value, ast.Compare):
                if len(node.value.ops) > 1:
                    return PatternStatus.STATIC
        return PatternStatus.NOT_FOUND
