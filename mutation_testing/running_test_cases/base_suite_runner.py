from coverage import Coverage


class BaseSuiteRunner:
    def __init__(self):
        self.coverage_data = None
        self._initialize()

    def _initialize(self):
        self.coverage = Coverage()

    def create_test_suite(self):
        raise NotImplementedError

    def run_tests(self, project_root=None):
        raise NotImplementedError

    def get_result(self):
        raise NotImplementedError

    def calculate_coverage(self):
        raise NotImplementedError

    def print_coverage_report(self):
        raise NotImplementedError

    def get_covered_lines(self):
        raise NotImplementedError
