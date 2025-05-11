import os
import pytest
import json

from .base_suite_runner import BaseSuiteRunner


class PytestRunner(BaseSuiteRunner):
    def _initialize(self):
        super()._initialize()

    def create_test_suite(
            self, project_root=None, test_file_pattern='test_*.py', is_module=False, test_module_path=None):
        pass

    def run_tests(self, test_root=None, parallel_level='8'):
        if int(parallel_level) > 1:
            pytest.main(['-n', parallel_level, test_root])
        else:
            pytest.main([test_root])

    def get_result(self, test_root=None):
        plugin = TestResultPlugin()
        pytest.main([test_root, '-p', 'no:terminal'], plugins=[plugin])
        passed_count = len(plugin.passed_tests)
        failed_count = len(plugin.failed_tests)
        skipped_count = len(plugin.skipped_tests)
        failed_names = plugin.failed_tests

        return {
            "passed_count": passed_count,
            "failed_count": failed_count,
            "skipped_count": skipped_count,
            "failed_names": list(failed_names)
        }

    def calculate_coverage(self, project_root=None, test_file_pattern='test_*.py', parallel_level='8'):
        self.coverage.start()
        pytest.main([project_root])

        self.coverage.stop()
        self.coverage.save()
        self.coverage_data = self.coverage.get_data()

    def print_coverage_report(self):
        print("\nCoverage Report:")
        print(self.get_covered_lines())

    def save_coverage_report(self, report_path='coverage_report.json'):
        with open(report_path, 'w') as f:
            json.dump(self.get_covered_lines(), f, indent=4)

    def get_covered_lines(self):
        covered_lines = {}
        for filename in self.coverage_data.measured_files():
            lines_covered = self.coverage_data.lines(filename)
            abs_filename = os.path.abspath(filename)
            covered_lines[abs_filename] = lines_covered
        return covered_lines


class TestResultPlugin:
    def __init__(self):
        self.passed_tests = set()
        self.failed_tests = set()
        self.skipped_tests = set()

    def pytest_runtest_logreport(self, report):
        if report.passed:
            self.passed_tests.add(report.nodeid)
        elif report.failed:
            self.failed_tests.add(report.nodeid)
        elif report.skipped:
            self.skipped_tests.add(report.nodeid)
