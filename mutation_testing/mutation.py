import ast
import pathlib
import subprocess
import time
import os
import glob
import random
import math
import re

import astunparse

from mutation_testing.detection import PatternHandler
from mutation_testing.running_test_cases import UnittestRunner, PytestRunner
from mutation_testing.mutator import mutate_source_tree
from mutation_testing.utils import revert_source_file, copy_source_file, \
    change_source_file, MutationLogger, get_python_files, merge_dynamic_results, TimeReporter
from mutation_testing.dyn_run import run_instrumentation, run_analysis, restore_original_files
from mutation_testing.constants import (
    TEST_SCRIPT_TEMPLATE_PARALLEL, TEST_SCRIPT_TEMPLATE_SERIAL, TEST_SCRIPT_FILE,
    DEFAULT_TEST_PATTERN,
    PYTEST, TEST_PROCESS_MODULE, RANDOM_SELECTED_PATTERNS_FILENAME, DIFF_SELECTED_PATTERNS_FILENAME,
    DEFAULT_TIMEOUT,
    RANDOM_STRATEGY, OPERATOR_RANDOM_STRATEGY, OPERATOR_RANDOM_STRATEGY_THRESHOLD, OPERATOR_DIFF_STRATEGY)
from mutation_testing.mutation_exceptions import MutationException
from mutation_testing.static_analysis import StaticAnalyzer
from mutation_testing.config import ConfigManager
from mutation_testing.detection.utils import store_patterns_to_file
from mutation_testing.get_diff import get_changed_lines as get_diff_changes, DIFF_TYPE_DELETED, DIFF_TYPE_UNKNOWN



