import ast
import inspect

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus, HookName
from mutation_testing.mutation_exceptions import OperatorMutateError, MutationException


class DeleteAttributeAccess(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            hook_name=HookName.READ_ATTRIBUTE,
            static_analysis=False,
            dynamic_analysis=True,
            node_type=ast.Attribute,
        )

    @staticmethod
    def mutate(node, **kwargs):
        try:
            if isinstance(node, ast.Attribute):
                return node.value
            raise OperatorMutateError("Node is not an attribute access", DeleteAttributeAccess, node)
        except MutationException as e:
            return node

    @staticmethod
    def _is_dynamic_pattern(attribute_data):
        attr = attribute_data.get("val", None)
        if attr is None:
            return PatternStatus.NOT_FOUND, None
        if inspect.ismethod(attr):
            return PatternStatus.NOT_FOUND, None
        if callable(attr):
            return PatternStatus.NOT_FOUND, None
        return PatternStatus.DYNAMIC, None
