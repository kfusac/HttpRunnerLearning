#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import ast

from httprunner import exceptions

function_regexp = r'^\$\{(\w+)\(([\$\w =,]*)\)\}$'
function_regexp_compile = re.compile(r'^(\w+)\(([\$\w =,]*)\)$')


def parse_string_value(str_value):
    '''
    safe eval prevent code inject
    '''

    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        return str_value


def parse_function(content):
    '''
    parse function expression
    
    Args:
        expression
    
    Returns:
        function metadata
    '''

    matched = function_regexp_compile.match(content)

    if not matched:
        raise exceptions.FunctionNotFoundError(f'{content} not found!')

    function_meta = {"func_name": matched.group(1), "args": [], "kwargs": {}}

    args_str = matched.group(2).strip()
    if args_str == "":
        return function_meta

    args_list = args_str.split(',')
    for arg in args_list:
        arg = arg.strip()
        if '=' in arg:
            key, value = arg.split('=')
            function_meta['kwargs'][key.strip()] = parse_string_value(
                value.strip())
        else:
            function_meta['args'].append(parse_string_value(arg))

    return function_meta