from mutation_testing.mutation_exceptions.mutation_exception import MutationException


class OperatorMutateError(MutationException):
    def __init__(self, errors, mutation_operator, node):
        if not isinstance(mutation_operator, str):
            mutation_operator = mutation_operator.__class__.__name__
        message = (f"Operator {mutation_operator} failed to mutate node {node}"
                   f"with errors: {errors}")
        super().__init__(message, errors)
        self.mutation_operator = mutation_operator
        self.node = node
        self.node_type = type(node)
