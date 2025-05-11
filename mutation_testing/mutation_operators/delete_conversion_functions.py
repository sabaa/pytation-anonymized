import ast

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus, HookName
from mutation_testing.mutation_exceptions import OperatorMutateError

CONVERSION_FUNCTIONS = {
    "int": int, "float": float, "complex": complex,
    "str": str, "ord": ord, "chr": chr, "bin": bin, "hex": hex, "oct": oct,
    "bool": bool, "list": list, "dict": dict, "set": set, "tuple": tuple,
    "frozenset": frozenset, "bytes": bytes, "bytearray": bytearray, "memoryview": memoryview
}


class DeleteConversionFunctions(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            hook_name=HookName.POST_CALL,
            static_analysis=False,
            dynamic_analysis=True,
            node_type=ast.Call,
        )

    @staticmethod
    def mutate(node, **kwargs):
        try:
            return node.args[0]
        except Exception as e:
            raise OperatorMutateError(e, DeleteConversionFunctions, node)

    @staticmethod
    def _is_dynamic_pattern(dynamic_data):
        call = dynamic_data.get("call", None)
        call_name = getattr(call, '__name__', None)
        if call_name and call_name in CONVERSION_FUNCTIONS.keys():
            positional_args = dynamic_data.get('pos_args', None)
            kw_args = dynamic_data.get('kw_args', None)
            args_count = len(positional_args) + len(kw_args.keys())
            if args_count != 1:
                return PatternStatus.NOT_FOUND
            if positional_args:
                is_equivalent = DeleteConversionFunctions._is_equivalent_pattern(call_name, positional_args[0])
                if is_equivalent:
                    return PatternStatus.EQUIVALENT
            return PatternStatus.DYNAMIC
        return PatternStatus.NOT_FOUND

    @staticmethod
    def _is_equivalent_pattern(function_name, argument):
        func_type = CONVERSION_FUNCTIONS.get(function_name, None)
        if isinstance(argument, func_type):
            return True
