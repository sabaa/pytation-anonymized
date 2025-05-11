import os
import csv
import fnmatch
import json
import glob
import time

from mutation_testing.constants import DYNAMIC_PATTERN_FILENAME


def change_source_file(source_file, new_code):
    """
    Change the contents of a source file to new code.
    :param source_file:
    :param new_code:
    :return:
    """
    with open(source_file, 'w') as f:
        f.write(new_code)


def revert_source_file(source_file):
    """
    Revert a source file to its original state.
    :param source_file:
    :return:
    """
    import os

    target = source_file + '.bak'

    os.remove(source_file)
    os.rename(target, source_file)


def copy_source_file(source_file):
    """
    Create a backup of a source file before making changes.
    :param source_file:
    :return:
    """
    import shutil

    original = source_file
    target = source_file + '.bak'

    shutil.copyfile(original, target)


DEFAULT_FIELDNAMES = ['operator', 'source_code_path', 'start_line', 'end_line', 'start_col', 'end_col', 'mutant_result', 'before_lines', 'after_lines',
                      'duration', 'failed_tests']


def create_new_dir(path):
    """
    Create a new directory for the mutated code.
    :param path:
    :return:
    """
    directory = os.path.join(path, "mutated_code")

    if os.path.exists(directory):
        return
    else:
        os.mkdir(directory)


def save_mutants(source_file, new_path):
    """
    Save mutated code to a new directory. (Directory created by create_new_dir(path))
    :param source_file:
    :param new_path:
    :return:
    """
    import shutil

    try:
        directory = os.listdir(new_path)
        for file in directory:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error occured deleting files.")

    shutil.copy(source_file, new_path)


