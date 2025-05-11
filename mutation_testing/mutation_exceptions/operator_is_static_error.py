from mutation_testing.mutation_exceptions.mutation_exception import MutationException


class OperatorIsStaticError(MutationException):
    def __init__(self, errors, mutation_operator):
        if not isinstance(mutation_operator, str):
            mutation_operator = mutation_operator.__class__.__name__
        message = (f"Operator {mutation_operator} could not detect static pattern. "
                   f"Errors are {errors}")
        super().__init__(message, errors)
        self.mutation_operator = mutation_operator

