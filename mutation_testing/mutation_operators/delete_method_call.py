import ast
import inspect

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus, HookName
from mutation_testing.mutation_exceptions import OperatorMutateError, MutationException


class DeleteMethodCall(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            hook_name=HookName.POST_CALL,
            static_analysis=False,
            dynamic_analysis=True,
            node_type=ast.Call,
        )

    @staticmethod
    def mutate(node, **kwargs):
        """
        Example1: a = A()

        node (ast.call) -> func (ast.name) -> id (str 'A')

        Example2: a.method()

        node (ast.call) -> func (ast.attribute) -> value (ast.name) -> id (str 'a')
                                                -> attr (str 'method')

        Example3: super().__init__()

        node (ast.call) -> func (ast.attribute) -> value (ast.call) -> func (ast.name) -> id (str 'super')
                                                -> attr (str '__init__')
        """
        if isinstance(node, ast.Call):
            mutated_node = None
            if hasattr(node, 'func') and isinstance(node.func, ast.Attribute):
                mutated_node = node.func.value
            elif hasattr(node, 'func') and isinstance(node.func, ast.Name):
                mutated_node = node.func

            if mutated_node:
                return mutated_node
            raise OperatorMutateError("Error in DeleteMethodCall.mutate", DeleteMethodCall, node)

    @staticmethod
    def _is_dynamic_pattern(dynamic_data):
        call = dynamic_data.get("call", None)
        if not call:
            return PatternStatus.NOT_FOUND, None
        if inspect.ismethod(call):
            return PatternStatus.DYNAMIC, None
        return PatternStatus.NOT_FOUND, None
