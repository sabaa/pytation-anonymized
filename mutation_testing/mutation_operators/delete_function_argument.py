import ast
import types
import inspect
from copy import deepcopy

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus, HookName
from mutation_testing.mutation_exceptions import OperatorIsDynamicError, OperatorMutateError


class DeleteFunctionArgument(BaseMutationOperator):
    def __init__(self):
        super().__init__(
            static_analysis=False,
            dynamic_analysis=True,
            hook_name=HookName.PRE_CALL,
            node_type=ast.Call,
        )

    @staticmethod
    def _is_dynamic_pattern(dynamic_data):
        """
        param: means name of the parameter
        arg: means the argument passed to the function (values)
        """
        try:
            function = dynamic_data.get("function", None)
            pos_args = dynamic_data.get('pos_args_copy', [])
            kw_args = dynamic_data.get('kw_args_copy', {})
            try:
                args, varargs, varkw, defaults, _, _, _ = inspect.getfullargspec(function)
            except Exception as e:
                return PatternStatus.NOT_FOUND, None
            required_params = args[:-len(defaults)] if defaults else args
            is_method = inspect.ismethod(function)
            is_class = inspect.isclass(function)

            removable_keys = []

            if is_method or is_class:
                required_params = required_params[1:]

            if not (defaults or varkw or varargs):
                return PatternStatus.NOT_FOUND, None

            mapping = {}
            required_args_index = 0
            removable_arg_positions = []
            double_starred_arg_position = 0
            removable_double_starred_arg_positions = []
            for pos, (star, arg) in enumerate(pos_args):
                if star == '':
                    if len(required_params) > required_args_index:
                        mapping[args[required_args_index]] = (pos, arg)
                        required_args_index += 1
                    else:
                        removable_arg_positions.append(pos)
                elif star == '*':
                    if len(required_params) > required_args_index:
                        required_args_index += len(arg)
                    else:
                        removable_arg_positions.append(pos)
                else:
                    if not any([k in required_params for k in arg.keys()]):
                        removable_double_starred_arg_positions.append(double_starred_arg_position)
                    double_starred_arg_position += 1

            for key in kw_args.keys():
                if key not in required_params:
                    removable_keys.append(key)

            if removable_arg_positions or removable_keys or removable_double_starred_arg_positions:
                return PatternStatus.DYNAMIC, {
                    "removable_positions": removable_arg_positions,
                    "removable_keys": removable_keys,
                    "removable_double_starred_arg_positions": removable_double_starred_arg_positions,
                }
            return PatternStatus.NOT_FOUND, None
        except ValueError as ve:
            if 'no signature found for builtin' in str(ve):
                return PatternStatus.NOT_FOUND, None
            raise OperatorIsDynamicError(ve, DeleteFunctionArgument, dynamic_data)
        except Exception as e:
            raise OperatorIsDynamicError(e, DeleteFunctionArgument, dynamic_data)

    @staticmethod
    def mutate(node: ast.Call, **kwargs):
        mutated_node: ast.Call = deepcopy(node)
        pattern_data = kwargs.get("pattern_data", None)
        if pattern_data is None:
            raise OperatorMutateError("No additional data found", DeleteFunctionArgument, node)
        dynamic_data = pattern_data.dynamic_data
        if (candidate_index := dynamic_data.get('candidate_index', None)) is not None:
            mutated_node.args.pop(candidate_index)
            return mutated_node
        elif (candidate_kw := dynamic_data.get('candidate_kw', None)) is not None:
            for i, arg in enumerate(mutated_node.keywords):
                if arg.arg == candidate_kw:
                    mutated_node.keywords.pop(i)
                    return mutated_node
        elif (candidate_double_starred_arg_position := dynamic_data.get('candidate_dstarred_pos', None)) is not None:
            idx = 0
            for i, arg in enumerate(mutated_node.keywords):
                if arg.arg is None:
                    if idx == candidate_double_starred_arg_position:
                        mutated_node.keywords.pop(i)
                        return mutated_node
                    idx += 1
        raise OperatorMutateError("No candidate index or keyword found", DeleteFunctionArgument, node)