class MutationTesting:
    """
    This is the main class for mutation testing framework.
    """
    def __init__(
            self, root_directory=None,
            test_file_pattern=DEFAULT_TEST_PATTERN,
            exclude_directories=None,
            include_directories=None,
            exclude_patterns=None,
            test_runner=PYTEST,
            test_root=None,
            test_script=None,
            parallel_level='8',
            subset_selection="no_op",
            selection_value=0,
            selection_threshold=10,
            timeout_coefficient=3,
            commit_before=None,
            commit_after=None
    ):
        self.root_directory = root_directory
        self.test_file_pattern = test_file_pattern
        self.test_runner = test_runner
        self.exclude_directories = exclude_directories
        self.include_directories = include_directories
        self.exclude_patterns = exclude_patterns
        self.test_root = test_root
        self.test_script = test_script
        if self.exclude_directories is None:
            self.exclude_directories = []
        if include_directories is None:
            self.include_directories = []
        if exclude_patterns is None:
            self.exclude_patterns = []
        self.exclude_directories.append(TEST_SCRIPT_FILE)
        self.logger = MutationLogger()
        self.parallel_level = parallel_level
        self.time_reporter = TimeReporter()
        self.subset_selection = subset_selection
        self.selection_value = selection_value
        self.selection_threshold = selection_threshold
        self.commit_before = commit_before
        self.commit_after = commit_after

        if os.path.exists('mutation_log.log'):
            os.remove('mutation_log.log')
        self.log_file = open('mutation_log.log', 'a')
        self.timeout = DEFAULT_TIMEOUT
        self.timeout_coefficient = timeout_coefficient
        self.pattern_count = 0
        self.all_patterns_count = 0

        self.mutant_results = {
            "DEAD": 0,
            "ALIVE": 0,
            "ERROR": 0,
            "TIMEOUT": 0,
            "ALL": 0,
            "mutation_score": 0.0
        }

    def log(self, msg):
        self.log_file.write(msg + '\n')
        self.log_file.flush()

    def run(self):
        """
        This is the main method to run the mutation testing framework.
        :return:
        """
        self.time_reporter.start_timer()
        all_patterns, _, _ = self.get_patterns()
        if ConfigManager.get_config().subset_selection:
            patterns = self.select_subset(
                all_patterns,
                strategy=self.subset_selection,
                value=self.selection_value,
                threshold=self.selection_threshold,
                commit_before=self.commit_before,
                commit_after=self.commit_after
            )
        else:
            patterns = all_patterns
        self.all_patterns_count = len(patterns)
        if ConfigManager.get_config().logging:
            self.log("Total selected patterns: " + str(self.all_patterns_count))
        if ConfigManager.get_config().mutation:
            patterns_per_file = self.get_patterns_per_file(patterns)
            self.time_reporter.set_to_now("start_mutation")
            for source_code_path in patterns_per_file.keys():
                self.run_for_current_file(patterns_per_file[source_code_path], source_code_path)
            self.time_reporter.set_to_now("end_mutation")
        self.time_reporter.end_timer()
        self.report()

    def report(self):
        self.time_reporter.set_to_now("start_post_processing")
        if self.mutant_results['ALL'] == 0:
            self.mutant_results['mutation_score'] = 0.0
        else:
            self.mutant_results['mutation_score'] = self.mutant_results['DEAD'] / (self.mutant_results['ALL'])
        self.time_reporter.set_to_now("end_post_processing")
        self.time_reporter.report()
        self.report_mutant_results()
        self.print_reports()
        # generate_html_report()


    @staticmethod
    def select_subset(
            patterns,
            strategy=OPERATOR_RANDOM_STRATEGY_THRESHOLD,
            value=0,
            threshold=10,
            commit_before=None,
            commit_after=None
    ):
        """
        Selecting a subset of patterns based on the strategy.
        Strategy can be:
        - RANDOM_STRATEGY: Randomly selecting a percentage of patterns
        - OPERATOR_RANDOM_STRATEGY: Randomly selecting a percentage of each operator
        - OPERATOR_RANDOM_STRATEGY_THRESHOLD: Randomly selecting a percentage of each operator with
            at least threshold mutants from each operator
        - OPERATOR_DIFF_STRATEGY: choosing mutants from the diff of two commits.
        :param patterns:
        :param strategy:
        :param value:
        :param threshold:
        :param commit_before:
        :param commit_after:
        :return:
        """
        if ConfigManager.get_config().logging:
            print("subset selection strategy: ", strategy)
        if strategy == RANDOM_STRATEGY:
            """
            Randomly selecting a percentage of patterns
            """
            selected_patterns = random.sample(patterns, math.floor(len(patterns) * value))
            store_patterns_to_file(selected_patterns, RANDOM_SELECTED_PATTERNS_FILENAME)
        elif strategy == OPERATOR_RANDOM_STRATEGY_THRESHOLD:
            """
            Randomly selecting a percentage of each operator with 
            at least threshold mutants from each operator
            """
            if ConfigManager.get_config().logging:
                print("subset selection strategy: ", strategy)
                print(f"value is: {value}, and threshold is: {threshold}")

            operator_patterns = {}
            for pattern in patterns:
                pattern_name = str(pattern.operator)
                if pattern_name not in operator_patterns:
                    operator_patterns[pattern_name] = []
                operator_patterns[pattern_name].append(pattern)
            selected_patterns = []
            for operator in operator_patterns.keys():
                random_selected = random.sample(
                    operator_patterns[operator], math.ceil(len(operator_patterns[operator]) * value))
                if len(random_selected) < threshold <= len(operator_patterns[operator]):
                    random_selected = random.sample(operator_patterns[operator], threshold)
                elif len(operator_patterns[operator]) < threshold:
                    random_selected = operator_patterns[operator]
                selected_patterns.extend(random_selected)
            store_patterns_to_file(selected_patterns, RANDOM_SELECTED_PATTERNS_FILENAME)
        elif strategy == OPERATOR_RANDOM_STRATEGY:
            """
            Choosing a percentage of each operator
            """
            operator_patterns = {}
            for pattern in patterns:
                pattern_name = str(pattern.operator)
                if pattern_name not in operator_patterns:
                    operator_patterns[pattern_name] = []
                operator_patterns[pattern_name].append(pattern)
            selected_patterns = []
            for operator in operator_patterns.keys():
                selected_patterns.extend(random.sample(
                    operator_patterns[operator], math.ceil(len(operator_patterns[operator]) * value)))
            store_patterns_to_file(selected_patterns, RANDOM_SELECTED_PATTERNS_FILENAME)
        elif strategy == OPERATOR_DIFF_STRATEGY:
            """
            choosing mutants from the diff of two commits
            """
            changes = get_diff_changes(commit_before, commit_after)

            selected_patterns = []
            for pattern in patterns:
                for change in changes:
                    if change['type'] in [DIFF_TYPE_DELETED, DIFF_TYPE_UNKNOWN]:
                        continue
                    if  os.path.relpath(pattern.pattern_location.filename) == os.path.relpath(change['filename']):
                        if pattern.pattern_location.start_line in change['lines'] or\
                            pattern.pattern_location.end_line in change['lines']:
                            selected_patterns.append(pattern)
            store_patterns_to_file(selected_patterns, DIFF_SELECTED_PATTERNS_FILENAME)
        else:
            selected_patterns = patterns
        return selected_patterns

    def report_mutant_results(self):
        with open("summary_report.csv", "w") as f:
            keys = list(self.mutant_results.keys())
            values = [str(self.mutant_results[key]) for key in keys]
            f.write(','.join(keys) + '\n')
            f.write(','.join(values) + '\n')

    def print_reports(self):
        print("Mutation Score: " + str(self.mutant_results['mutation_score']))
        self.time_reporter.print_report()

    def get_patterns(self):
        """
        This method is used to get the patterns from the static analysis and dynamic analysis.
        :return:
        """
        python_files = get_python_files(
            self.root_directory, self.exclude_directories, self.include_directories, self.exclude_patterns)
        covered_lines = self.get_covered_lines_per_file()
        static_analyzer = None
        if ConfigManager.get_config().detection:
            self.time_reporter.set_to_now("start_static")
            static_analyzer = self.run_static_analysis(python_files)
            self.time_reporter.set_to_now("end_static")
            if ConfigManager.get_config().logging:
                self.log("Static analysis done time: " + str(self.time_reporter.get_static_time()))
            self.time_reporter.set_to_now("start_dynamic")
            self.run_dynamic_analysis(python_files)
            self.time_reporter.set_to_now("end_dynamic")
        if ConfigManager.get_config().logging:
            self.log("Dynamic analysis done time: " + str(self.time_reporter.get_dynamic_time()))
        patterns, equivalents, uncovered = PatternHandler.get_patterns(
            static_analyzer=static_analyzer,
            covered_lines=covered_lines
        )
        return patterns, equivalents, uncovered

    @staticmethod
    def get_patterns_per_file(patterns):
        patterns_per_file = {}
        for pattern in patterns:
            if pattern.pattern_location.filename not in patterns_per_file.keys():
                patterns_per_file[pattern.pattern_location.filename] = []
            patterns_per_file[pattern.pattern_location.filename].append(pattern)
        return patterns_per_file

    def run_for_current_file(self, patterns, source_code_path):
        if ConfigManager.get_config().logging:
            self.log("Running Mutation for file: " + source_code_path)
        for pattern in patterns:
            self.pattern_count += 1
            current_source_code_ast = self.__initialize_source_code(source_code_path)
            self.mutate_for_current_pattern(current_source_code_ast, pattern, source_code_path)

    def mutate_for_current_pattern(self, current_source_code_ast, pattern, source_code_path):
        """
        This method is used to mutate the code for a given pattern.
        :param current_source_code_ast:
        :param pattern:
        :param source_code_path:
        :return:
        """
        if ConfigManager.get_config().logging:
            self.log("Mutating for operator: {} at {} line {}".format(
                str(pattern.operator), source_code_path, pattern.pattern_location.start_line))
            self.log("Pattern {}/{}".format(self.pattern_count, self.all_patterns_count))
        start_current_mutation = time.time()
        copy_source_file(source_code_path)
        parent = os.path.dirname(source_code_path)
        try:
            new_code, new_node = self.mutate_code(pattern, current_source_code_ast)
        except MutationException as e:
            if ConfigManager.get_config().logging:
                self.log("Mutating for operator: {} at {} line {}. error is {}".format(
                    str(pattern.operator), source_code_path, pattern.pattern_location.start_line, e))
            revert_source_file(source_code_path)
            return
        except Exception as e:
            if ConfigManager.get_config().logging:
                self.log("ERROR: Mutating for operator: {} at {} line {}. error is {}".format(
                    str(pattern.operator), source_code_path, pattern.pattern_location.start_line, e))
            revert_source_file(source_code_path)
            return
        change_source_file(source_code_path, new_code)
        try:
            test_result = subprocess.run(
            ["python", "-m", TEST_PROCESS_MODULE, self.parallel_level],
            capture_output=True, text=True, timeout=self.timeout
        )
        except subprocess.TimeoutExpired:
            test_result = "TIMEOUT"
        revert_source_file(source_code_path)
        end_current_mutation = time.time()
        if ConfigManager.get_config().logging:
            if test_result == "TIMEOUT":
                self.log("Timeout for operator: {} at {} line {} in {} seconds".format(
                    str(pattern.operator),
                    source_code_path,
                    pattern.pattern_location.start_line,
                    end_current_mutation - start_current_mutation
                ))
            else:
                self.log("Mutation done for operator: {} at {} line {} in {} seconds".format(
                    str(pattern.operator),
                    source_code_path,
                    pattern.pattern_location.start_line,
                    end_current_mutation - start_current_mutation
                ))
        test_report = {}
        try:
            test_report = self.get_test_report(test_result)
            mutation_result = self.get_mutation_result(test_report)
        except Exception as e:
            mutation_result = "ERROR"
            if ConfigManager.get_config().logging:
                self.log(f"Error in determining result for operator: {str(pattern.operator)} at {source_code_path} line "
                            f"{pattern.pattern_location.start_line}. Error: {e}")
        if mutation_result not in self.mutant_results:
            self.mutant_results[mutation_result] = 0
        self.mutant_results[mutation_result] += 1
        self.mutant_results["ALL"] += 1
        self.logger.write_to_csv(
            [str(pattern.operator),
             source_code_path,
             pattern.pattern_location.start_line,
              pattern.pattern_location.end_line,
             pattern.pattern_location.start_col,
             pattern.pattern_location.end_col,
             mutation_result,
             astunparse.unparse(pattern.node),
             astunparse.unparse(new_node),
             end_current_mutation - start_current_mutation,
             test_report.get('failed_tests', [])
             ]
        )

    @staticmethod
    def get_test_report(test_result):
        """
        This method is used to get the test report from the test result.
        :param test_result:
        :return:
        """
        output = test_result.stdout
        error_output = test_result.stderr
        passed = int(re.search(r"(\d+) passed", output).group(1)) if re.search(r"(\d+) passed", output) else 0
        failed = int(re.search(r"(\d+) failed", output).group(1)) if re.search(r"(\d+) failed", output) else 0
        errors = int(re.search(r"(\d+) error", output).group(1)) if re.search(r"(\d+) error", output) else 0

        failed_tests = re.findall(r"FAILED (.+) -", output)

        return {
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "failed_tests": failed_tests,
            "output": output,
            "error_output": error_output
        }

    @staticmethod
    def get_mutation_result(test_report):
        if test_report['failed'] != 0 or test_report['errors'] != 0:
            return 'DEAD'
        if test_report['passed'] > 0:
            return 'ALIVE'
        return 'UNKNOWN'


    def log_results(self, pattern, source_code_path, test_result):
        self.logger.write_to_csv(
            [str(pattern.operator), pattern.pattern_location.start_line, source_code_path,
             test_result[0], test_result[1], test_result[2], test_result[3]])

    @staticmethod
    def __initialize_source_code(source_code_path: str):
        current_source_code = open(source_code_path, 'r').read()
        return ast.parse(current_source_code)

    @staticmethod
    def mutate_code(pattern, current_source_code_ast):
        pattern_data = pattern.pattern_data
        if pattern_data is None:
            pattern_data = {"file_ast": current_source_code_ast}
        try:
            mutated_node = pattern.operator.mutate(pattern.node, pattern_data=pattern_data)
            mutated_tree = mutate_source_tree(
                pattern.node,
                mutated_node,
                current_source_code_ast)
        except MutationException as e:
            raise e

        return astunparse.unparse(mutated_tree), mutated_node

    def generate_test_script(self):  # Dynapyt entry point
        current_path = str(pathlib.Path(__file__).parent.resolve())
        if self.parallel_level == '1':
            with open(current_path + "/" + TEST_SCRIPT_TEMPLATE_SERIAL, 'r') as f:
                template = f.read()
        else:
            with open(current_path + "/" + TEST_SCRIPT_TEMPLATE_PARALLEL, 'r') as f:
                template = f.read()
        script = template.format(
            parallel_level=self.parallel_level,
        )

        with open(TEST_SCRIPT_FILE, 'w') as f:
            f.write(script)


    def run_dynamic_analysis(self, python_files):
        """
        This method is used to run the dynamic analysis using DynaPyt.
        :param python_files:
        :return:
        """
        try:
            run_instrumentation(python_files)
            self.generate_test_script()
            run_analysis(TEST_SCRIPT_FILE)
            
        finally:
            restore_original_files(self.root_directory, self.exclude_directories, [TEST_SCRIPT_FILE])
            merge_dynamic_results()

    @staticmethod
    def run_static_analysis(python_files):
        static_analyzer = StaticAnalyzer()
        static_analyzer.analyze(python_files)
        return static_analyzer

    def get_covered_lines_per_file(self):
        test_runner = self.get_test_runner()
        before_tests = time.time()
        test_runner.calculate_coverage(self.test_root, self.test_file_pattern)
        total_test_time = time.time() - before_tests
        self.timeout = total_test_time * self.timeout_coefficient
        test_runner.save_coverage_report()
        return test_runner.get_covered_lines()

    def get_test_runner(self):
        if self.test_runner == PYTEST:
            return PytestRunner()
        else:
            return UnittestRunner()

    @staticmethod
    def clean_up():
        import os
        # delete all files with names gw*_dynamic_patterns_list.json
        gw_files = glob.glob('gw*_dynamic_patterns_list.json')
        files_to_delete = [
                              "dynamic_patterns_list.json",
                              "static_patterns_list.json",
                              "coverage_report.json",
                              "txt_results.txt",
                              "dyn_test_script.py",
                              "csv_results.csv",
                              "mutation_testing_report.html",
                              "dyna_log.log",
                              "mutation_log.log",
                              "static_log.log",
                              RANDOM_SELECTED_PATTERNS_FILENAME
                          ] + gw_files

        for file_name in files_to_delete:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"Deleted {file_name}")
            else:
                print(f"{file_name} does not exist, skipping deletion.")
