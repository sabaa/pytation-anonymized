from typing import Any, Callable, Dict, Tuple, List
import inspect
import os

from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from dynapyt.utils.nodeLocator import get_node_by_location
from dynapyt.instrument.IIDs import Location as DynLocation

from mutation_testing.detection.pattern import PatternLocation, Pattern, PatternStatus, PatternData
from mutation_testing.detection.utils import store_patterns_to_file
from mutation_testing.constants import DYNAMIC_PATTERN_FILENAME
from mutation_testing.mutation_operators import MutationOperators, HookName
from mutation_testing.mutation_operators import CONVERSION_FUNCTIONS
from mutation_testing.config import ConfigManager


class OperatorAnalysis(BaseAnalysis):
    def __init__(self, output_dir=None):
        super(OperatorAnalysis, self).__init__()
        self.dynamic_patterns = []
        self.operators = {}
        if ConfigManager.get_config().logging:
            dyna_log_path = 'dyna_log.log'
            if os.path.exists(dyna_log_path):
                os.remove(dyna_log_path)
            self.log_file = open('dyna_log.log', 'a')

        for operator in MutationOperators.operators():
            if operator.hook_name and operator.hook_name not in self.operators.keys():
                self.operators[operator.hook_name] = []
            if operator.hook_name:
                self.operators[operator.hook_name].append(operator)

        self.unique_location_types = set()
        self.unique_hooks = set()
        self.unique_founds = set()

        self.pre_call_visited = set()

    def log(self, msg):
        if ConfigManager.get_config().logging:
            self.log_file.write(msg + '\n')
            self.log_file.flush()

    def post_call(
            self,
            dyn_ast: str,
            iid: int,
            result: Any,
            call: Callable,
            pos_args: Tuple,
            kw_args: Dict,
    ) -> Any:
        # not instrumenting __repr__ and __str__ methods to prevent infinite recursion
        name = getattr(call, '__name__', None)
        if name == '__repr__' or name == '__str__':
            return result

        if (dyn_ast, iid, PatternStatus.DYNAMIC) in self.unique_founds:
            return result

        if name is None or name not in CONVERSION_FUNCTIONS.keys():
            if ('call', dyn_ast, iid) in self.unique_hooks:
                return result
            self.unique_hooks.add(('call', dyn_ast, iid))
        if ConfigManager.get_config().logging:
            self.log(f'Post call: {dyn_ast}, {iid}')

        call_data = {
            "dyn_ast": dyn_ast,
            "iid": iid,
            "result": result,
            "call": call,
            "pos_args": pos_args,
            "kw_args": kw_args,
        }
        for operator in self.operators.get(HookName.POST_CALL, []):
            try:
                self.detect_pattern(operator, call_data)
            except Exception:
                if ConfigManager.get_config().logging:
                    self.log(f'Error in post_call operator: {operator} at {dyn_ast}, {iid}')

        return result

    def read_attribute(
            self,
            dyn_ast: str,
            iid: int,
            base: Any,
            name: str,
            val: Any
    ) -> Any:
        if ('attribute', dyn_ast, iid) in self.unique_hooks:
            return val
        self.unique_hooks.add(('attribute', dyn_ast, iid))

        if ConfigManager.get_config().logging:
            self.log(f'Read attribute: {dyn_ast}, {iid}')

        attribute_data = {
            "dyn_ast": dyn_ast,
            "iid": iid,
            "base": base,
            "name": name,
            "val": val,
        }
        for operator in self.operators.get(HookName.READ_ATTRIBUTE, []):
            try:
                self.detect_pattern(operator, attribute_data)
            except Exception:
                if ConfigManager.get_config().logging:
                    self.log(f'Error in read_attribute operator: {operator} at {dyn_ast}, {iid}')

        return val

    def pre_call(
            self,
            dyn_ast: str,
            iid: int,
            function: Callable,
            pos_args: Tuple,
            kw_args: Dict,
            pos_args_copy: List,
            kw_args_copy: List,
    ):
        name = getattr(function, '__name__', None)
        if name == '__repr__' or name == '__str__':
            return

        if ('pre_call', dyn_ast, iid) in self.pre_call_visited:
            return
        self.pre_call_visited.add(('pre_call', dyn_ast, iid))

        if (dyn_ast, iid, PatternStatus.DYNAMIC) in self.unique_founds:
            return

        if ConfigManager.get_config().logging:
            self.log(f'Pre call: {dyn_ast}, {iid}')

        call_data = {
            "dyn_ast": dyn_ast,
            "iid": iid,
            "function": function,
            "pos_args": pos_args,
            "kw_args": kw_args,
            "pos_args_copy": pos_args_copy,
            "kw_args_copy": kw_args_copy,
        }
        for operator in self.operators.get(HookName.PRE_CALL, []):
            try:
                if isinstance(operator, MutationOperators.DeleteFunctionArgument.value):
                    pattern_data_list = []
                    pattern_status, additional_data = operator.get_pattern_status(call_data)
                    if pattern_status == PatternStatus.DYNAMIC:
                        pattern_location, node = self.get_pattern_location_node(dyn_ast, iid)
                        if pattern_location is None:
                            pattern_location = PatternLocation(filename="unknown", node_name="unknown")
                        pattern_location.node_name = function.__name__
                        unique_identifier = (pattern_location.get_unique_value(), pattern_status)
                        if unique_identifier in self.unique_location_types:
                            continue
                        self.unique_location_types.add(unique_identifier)
                        if additional_data:
                            for key, value in additional_data.items():
                                if key == 'removable_positions':
                                    for candidate_index in value:
                                        pattern_data_list.append(
                                            PatternData(dynamic_data={'candidate_index': candidate_index}))
                                elif key == 'removable_keys':
                                    for candidate_kw in value:
                                        pattern_data_list.append(
                                            PatternData(dynamic_data={'candidate_kw': candidate_kw}))
                                elif key == 'removable_double_starred_arg_positions':
                                    for candidate_dstarred_pos in value:
                                        pattern_data_list.append(PatternData(
                                            dynamic_data={'candidate_dstarred_pos': candidate_dstarred_pos}))
                        pattern_list = []
                        for pattern_data in pattern_data_list:
                            pattern_list.append(Pattern(node, operator, pattern_status, pattern_location, pattern_data))
                        self.unique_founds.add((dyn_ast, iid, pattern_status))
                        self.dynamic_patterns.extend(pattern_list)

            except Exception:
                if ConfigManager.get_config().logging:
                    self.log(f'Error in pre_call operator: {operator} at {dyn_ast}, {iid}')

    def detect_pattern(self, operator, dynamic_data):
        dyn_ast = dynamic_data.get('dyn_ast')
        iid = dynamic_data.get('iid')
        pattern_status, additional_data = operator.get_pattern_status(dynamic_data)
        if pattern_status == PatternStatus.DYNAMIC or pattern_status == PatternStatus.EQUIVALENT:
            pattern_location, node = self.get_pattern_location_node(dyn_ast, iid)
            if pattern_location is None:
                pattern_location = PatternLocation(filename="unknown", node_name="unknown")
            if (pattern_location.get_unique_value(), pattern_status) in self.unique_location_types:
                return
            if additional_data:
                pattern_data = PatternData(dynamic_data=additional_data)
            else:
                pattern_data = None

            unique_identifier = (pattern_location.get_unique_value(), pattern_status)
            if unique_identifier in self.unique_location_types:
                return
            self.unique_location_types.add(unique_identifier)
            self.unique_founds.add((dyn_ast, iid, pattern_status))
            new_pattern = Pattern(node, operator, pattern_status, pattern_location, pattern_data)
            self.dynamic_patterns.append(new_pattern)

    def end_execution(self) -> None:
        store_patterns_to_file(self.dynamic_patterns, DYNAMIC_PATTERN_FILENAME, from_dynamic_analysis=True)

    def get_pattern_location_node(self, dyn_ast, iid):
        d_ast = self._get_ast(dyn_ast)
        if d_ast is None:
            return None, None
        ast, iids = self._get_ast(dyn_ast)
        filename_orig, start_line, start_col, end_line, end_col = iids.iid_to_location[iid]
        location = DynLocation(filename_orig, start_line, start_col, end_line, end_col)
        node = get_node_by_location(ast, location)
        filename = filename_orig[:-len(".orig")]
        pattern_location = PatternLocation(filename, start_line, start_col, end_line, end_col)
        return pattern_location, node
