from mutation_testing.mutation_exceptions.mutation_exception import MutationException


class ReadAttributeAnalysisError(MutationException):
    def __init__(self, errors, mutation_operator, attribute_data, node_location):
        if not isinstance(mutation_operator, str):
            mutation_operator = mutation_operator.__class__.__name__
        message = (f"Read attribute analysis error for operator {mutation_operator}"
                   f"Node location: {node_location}."
                   f"Errors: {errors}")
        super().__init__(message, errors)
        self.mutation_operator = mutation_operator
        self.attribute_data = attribute_data
        self.node_location = node_location
        self.message = message

    def __str__(self):
        return self.message
