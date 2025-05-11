from subprocess import run
import os

ANALYSIS_PATH = "OperatorAnalysis"
MODULE = "mutation_testing.dynamic_analysis"

FULL_ANALYSIS_PATH = ".".join([MODULE, ANALYSIS_PATH])


def run_instrumentation(file_paths):
    # python -m dynapyt.instrument.instrument --files <path to Python file> --analysis <analysis class full dotted path>

    command = [
        "python",
        "-m",
        "dynapyt.instrument.instrument",
        "--analysis", FULL_ANALYSIS_PATH, "--files"]
    command.extend(file_paths)
    run(command)


def run_analysis(test_runner_script_path="dyn_test_helper.py"):
    # python -m dynapyt.run_analysis --entry <entry file (python)> --analysis <analysis class full dotted path>

    command = [
        "python",
        "-m",
        "dynapyt.run_analysis",
        "--entry", test_runner_script_path,
        "--analysis", FULL_ANALYSIS_PATH]
    run(command)


def restore_original_files(directory, excluded_directories=None, excluded_files=None):
    if excluded_directories is None:
        excluded_directories = set()
    if excluded_files is None:
        excluded_files = set()

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_directories]
        for filename in files:
            full_path = os.path.join(root, filename)

            if filename.endswith(".py.orig") and filename not in excluded_files:
                original_filename = filename[:-len(".orig")]
                original_path = os.path.join(root, original_filename)

                if os.path.exists(original_path):
                    os.replace(full_path, original_path)

            elif filename.endswith("-dynapyt.json") and filename not in excluded_files:
                os.remove(full_path)
