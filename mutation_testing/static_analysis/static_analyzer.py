import ast

from mutation_testing.constants import STATIC_PATTERN_FILENAME
from mutation_testing.static_analysis import ASTExtractor
from mutation_testing.mutation_operators import MutationOperators
from mutation_testing.detection import PatternLocation, Pattern, PatternStatus, PatternData, store_patterns_to_file
from mutation_testing.mutation_exceptions import MutationException
from mutation_testing.config import ConfigManager

class StaticAnalyzer:
    def __init__(self):
        self.static_patterns = []

    @staticmethod
    def log(msg):
        if ConfigManager.get_config().logging:
            with open('static_log.log', 'a+') as log_file:
                log_file.write(msg + '\n')
                log_file.flush()

    @staticmethod
    def get_static_patterns(
            nodes,
            filename,
            operators=MutationOperators.operators(),
    ):
        static_patterns = []
        for node in nodes:
            for operator in operators:
                if not operator.static_analysis:
                    continue
                try:
                    pattern_status, _ = operator.get_pattern_status(node)
                except MutationException as e:
                    if ConfigManager.get_config().logging:
                        StaticAnalyzer.log(f"Error in detecting pattern: {e}, node is {node} in {filename} at line {node.lineno} and col {node.col_offset}")
                    continue
                if pattern_status != PatternStatus.NOT_FOUND:
                    pattern_location = PatternLocation(
                        filename=filename,
                        start_line=node.lineno if hasattr(node, 'lineno') else None,
                        start_col=node.col_offset + 1 if hasattr(node, 'col_offset') else None,
                        end_line=node.end_lineno if hasattr(node, 'end_lineno') else None,
                        end_col=node.end_col_offset + 1 if hasattr(node, 'end_col_offset') else None,
                        node_name=node.func.attr if hasattr(node, 'func') and hasattr(node.func, 'attr') else None
                    )
                    static_pattern = Pattern(node, operator, pattern_status, pattern_location)
                    static_patterns.append(static_pattern)
        return static_patterns

    @staticmethod
    def get_ast_nodes(filename):
        with open(filename, 'r') as f:
            source_code = f.read()
            tree = ast.parse(source_code)
            extractor = ASTExtractor()
            extractor.visit(tree)
            all_nodes = extractor.get_nodes()
        return all_nodes

    def analyze(self, python_files):
        for file in python_files:
            nodes = self.get_ast_nodes(file)
            new_static_patterns = self.get_static_patterns(nodes, file)
            unique_static_patterns = self.get_unique_static_patterns(new_static_patterns)
            self.static_patterns.extend(unique_static_patterns)
        store_patterns_to_file(self.static_patterns, STATIC_PATTERN_FILENAME)


    def get_unique_static_patterns(self, new_static_patterns):
        unique_static_patterns = []
        for pattern in new_static_patterns:
            if pattern not in self.static_patterns:
                unique_static_patterns.append(pattern)
        return unique_static_patterns
