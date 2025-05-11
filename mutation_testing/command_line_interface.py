import argparse

from mutation_testing.mutation import MutationTesting
from mutation_testing.config import ConfigManager, Config


def main():
    parser = argparse.ArgumentParser(description="Python Project Test Runner")
    parser.add_argument("-r", "--root-directory", required=True, help="Root directory of the Python project")
    parser.add_argument("-x", "--exclude-directories", nargs="+", help="Paths to the directories to be excluded")
    parser.add_argument("-m", "--test-runner", default="pytest", help="Choose between pytest and unittest")
    parser.add_argument("-i", "--include-directories", nargs="+", help="Paths to the directories to be included")
    parser.add_argument("-p", "--exclude-patterns", nargs="+", help="Patterns to exclude from the result")
    parser.add_argument("-t", "--test_root", nargs="+", help="Root for test files, by default it is the root directory")
    parser.add_argument("-ne", "--no-equivalency-check", action="store_true", help="Turn off equivalency check heuristics")
    parser.add_argument("-nm", "--no-mutation", action="store_true", help="Turn off mutation, only run detection")
    parser.add_argument("-nd", "--no-detection", action="store_true", help="Turn off detection, only run mutation")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean the mutation testing results")
    parser.add_argument("-ts", "--test-script", help="Test script to run the tests")
    parser.add_argument("-gpr", "--generate-pre-report", action="store_true", help="Generate pre-report")
    parser.add_argument("-dl", "--disable-logging", action="store_true", help="Disable logging")
    parser.add_argument("-pl", "--parallel-level", default='8', help="Number of parallel processes to run tests")
    parser.add_argument("-ss", "--subset-selection", default='no_op', help="Enable subset selection")
    # Using with operator_random_threshold
    parser.add_argument("-ssv", "--subset-value", default='0', help="Subset selection value")
    parser.add_argument("-sst", "--subset-threshold", default='10', help="Subset selection threshold")
    # Using with operator_diff
    parser.add_argument("-commit-before", "--commit-before", help="Commit hash before fixing")
    parser.add_argument("-commit-after", "--commit-after", help="Commit hash after fixing")

    parser.add_argument("-to", "--timeout-co", default='3', help="Timeout coefficient for each test case")

    args = parser.parse_args()

    if args.clean:
        clean_results()
        return

    test_root = args.test_root if args.test_root else args.root_directory
    main_directories = args.include_directories if args.include_directories else args.root_directory

    if args.generate_pre_report:
        from mutation_testing.pre_report import generate_pre_report
        print(generate_pre_report(main_directories, test_root, str(args.parallel_level)))
        return

    _config = Config()
    if args.no_equivalency_check:
        _config.equivalency_check = False
    if args.no_mutation:
        _config.mutation = False
    if args.no_detection:
        _config.detection = False
    if args.disable_logging:
        _config.logging = False
    if args.subset_selection != 'no_op':
        _config.subset_selection = True
    ConfigManager.set_config(_config)

    run_mutation_testing(
        root_directory=args.root_directory,
        exclude_directories=args.exclude_directories,
        test_runner=args.test_runner,
        include_directories=args.include_directories,
        exclude_patterns=args.exclude_patterns,
        test_root=test_root,
        test_script=args.test_script,
        parallel_level=args.parallel_level,
        subset_selection=args.subset_selection,
        selection_value=args.subset_value,
        selection_threshold=args.subset_threshold,
        timeout_coefficient=args.timeout_co,
        commit_before=args.commit_before,
        commit_after=args.commit_after
    )


def run_mutation_testing(
        root_directory,
        exclude_directories,
        test_runner,
        include_directories,
        exclude_patterns,
        test_root,
        test_script,
        parallel_level,
        subset_selection,
        selection_value,
        selection_threshold,
        timeout_coefficient,
        commit_before=None,
        commit_after=None
):
    mutation_testing = MutationTesting(
        root_directory=root_directory,
        exclude_directories=exclude_directories,
        include_directories=include_directories,
        exclude_patterns=exclude_patterns,
        test_runner=test_runner,
        test_root=test_root,
        test_script=test_script,
        parallel_level=str(parallel_level),
        subset_selection=subset_selection.strip(),
        selection_value=float(selection_value),
        selection_threshold=int(selection_threshold),
        timeout_coefficient=int(timeout_coefficient),
        commit_before=commit_before,
        commit_after=commit_after
    )
    mutation_testing.run()


def clean_results():
    MutationTesting.clean_up()


if __name__ == '__main__':
    main()
