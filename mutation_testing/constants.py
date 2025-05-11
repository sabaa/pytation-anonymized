# mutation testing process
TEST_SCRIPT_TEMPLATE_PARALLEL = "templates/dyn_test_script_template_parallel.tmp"
TEST_SCRIPT_TEMPLATE_SERIAL = "templates/dyn_test_script_template_one_proc.tmp"
TEST_SCRIPT_FILE = "dyn_test_script.py"

DEFAULT_TEST_PATTERN = 'test_*.py'
UNITTEST = 'unittest'
PYTEST = 'pytest'

TEST_PROCESS_MODULE = 'mutation_testing.test_process'

# mutation testing verifier
ONE_FILE_TEST_SCRIPT_TEMPLATE = 'templates/one_file_test_script_template.tmp'
ONE_FILE_TEST_SCRIPT_FILE = 'one_file_test_script.py'
SAMPLE_CODE_PATH = 'mutation_testing/tests/sample_codes'

# pattern list
DYNAMIC_PATTERN_FILENAME = "dynamic_patterns_list.json"
STATIC_PATTERN_FILENAME = "static_patterns_list.json"
UNCOVERED_PATTERN_FILENAME = "uncovered_patterns_list.json"
EQUIVALENT_PATTERN_FILENAME = "equivalent_patterns_list.json"

RANDOM_SELECTED_PATTERNS_FILENAME = "random_selected_patterns.json"
DIFF_SELECTED_PATTERNS_FILENAME = "diff_selected_patterns.json"

# report generation
HTML_REPORT_FILENAME = "mutation_testing_report.html"

DEFAULT_TIMEOUT = 50  # seconds

# subset selection strategy
RANDOM_STRATEGY = 'random'
OPERATOR_RANDOM_STRATEGY = 'operator_random'
OPERATOR_RANDOM_STRATEGY_THRESHOLD = 'operator_random_threshold'
OPERATOR_DIFF_STRATEGY = 'operator_diff'
