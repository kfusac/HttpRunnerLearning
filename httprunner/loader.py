import json
import yaml

from httprunner import expections


def load_yaml_file(yaml_file):
    '''
    load yaml file and check file content format
    '''

    with open(yaml_file, 'r', encoding='utf-8') as f:
        yaml_content = yaml.load(f)
        _check_format(yaml_file, yaml_content)
        if not isinstance(yaml_content, dict):
            err_msg = f'YAML file format error: {yaml_file}'
            raise expections.FileFormatError(err_msg)
        return yaml_content


def load_json_file(json_file):
    '''
    load json file and check file content format
    '''

    with open(json_file, encoding='utf-8') as data_file:
        try:
            json_content = json.load(data_file)
        except expections.JSONDecodeError:
            err_msg = f'JSONDecodeError: JSON file format error: {json_file}'
            print(err_msg)
            raise expections.FileFormatError(err_msg)

        _check_format(json_file, json_content)
        return json_content


def _check_format(file_path, content):
    '''
    check testcase format if vaild
    '''

    if not content:
        err_msg = f'Testcase file content is empty: {file_path}'
        print(err_msg)
        raise expections.FileFormatError(err_msg)
    elif not isinstance(content, (list, dict)):
        err_msg = f'testcase does content format invaild: {file_path}'
