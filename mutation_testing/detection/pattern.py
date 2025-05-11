import json

from mutation_testing.mutation_operators.base_operator import PatternStatus


class PatternLocation:
    def __init__(
            self,
            filename=None,
            start_line=None,
            start_col=None,
            end_line=None,
            end_col=None,
            node_name=None
    ):
        self.filename = filename
        self.start_line = start_line
        self.start_col = start_col
        self.end_line = end_line
        self.end_col = end_col
        self.node_name = node_name

    def serialize_to_dict(self):
        return {
            "filename": self.filename,
            "short_filename": self.filename.split("/")[-1] if self.filename else "",
            "start_line": self.start_line,
            "start_col": self.start_col,
            "end_line": self.end_line,
            "end_col": self.end_col,
            "node_name": self.node_name
        }

    def __eq__(self, other):
        return (
            self.filename == other.filename and
            int(self.start_line) == int(other.start_line) and
            int(self.start_col) == int(other.start_col) and
            int(self.end_line) == int(other.end_line) and
            int(self.end_col) == int(other.end_col) and
            self.node_name == other.node_name
        )

    def get_unique_value(self):
        return (
            self.filename,
            int(self.start_line) if self.start_line else None,
            int(self.start_col) if self.start_col else None,
            int(self.end_line) if self.end_line else None,
            int(self.end_col) if self.end_col else None,
            self.node_name
        )


class Pattern:
    def __init__(self, node, operator, pattern_status: PatternStatus, pattern_location=None, pattern_data=None):
        self.operator = operator
        self.operator_name = str(operator)
        self.node = node
        self.pattern_location = pattern_location
        self.pattern_status = pattern_status
        self.pattern_data = pattern_data

    def serialize_to_json(self):
        pattern_dict = {
            "operator_name": self.operator_name,
            "pattern_status": self.pattern_status.value,
            "pattern_location": self.pattern_location.serialize_to_dict(),
            "pattern_data": self.pattern_data.serialize_to_json() if self.pattern_data else {}
        }
        return json.dumps(pattern_dict, indent=2)

    def __eq__(self, other):
        return (
            self.operator_name == other.operator_name and
            self.pattern_location == other.pattern_location and
            self.pattern_status == other.pattern_status
        )


class PatternData:
    def __init__(self, dynamic_data=None, static_data=None):
        self.dynamic_data = dynamic_data
        self.static_data = static_data

    def serialize_to_json(self):
        return {
            "dynamic_data": self.dynamic_data,
            "static_data": self.static_data
        }
