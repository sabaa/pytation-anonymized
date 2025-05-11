import json
import libcst
import os

from dynapyt.utils.nodeLocator import get_node_by_location
from dynapyt.instrument.IIDs import Location as DynLocation
from filelock import FileLock

from mutation_testing.detection.pattern import PatternLocation, Pattern, PatternStatus, PatternData
from mutation_testing.mutation_operators import MutationOperators
from mutation_testing.detection.node_finder import get_ast_node_by_location, get_ast_node_by_name, get_ast_node_multiple_calls


def store_patterns_to_file(pattern_list, filename, delete_existing_data=False, from_dynamic_analysis=False):
    if from_dynamic_analysis and os.environ.get("PYTEST_XDIST_WORKER") is not None:
        filename = f'{os.environ.get("PYTEST_XDIST_WORKER")}_{filename}'
    patterns_data = []

    for pattern in pattern_list:
        pattern_data = json.loads(pattern.serialize_to_json())
        patterns_data.append(pattern_data)

    try:
        with FileLock(filename):
            with open(filename, 'r') as file:
                existing_pattern = json.loads(file.read())
    except FileNotFoundError:
        existing_pattern = []
    except json.decoder.JSONDecodeError:
        existing_pattern = []

    if delete_existing_data:
        existing_pattern = []

    existing_pattern.extend(patterns_data)

    with FileLock(filename):
        with open(filename, 'w+') as file:
            json.dump(existing_pattern, file, indent=2)


def read_dynamic_pattern(read_pattern):
    pattern_location_data = read_pattern.get("pattern_location", {})
    pattern_location = PatternLocation(
        filename=pattern_location_data.get("filename"),
        start_line=pattern_location_data.get("start_line"),
        start_col=pattern_location_data.get("start_col"),
        end_line=pattern_location_data.get("end_line"),
        end_col=pattern_location_data.get("end_col")
    )

    pattern_data_data = read_pattern.get("pattern_data", {})
    pattern_data = PatternData(
        dynamic_data=pattern_data_data.get("dynamic_data"),
        static_data=pattern_data_data.get("static_data")
    )

    operator_name = read_pattern.get("operator_name")
    _operator = MutationOperators[operator_name].value
    operator = _operator()
    node_name = None
    if isinstance(operator, MutationOperators.DeleteFunctionArgument.value):
        node_name = pattern_location_data.get("node_name", None)
        node = get_ast_node_multiple_calls(
            pattern_location,
            operator.node_type,
            operator.node_name,
            node_name
        )
    else:
        node = get_ast_node_by_location(
            pattern_location,
            operator.node_type,
            operator.node_name
        )
    dynamic_pattern = Pattern(node=node, operator=operator, pattern_status=PatternStatus.DYNAMIC,
                              pattern_location=pattern_location, pattern_data=pattern_data)

    return dynamic_pattern


def read_static_pattern(read_pattern):
    pattern_location_data = read_pattern.get("pattern_location", {})
    pattern_location = PatternLocation(
        filename=pattern_location_data.get("filename"),
        start_line=pattern_location_data.get("start_line"),
        start_col=pattern_location_data.get("start_col"),
        end_line=pattern_location_data.get("end_line"),
        end_col=pattern_location_data.get("end_col")
    )

    operator_name = read_pattern.get("operator_name")
    _operator = MutationOperators[operator_name].value
    operator = _operator()
    pattern_status = PatternStatus(read_pattern.get("pattern_status"))

    pattern_data_data = read_pattern.get("pattern_data", {})
    pattern_data = PatternData(
        dynamic_data=pattern_data_data.get("dynamic_data"),
        static_data=pattern_data_data.get("static_data")
    )

    node = get_ast_node_by_location(
        pattern_location=pattern_location,
        node_type=operator.node_type,
        node_condition=operator.node_condition
    )

    return Pattern(node=node, operator=operator, pattern_status=pattern_status,
                                pattern_location=pattern_location, pattern_data=pattern_data)



def patterns_from_file(filename):
    patterns = {
        PatternStatus.DYNAMIC: [],
        PatternStatus.STATIC: [],
        PatternStatus.EQUIVALENT: [],
        PatternStatus.UNCOVERED: []
    }

    try:
        with open(filename, 'r') as file:
            read_patterns = json.load(file)

            for read_pattern in read_patterns:
                pattern_status_value = read_pattern.get("pattern_status")
                pattern_status = PatternStatus(pattern_status_value)
                if pattern_status == PatternStatus.DYNAMIC or pattern_status == PatternStatus.EQUIVALENT:
                    pattern = read_dynamic_pattern(read_pattern)
                elif pattern_status == PatternStatus.STATIC or pattern_status == PatternStatus.UNCOVERED:
                    pattern = read_static_pattern(read_pattern)

                patterns[pattern_status].append(pattern)

    except FileNotFoundError:
        print(f"File '{filename}' not found. Returning an empty list.")

    return patterns


def get_node_from_location(pattern_location):
    with open(pattern_location.filename, 'r') as file:
        source_code = file.read()
    libcst_ast = libcst.parse_module(source_code)
    location = DynLocation(
        pattern_location.filename,
        pattern_location.start_line,
        pattern_location.start_col,
        pattern_location.end_line,
        pattern_location.end_col
    )
    return get_node_by_location(libcst_ast, location)
