import ast
import pathlib
import subprocess

import astunparse

from mutation_testing.detection import PatternHandler
from mutation_testing.running_test_cases import UnittestRunner
from mutation_testing.mutator import mutate_source_tree
from mutation_testing.static_analysis import StaticAnalyzer
from mutation_testing.utils import revert_source_file, copy_source_file, change_source_file
from mutation_testing.dyn_run import run_instrumentation, run_analysis, restore_original_files
from mutation_testing.constants import (ONE_FILE_TEST_SCRIPT_TEMPLATE, ONE_FILE_TEST_SCRIPT_FILE,
                                        SAMPLE_CODE_PATH, TEST_PROCESS_PATH, UNITTEST)


class MutationTestingVerifier:
    def __init__(self, source_code_path, test_file_path):
        self.source_code_path = source_code_path
        self.test_file_path = test_file_path

    def run(self):
        patterns, _, _ = self.get_patterns()
        self.run_mutation_testing(patterns, self.source_code_path)

    def get_patterns(self):
        self.run_dynamic_analysis(self.source_code_path, self.test_file_path)
        static_analyzer = self.run_static_analysis([self.source_code_path])
        patterns, equivalents, uncovered = PatternHandler.get_patterns(static_analyzer=static_analyzer)
        print("Found patterns: ")
        for pattern in patterns:
            print("Pattern: ", pattern.serialize_to_json())
        print("Found equivalents: ", equivalents)
        print("Found uncovered: ", uncovered)
        return patterns, equivalents, uncovered

    def run_dynamic_analysis(self, source_code_path, test_file_path):
        run_instrumentation([source_code_path])
        script = self.generate_code_script(test_file_path)
        run_analysis(script)
        restore_original_files(SAMPLE_CODE_PATH)

    @staticmethod
    def run_static_analysis(python_files):
        static_analyzer = StaticAnalyzer()
        static_analyzer.analyze(python_files)
        return static_analyzer

    def run_mutation_testing(self, patterns, source_code_path):
        for pattern in patterns:
            current_source_code_ast = self.__initialize_source_code(source_code_path)
            self.mutate_for_current_pattern(current_source_code_ast, pattern, source_code_path)

    def mutate_for_current_pattern(self, current_source_code_ast, pattern, source_code_path):
        pattern_data = pattern.pattern_data
        if pattern_data is None:
            pattern_data = {"file_ast": current_source_code_ast}
        print("\t\t\t*******************")
        copy_source_file(source_code_path)
        change_source_file(source_code_path, self.mutate_code(pattern, current_source_code_ast))
        b_test_result = subprocess.check_output(["python", TEST_PROCESS_PATH, UNITTEST, "True", self.test_file_path])
        test_result = b_test_result.decode("utf-8")
        revert_source_file(source_code_path)
        self.log_results(pattern, source_code_path, test_result)
        print("\t\t\t*******************")

    @staticmethod
    def log_results(pattern, source_code_path, test_result):
        print("Pattern: " + str(pattern.operator))
        print("Line: " + str(pattern.pattern_location.start_line))
        print("Source code path: " + source_code_path)
        print("Test Results " + str(test_result))

    @staticmethod
    def generate_code_script(test_file_path):
        current_path = str(pathlib.Path(__file__).parent.resolve())
        with open(current_path + "/" + ONE_FILE_TEST_SCRIPT_TEMPLATE, 'r') as f:
            template = f.read()
        script = template.format(test_file_path=test_file_path)
        with open(ONE_FILE_TEST_SCRIPT_FILE, 'w') as f:
            f.write(script)
        return ONE_FILE_TEST_SCRIPT_FILE

    @staticmethod
    def mutate_code(pattern, current_source_code_ast):
        pattern_data = pattern.pattern_data
        if pattern_data is None:
            pattern_data = {"file_ast": current_source_code_ast}
        if pattern.node is None:
            print("Pattern node is None")
        mutated_tree = mutate_source_tree(
            pattern.node, pattern.operator.mutate(pattern.node, pattern_data=pattern_data), current_source_code_ast)
        return astunparse.unparse(mutated_tree)

    def get_test_result(self):
        test_runner = UnittestRunner()
        self.__initialize_test_runner(test_runner)
        test_runner.run_tests()
        return test_runner.get_result()

    def __initialize_test_runner(self, test_runner):
        test_runner.create_test_suite(is_module=True, test_module_path=self.test_file_path)

    @staticmethod
    def __initialize_source_code(source_code_path: str):
        current_source_code = open(source_code_path, 'r').read()
        return ast.parse(current_source_code)
