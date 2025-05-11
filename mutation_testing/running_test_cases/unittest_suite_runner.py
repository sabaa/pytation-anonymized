import os

import coverage

from unittest.result import TestResult
from unittest.loader import TestLoader
from unittest.suite import TestSuite

from .utils import get_module_from_path
from .base_suite_runner import BaseSuiteRunner


class UnittestRunner(BaseSuiteRunner):

    def __init__(self):
        super().__init__()
        self.coverage_data = None
        self._initialize()

    def _initialize(self):
        self.test_suite = TestSuite()
        self.test_result = TestResult()
        self.test_loader = TestLoader()

    def create_test_suite(
            self, project_root=None, test_file_pattern='test_*.py', is_module=False, test_module_path=None):
        self._initialize()
        if is_module:
            self._create_test_suite_from_module(get_module_from_path(test_module_path))
        else:
            self._add_tests_from_directories(project_root, test_file_pattern)

    def run_tests(self, project_root=None):
        self.test_suite.run(self.test_result)

    def _create_test_suite_from_module(self, test_module):
        test_loader = TestLoader()
        self.test_suite = test_loader.loadTestsFromModule(test_module)

    def _add_tests_from_directories(self, test_directories, test_file_pattern='test_*.py'):
        for test_dir in test_directories:
            self.test_suite.addTests(self.test_loader.discover(test_dir, pattern=test_file_pattern))

    def get_result(self, project_root=None):
        # for now, it returns the ratio of passed/all test cases and a list of failed test cases
        all_tests_count = self.test_result.testsRun
        passed_tests_count = all_tests_count - len(self.test_result.failures) - len(self.test_result.errors)
        failed_tests = self.test_result.failures + self.test_result.errors
        ration_of_passed_tests = passed_tests_count / all_tests_count
        return ration_of_passed_tests, failed_tests

    def calculate_coverage(self, project_root=None, test_file_pattern='test_*.py'):
        cov = coverage.Coverage()
        cov.start()
        self.create_test_suite(project_root, test_file_pattern)
        self.run_tests()
        cov.stop()
        cov.save()
        self.coverage_data = cov.get_data()

    def print_coverage_report(self):
        print("\nCoverage Report:")
        print(self.get_covered_lines())

    def get_covered_lines(self):
        covered_lines = {}
        for filename in self.coverage_data.measured_files():
            lines_covered = self.coverage_data.lines(os.path.abspath(filename))
            covered_lines[filename] = lines_covered
        return covered_lines
