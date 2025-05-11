from enum import Enum

from mutation_testing.mutation_operators.delete_conversion_functions import DeleteConversionFunctions
from mutation_testing.mutation_operators.delete_elements_iterable import DeleteElementsIterable
from mutation_testing.mutation_operators.delete_expressions_if import DeleteExpressionsIf
from mutation_testing.mutation_operators.delete_function_argument import DeleteFunctionArgument
from mutation_testing.mutation_operators.change_used_attribute import ChangeUsedAttribute
from mutation_testing.mutation_operators.delete_method_call import DeleteMethodCall
from mutation_testing.mutation_operators.delete_attribute_access import DeleteAttributeAccess
from mutation_testing.mutation_operators.switch_similar_functions import SwitchSimilarFunctions


class MutationOperators(Enum):
    DeleteConversionFunctions = DeleteConversionFunctions
    DeleteElementsIterable = DeleteElementsIterable
    DeleteExpressionsIf = DeleteExpressionsIf
    DeleteFunctionArgument = DeleteFunctionArgument
    ChangeUsedAttribute = ChangeUsedAttribute
    DeleteMethodCall = DeleteMethodCall
    DeleteAttributeAccess = DeleteAttributeAccess

    @staticmethod
    def operators():
        return [
            DeleteConversionFunctions(),
            DeleteElementsIterable(),
            DeleteExpressionsIf(),
            DeleteFunctionArgument(),
            ChangeUsedAttribute(),
            DeleteMethodCall(),
            DeleteAttributeAccess(),
        ]
