import os
import pytest
from unittest.mock import Mock, call
from mutation_testing.running_test_cases import PytestRunner, TestResultPlugin


@pytest.fixture
def tmp_test_directory(tmpdir):
    # Create a temporary directory
    test_dir = tmpdir.mkdir("test_project")
    # Create some test files within the directory
    test_file = test_dir.join("test_example.py")
    test_file.write("import pytest\ndef test_pass():\n    assert True\n\ndef test_fail():\n    assert False\n")
    return str(test_dir)


def test_run_tests(tmp_test_directory):
    runner = PytestRunner()
    runner.run_tests(tmp_test_directory)


def test_get_result(tmp_test_directory):
    runner = PytestRunner()
    ratio, failed_tests = runner.get_result(tmp_test_directory)
    assert ratio == 0.5  # 1 out of 2 tests passed
    assert failed_tests == {'test_example.py::test_fail'}


def test_calculate_coverage(tmp_test_directory):
    runner = PytestRunner()
    runner.calculate_coverage(tmp_test_directory)
    assert runner.coverage_data is not None


def test_get_covered_lines(tmp_test_directory):
    runner = PytestRunner()
    runner.calculate_coverage(tmp_test_directory)
    covered_lines = runner.get_covered_lines()
    assert isinstance(covered_lines, dict)
    assert "test_example.py" in covered_lines
    assert isinstance(covered_lines["test_example.py"], set)


def test_test_result_plugin():
    plugin = TestResultPlugin()
    mock_report_passed = Mock(passed=True, failed=False, skipped=False, nodeid="test1")
    mock_report_failed = Mock(passed=False, failed=True, skipped=False, nodeid="test2")
    mock_report_skipped = Mock(passed=False, failed=False, skipped=True, nodeid="test3")

    plugin.pytest_runtest_logreport(mock_report_passed)
    plugin.pytest_runtest_logreport(mock_report_failed)
    plugin.pytest_runtest_logreport(mock_report_skipped)

    assert "test1" in plugin.passed_tests
    assert "test2" in plugin.failed_tests
    assert "test3" in plugin.skipped_tests
