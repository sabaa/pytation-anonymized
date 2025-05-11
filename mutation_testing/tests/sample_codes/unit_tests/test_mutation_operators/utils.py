"""
This file is used to run the mutation testing for all the operators over sample codes.
This is NOT a part of the mutation testing framework. This is just a script to run the mutation testing
for all the test cases.
"""
import os.path
from os import walk
from mutation_testing.mutation_testing_verifier import MutationTestingVerifier


def get_all_file_names_in_dir(dir_path):
    file_names = []
    for (dir_root, dir_names, filenames) in walk(dir_path):
        file_names.extend(filenames)
        break
    if '__init__.py' in file_names:
        file_names.remove('__init__.py')
    refined_file_names = []
    for f in file_names:
        if f.endswith('.py'):
            refined_file_names.append(f)
    return refined_file_names


def run_for_operator(op_name_arg):
    base_dir = 'mutation_testing/tests/sample_codes'
    operator_name_sample = '/' + op_name_arg
    sample_code_dir = base_dir + operator_name_sample
    sample_file_names = get_all_file_names_in_dir(sample_code_dir + '/code')
    print('Sample file names: ', sample_file_names)
    test_file_names = get_all_file_names_in_dir(sample_code_dir + '/test')
    print('Test file names: ', test_file_names)

    for sample_file in sample_file_names:
        print('---------------------------')
        print('Sample file: ', sample_file)
        test_code_file = sample_code_dir + '/test/' + 'test_' + sample_file
        source_code_file = sample_code_dir + '/code/' + sample_file
        mutation_testing = MutationTestingVerifier(source_code_file, test_code_file)
        mutation_testing.run()
        print('---------------------------')


for i in ('dynamic_patterns_list.json', 'one_file_test_script.py', 'static_patterns_list.json'):
    if os.path.exists(i):
        os.remove(i)

op_names = ['delete_function_argument']


for op_name in op_names:
    print('Operator: ', op_name)
    run_for_operator(op_name)
    print('---------------------------')
