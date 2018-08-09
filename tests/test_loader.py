import os
import pytest

from httprunner import exceptions, loader


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
        assert loader.locate_file(
            start_path, 'custom_functions.py') == os.path.join('tests','custom_functions.py')

        assert loader.locate_file(
            'tests/', 'custom_functions.py') == os.path.join('tests','custom_functions.py')

        assert loader.locate_file(
            'tests', 'custom_functions.py') == os.path.join('tests','custom_functions.py')

        assert loader.locate_file(
            'tests/base.py',
            'custom_functions.py') == os.path.join('tests','custom_functions.py')

        assert loader.locate_file(
            'tests/testcase/smoke_test.yml',
            'custom_functions.py') == os.path.join('tests','custom_functions.py')
