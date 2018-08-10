import os
import pytest

from httprunner import exceptions, loader
import importlib


class TestFileLoader:
    def test_load_json_file_format_error(self):
        json_tmp_file_path = 'tests/data/tmp.json'

        #create empty file
        with open(json_tmp_file_path, 'w') as f:
            f.write('')

        with pytest.raises(exceptions.FileFormatError):
            loader.load_json_file(json_tmp_file_path)

        os.remove(json_tmp_file_path)

        # create empty json file
        with open(json_tmp_file_path, 'w') as f:
            f.write('{}')

        with pytest.raises(exceptions.FileFormatError):
            loader.load_json_file(json_tmp_file_path)

        os.remove(json_tmp_file_path)

        # create invaild format json file
        with open(json_tmp_file_path, 'w') as f:
            f.write('abc')

        with pytest.raises(exceptions.FileFormatError):
            loader.load_json_file(json_tmp_file_path)

        os.remove(json_tmp_file_path)

    def test_load_yaml_file_format_error(self):
        yml_tmp_file_path = 'tests/data/tmp.yml'

        #create empty file
        with open(yml_tmp_file_path, 'w') as f:
            f.write('')

        with pytest.raises(exceptions.FileFormatError):
            loader.load_yaml_file(yml_tmp_file_path)

        os.remove(yml_tmp_file_path)

        # create invaild format yaml file
        with open(yml_tmp_file_path, 'w') as f:
            f.write('abc')

        with pytest.raises(exceptions.FileFormatError):
            loader.load_yaml_file(yml_tmp_file_path)

        os.remove(yml_tmp_file_path)

    def test_locate_file(self):
        with pytest.raises(exceptions.FileNotFoundError):
            loader.locate_file(os.getcwd(), 'custom_functions.py')

        with pytest.raises(exceptions.FileNotFoundError):
            loader.locate_file('', 'custom_functions.py')

        start_path = os.path.join(os.getcwd(), 'tests')
        assert loader.locate_file(start_path,
                                  'custom_functions.py') == os.path.join(
                                      'tests', 'custom_functions.py')

        assert loader.locate_file('tests/',
                                  'custom_functions.py') == os.path.join(
                                      'tests', 'custom_functions.py')

        assert loader.locate_file('tests',
                                  'custom_functions.py') == os.path.join(
                                      'tests', 'custom_functions.py')

        assert loader.locate_file('tests/base.py',
                                  'custom_functions.py') == os.path.join(
                                      'tests', 'custom_functions.py')

        assert loader.locate_file('tests/testcase/smoke_test.yml',
                                  'custom_functions.py') == os.path.join(
                                      'tests', 'custom_functions.py')


class TestModuleLoader:
    def test_load_python_module(self):
        pytest_module_items = loader.load_python_module(pytest)
        assert 'mark' in pytest_module_items['variables']
        assert 'skip' in pytest_module_items['functions']

    def test_load_custom_function_module(self):
        imported_custom_functions_module = loader.load_custom_function_module()
        assert {} == imported_custom_functions_module['variables']
        assert {} == imported_custom_functions_module['functions']

        imported_custom_functions_module = loader.load_custom_function_module(
            'tests')
        assert 'http://127.0.0.1:5000' == imported_custom_functions_module[
            'variables']['BASE_URL']
        assert 'gen_md5' in imported_custom_functions_module['functions']

        is_status_code_200 = imported_custom_functions_module['functions'][
            'is_status_code_200']
        assert is_status_code_200(200)
        assert not is_status_code_200(500)
