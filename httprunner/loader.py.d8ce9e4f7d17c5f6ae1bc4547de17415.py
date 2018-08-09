import os
import json
import yaml

from httprunner import exceptions, validator

###############################################################################
##   file loader
###############################################################################

def load_yaml_file(yaml_file):
    '''
    load yaml file and check file content format
    '''

    with open(yaml_file, 'r', encoding='utf-8') as f:
        yaml_content = yaml.load(f)
        _check_format(yaml_file, yaml_content)
        if not isinstance(yaml_content, dict):
            err_msg = f'YAML file format error: {yaml_file}'
            raise exceptions.FileFormatError(err_msg)
        return yaml_content


def load_json_file(json_file):
    '''
    load json file and check file content format
    '''

    with open(json_file, encoding='utf-8') as data_file:
        try:
            json_content = json.load(data_file)
        except exceptions.JSONDecodeError:
            err_msg = f'JSONDecodeError: JSON file format error: {json_file}'
            print(err_msg)
            raise exceptions.FileFormatError(err_msg)

        _check_format(json_file, json_content)
        return json_content

def locate_file(start_path,file_name):
    '''
    locate filename and return file path.
    searching will be recursive upward until currect working directory.
    
    Args:
        start_path (str): start locating path, maybe file path or directory path
        file_name (str): target file name
    
    Returns:
        str: located file path. None if file not found.
    
    Raises:
        exceptions.FileNotFoundError: If failed to locate file.
    '''
    
    if os.path.isfile(start_path):
        start_dir_path=os.path.dirname(start_path)
    elif os.path.isdir(start_path):
        start_dir_path=start_path
    else:
        raise exceptions.FileFormatError(f'invaild path: {start_path}')
    
    file_path=os.path.join(start_dir_path,file_name)
    if os.path.isfile(file_path):
        if os.path.isabs(file_path):
            file_path=file_path[len(os.getcwd())+1:]
        return file_path
    
    if os.path.abspath(start_dir_path)==os.getcwd():
        raise exceptions.FileNotFoundError(f'{file_name} not found in {start_path}')
    
    return locate_file(os.path.dirname(start_dir_path),file_name)

def _check_format(file_path, content):
    '''
    check testcase format if vaild
    '''

    if not content:
        err_msg = f'Testcase file content is empty: {file_path}'
        print(err_msg)
        raise exceptions.FileFormatError(err_msg)
    elif not isinstance(content, (list, dict)):
        err_msg = f'testcase does content format invaild: {file_path}'

###############################################################################
##   module loader
###############################################################################

def convert_module_name(python_file_path):
    '''
    convert python file relative path to module name.
    
    Args:
        python_file_path (str): python file relative path
    
    Returns:
        str: module name
    '''

    module_name = python_file_path.replace('/', '.').rstrip('.py')
    return module_name


def load_python_module(module):
    '''
    load python module.
    
    Args:
        module: python module
    
    Returns:
        dict: variables and functions mapping for specified python module

            {
                'variables':{},
                'functions':{}
            }
    '''

    modules = {'variables': {}, 'functions': {}}
    for name, item in vars(module).items():
        if validator.is_function((name, item)):
            modules['functions'][name] = item
        elif validator.is_variable((name, item)):
            modules['variables'][name] = item
        else:
            pass

    return modules


def load_custom_function_module(start_path=None):
    '''
    load custom function module,default custom_function.py
    
    Args:
        start_path (str, optional): start locating path, maybe file path or directory path.
        Defuault to currect working directory.
    
    Returns:
        dict: variables and functions mapping for custom_function.py

            {
                'variables': {},
                'functions': {}
            }
    '''

    start_path = start_path or os.getcwd()

    try:
        module_path = 'tests/'
    except expression as identifier:
        pass


