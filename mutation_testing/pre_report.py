import os
import coverage
import json
import pytest

"""
These functions are used to generate a pre-report for a project before mutation testing.
In the pre-report, the coverage report, lines of code, number of classes and number of function definitions are
calculated and saved to a JSON file.
"""
def generate_coverage_report(test_dir, parallel_level='8', main_src_dirs=None):
    # Set up coverage
    cov = coverage.Coverage(branch=True, source=main_src_dirs)
    cov.start()
    pytest.main([test_dir, '--import-mode=importlib'])
    cov.stop()
    cov.save()

    cov_data = cov.report(show_missing=True)
    report = cov_data

    return report


def count_lines_of_code(directories):
    total_lines = 0
    for directory in directories:
        total_lines += count_lines_of_code_in_directory(directory)

    return total_lines


def count_lines_of_code_in_directory(directory):
    tl = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    tl += sum(1 for line in f)
    return tl


def count_classes_and_defs(directories):
    total_classes = 0
    total_functions = 0
    for directory in directories:
        new_tc, new_tf = count_classes_and_defs_directory(directory)
        total_classes += new_tc
        total_functions += new_tf
    return total_classes, total_functions


def count_classes_and_defs_directory(directory):
    tc = 0
    tf = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip().startswith("class "):
                            tc += 1
                        elif line.strip().startswith("def "):
                            tf += 1
    return tc, tf


def generate_pre_report(main_src_dirs, test_dir, parallel_level='8'):
    print(f"Generating pre-report for project with main source directories: {main_src_dirs} and test directory: {test_dir} .")
    coverage_report = generate_coverage_report(test_dir, parallel_level, main_src_dirs)

    loc = count_lines_of_code(main_src_dirs)
    classes, functions = count_classes_and_defs(main_src_dirs)

    report = {
        "project_stats": {
            "coverage_report": coverage_report,
            "lines_of_code": loc,
            "number_of_classes": classes,
            "number_of_function_definitions": functions
        }
    }

    with open("pre_report.json", "w") as f:
        json.dump(report, f)

    print("Report generated and saved to 'pre_report.json'.")
    return report
