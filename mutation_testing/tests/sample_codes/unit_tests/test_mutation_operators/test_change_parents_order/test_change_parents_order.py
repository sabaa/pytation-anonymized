import pytest
import os
import ast

from mutation_testing.mutation_operators.change_parents_order import ChangeParentsOrder, PatternStatus, HookName
from mutation_testing.mutation_testing_verifier import MutationTestingVerifier

base_dir = 'mutation_testing/tests/sample_codes'
operator_name_sample = '/change_parents_order'
sample_code_dir = base_dir + operator_name_sample

file_names = ['init_inheritance.py']

class TestChangeParentsOrder:

    @pytest.fixture
    def mutation_operator(self):
        return ChangeParentsOrder()

    def test_static_analysis(self, mutation_operator):
        assert not mutation_operator.static_analysis

    def test_dynamic_analysis(self, mutation_operator):
        assert mutation_operator.dynamic_analysis

    def test_node_type(self, mutation_operator):
        assert mutation_operator.node_type == ast.ClassDef

    def test_hook_name(self, mutation_operator):
        assert mutation_operator.hook_name == HookName.POST_CALL

    def test_is_dynamic_pattern_not_found(self, mutation_operator):
        dynamic_data = {"call": None}
        assert mutation_operator._is_dynamic_pattern(dynamic_data) == PatternStatus.NOT_FOUND

    def test_sample_code_init_inheritance(self):
        source_code_file = sample_code_dir + "/code" + "/init_inheritance.py"
        test_code_file = sample_code_dir + "/test" + "/test_init_inheritance.py"
        mutation_testing = MutationTestingVerifier(
            source_code_file, test_code_file, dynamic_analysis=True, static_analysis=False)
        patterns, equivalents, uncovered = mutation_testing.get_patterns()

    # def test_mutate(self):
    #     mutation_operator = ChangeParentsOrder()
    #     node = ast.ClassDef()
    #     node.bases = [ast.Name(id="Base1"), ast.Name(id="Base2")]
    #     mutated_node = mutation_operator.mutate(node)
    #     assert mutated_node.bases == [ast.Name(id="Base2"), ast.Name(id="Base1")]


    def teardown_method(self):
        for i in ('dynamic_patterns_list.json', 'one_file_test_script.py', 'static_patterns_list.json'):
            if os.path.exists(i):
                os.remove(i)