class MutationLogger:
    """
    A class to log mutation testing results to a CSV file
    """
    def __init__(self,
                 scv_filename='csv_results.csv',
                 txt_filename='txt_results.txt',
                 fieldnames=None):
        if fieldnames is None:
            fieldnames = DEFAULT_FIELDNAMES
        if os.path.exists(scv_filename):
            os.remove(scv_filename)
        with open(scv_filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)

        self.csv_filename = scv_filename

        self.txt_filename = txt_filename
        if os.path.exists(self.txt_filename):
            os.remove(self.txt_filename)
        with open(self.txt_filename, 'w') as f:
            f.write('')

    def write_to_csv(self, data):
        """
        Write the final results to a CSV file.
        Each row in the CSV file will contain the following fields:
        - operator
        - source_code_path
        - source_code_line
        - mutant_result (dead/alive/timeout)
        - before_lines (lines of code before mutation)
        - after_lines (lines of code after mutation)
        - duration (time taken to run the test)
        - failed_tests (a list of failed tests)
        :param data:
        :return:
        """
        with open(self.csv_filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def write_to_txt(self, data):
        with open(self.txt_filename, 'a') as f:
            f.write(data)
            f.write('\n')


def get_python_files(root_directory, exclude_directories=None, include_directories=None, exclude_patterns=None):
    """
    Get a list of Python files within a specified root directory, with options to exclude directories,
    include specific directories, and exclude files based on patterns.

    :param root_directory: The root directory to start searching for Python files.
    :param exclude_directories: A list of directories to exclude from the search.
    :param include_directories: A list of directories to include in the search (if provided).
    :param exclude_patterns: A list of file patterns to exclude from the result.
    :return: A list of paths to Python files that meet the specified criteria.
    """
    if exclude_directories is None:
        exclude_directories = []
    if include_directories is None:
        include_directories = []
    if exclude_patterns is None:
        exclude_patterns = []

    python_files = []
    abs_exclude_directories = [os.path.join(root_directory, ex_dir) for ex_dir in exclude_directories]
    abs_include_directories = [os.path.join(root_directory, inc_dir) for inc_dir in include_directories]

    if include_directories:
        start_dirs = abs_include_directories
    else:
        start_dirs = [root_directory]

    for start_dir in start_dirs:
        for path, sub_dirs, files in os.walk(start_dir):
            if not any([path.startswith(j) for j in abs_exclude_directories]):
                for name in files:
                    if name.endswith('.py'):
                        file_path = os.path.join(path, name)

                        if not any(fnmatch.fnmatch(file_path, pattern) for pattern in exclude_patterns):
                            python_files.append(file_path)

    return python_files


def hashable_pattern_location(location):
    """
    Create a hashable representation of a pattern location to use as a key in a dictionary to avoid duplicates.
    :param location:
    :return:
    """
    return (
        location['filename'],
        location['short_filename'],
        location['start_line'],
        location['start_col'],
        location['end_line'],
        location['end_col'],
        location['node_name']
    )


def hashable_pattern_data(data):
    key = []
    if 'dynamic_data' in data and data['dynamic_data'] is not None:
        for k, v in data['dynamic_data'].items():
            key.append(str(str(k) + str(v)))

    if 'static_data' in data and data['static_data'] is not None:
        for k, v in data['static_data'].items():
            key.append(str(str(k) + str(v)))

    return ','.join(key)


def create_key(entry):
    operator_name = entry['operator_name']
    if operator_name == 'DeleteFunctionArgument':
        return (
            entry['operator_name'],
            entry['pattern_status'],
            hashable_pattern_location(entry['pattern_location'], ),
            hashable_pattern_data(entry['pattern_data'])
        )
    return (
        entry['operator_name'],
        entry['pattern_status'],
        hashable_pattern_location(entry['pattern_location'], ),
    )


def merge_dynamic_results(
        output_file=DYNAMIC_PATTERN_FILENAME,
        general_input_name=DYNAMIC_PATTERN_FILENAME,
        glob_pattern='gw*'
):
    """
    Dynamic analysis may run on different threads and generate different files. This function merges the results and
    removes duplicates.
    :param output_file:
    :param general_input_name:
    :param glob_pattern:
    :return:
    """
    input_files = glob.glob(f"{glob_pattern}_{general_input_name}")

    if not input_files:
        print(f"No files found matching pattern '{glob_pattern}_{general_input_name}'")
        return
    combined_entries = []
    seen_entries = set()
    for file in input_files:
        with open(file, 'r') as f:
            data = json.load(f)
            for entry in data:
                key = create_key(entry)
                if key not in seen_entries:
                    seen_entries.add(key)
                    combined_entries.append(entry)

    with open(output_file, 'w') as f:
        json.dump(combined_entries, f, indent=4)

    print(f"Combined JSON written to {output_file}")


class TimeReporter:
    """
    A class to report the time taken for different parts of the mutation testing
    """
    def __init__(self):
        self.start = 0.0
        self.end = 0.0
        self.start_static = 0.0
        self.end_static = 0.0
        self.start_dynamic = 0.0
        self.end_dynamic = 0.0
        self.start_mutation = 0.0
        self.end_mutation = 0.0
        self.start_post_processing = 0.0
        self.end_post_processing = 0.0

    def start_timer(self):
        self.start = time.time()

    def end_timer(self):
        self.end = time.time()

    def set_to_now(self, time_name):
        setattr(self, time_name, time.time())

    def get_static_time(self):
        return self.end_static - self.start_static

    def get_dynamic_time(self):
        return self.end_dynamic - self.start_dynamic

    def get_mutation_time(self):
        return self.end_mutation - self.start_mutation

    def get_post_processing_time(self):
        return self.end_post_processing - self.start_post_processing

    def get_total_time(self):
        return self.end - self.start

    def print_report(self):
        print("Time report:")
        print("Time taken for static analysis: ", self.get_static_time())
        print("Time taken for dynamic analysis: ", self.get_dynamic_time())
        print("Time taken for mutation: ", self.get_mutation_time())
        print("Time taken for post processing: ", self.get_post_processing_time())
        print("Total time taken: ", self.get_total_time())

    def report(self, filename="time_report.csv"):
        with open(filename, "w") as f:
            static_time = self.get_static_time()
            dynamic_time = self.get_dynamic_time()
            mutation_time = self.get_mutation_time()
            post_processing_time = self.get_post_processing_time()
            total_time = self.get_total_time()
            f.write('static_time,dynamic_time,mutation_time,post_processing_time,total_time\n')
            f.write(f"{static_time},{dynamic_time},{mutation_time},{post_processing_time},{total_time}")