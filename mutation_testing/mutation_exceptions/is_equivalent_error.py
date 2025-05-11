from mutation_testing.mutation_exceptions.mutation_exception import MutationException


class IsEquivalentError(MutationException):
    def __init__(self, errors, mutation_operator, dynamic_data):
        if not isinstance(mutation_operator, str):
            mutation_operator = mutation_operator.__class__.__name__
        message = (
            f"Operator {mutation_operator} could not detect equivalent dynamic pattern"
            f"Errors are {errors}")
        super().__init__(message, errors)
        self.mutation_operator = mutation_operator
        self.dynamic_data = dynamic_data
