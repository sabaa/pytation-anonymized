from enum import Enum

from mutation_testing.config import ConfigManager


class PatternStatus(Enum):
    STATIC = 'STATIC'
    DYNAMIC = 'DYNAMIC'
    EQUIVALENT = 'EQUIVALENT'
    NOT_FOUND = 'NOT_FOUND'
    UNCOVERED = 'UNCOVERED'


class HookName(Enum):
    POST_CALL = 'post_call'
    READ_ATTRIBUTE = 'read_attribute'
    PRE_CALL = 'pre_call'


class BaseMutationOperator:
    def __init__(
            self,
            hook_name: HookName = None,
            static_analysis: bool = False,
            dynamic_analysis: bool = False,
            node_type=None,
            node_name: str = None,
            node_condition = None
    ) -> None:
        self.hook_name = hook_name
        self.static_analysis = static_analysis
        self.dynamic_analysis = dynamic_analysis
        self.node_type = node_type
        self.node_name = node_name
        self.node_condition = node_condition

        if dynamic_analysis and hook_name is None:
            raise ValueError('hook_name must be set if dynamic_analysis is True')

    def _get_result(self, data):
        result = None
        if self.dynamic_analysis:
            result = self._is_dynamic_pattern(data)
        elif self.static_analysis:
            result = self._is_static_pattern(data)
        if result is None:
            result = PatternStatus.NOT_FOUND, None

        if not (isinstance(result, tuple) and len(result) == 2):
            result = result, None
        return result

    @staticmethod
    def _handle_equivalency(result, is_dynamic_analysis):
        if result[0] == PatternStatus.EQUIVALENT and not BaseMutationOperator._get_config().equivalency_check:
            if is_dynamic_analysis:
                return PatternStatus.DYNAMIC, result[1]
            else:
                return PatternStatus.STATIC, result[1]
        return result

    def get_pattern_status(self, data):
        result = self._get_result(data)
        result = self._handle_equivalency(result, self.dynamic_analysis)
        return result

    @staticmethod
    def mutate(node, **kwargs):
        pass

    @staticmethod
    def _is_static_pattern(node) -> PatternStatus:
        pass

    @staticmethod
    def _is_dynamic_pattern(dynamic_data):
        pass

    @staticmethod
    def _is_equivalent_pattern(*args, **kwargs) -> PatternStatus:
        pass

    @staticmethod
    def _get_config():
        return ConfigManager.get_config()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'

    def __str__(self):
        return self.__repr__()
