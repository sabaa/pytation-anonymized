import ast
import inspect
from copy import deepcopy
import random

from mutation_testing.mutation_operators import BaseMutationOperator, PatternStatus, HookName
from mutation_testing.mutation_exceptions import OperatorMutateError, MutationException

CANDIDATE_ATTR_KW = "candidate_attr"


class ChangeUsedAttribute(BaseMutationOperator):
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
            pattern_data = kwargs.get("pattern_data", None)
            if not pattern_data:
                raise OperatorMutateError("No additional data found", ChangeUsedAttribute, node)
            dynamic_data = pattern_data.dynamic_data
            candidate_attr = dynamic_data.get(CANDIDATE_ATTR_KW, None)
            if candidate_attr:
                mutated_node = deepcopy(node)
                mutated_node.attr = candidate_attr
                return mutated_node

            else:
                raise OperatorMutateError("No candidate attribute found", ChangeUsedAttribute, node)
        except MutationException as e:
            return node

    @staticmethod
    def _is_dynamic_pattern(attribute_data):
        base = attribute_data.get("base", None)
        attr_name = attribute_data.get("name", None)
        attr = attribute_data.get("val", None)
        if attr is None:
            return PatternStatus.NOT_FOUND, None
        if inspect.ismethod(attr):
            return PatternStatus.NOT_FOUND, None
        if callable(attr):
            return PatternStatus.NOT_FOUND, None
        attrs = []
        for f in dir(base):
            if f.startswith('__'):
                continue
            getattr_stat = inspect.getattr_static(base, f, None)
            if getattr_stat is None or isinstance(getattr_stat, property) or callable(getattr_stat):
                continue
            attrs.append(f)
        if len(attrs) > 1:
            # get another attribute
            candidate_attrs = []
            for attr in attrs:
                if attr != attr_name:
                    candidate_attrs.append(attr)
            if len(candidate_attrs) > 0:
                candidate_attr = random.choice(candidate_attrs)
                return PatternStatus.DYNAMIC, {CANDIDATE_ATTR_KW: candidate_attr}
        return PatternStatus.EQUIVALENT, None
