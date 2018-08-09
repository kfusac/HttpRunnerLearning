#!/usr/bin/python
#-*- coding: utf-8 -*-

import pytest

from httprunner import exceptions, parser


class TestParser:
    def test_parse_string_value(self):
        assert parser.parse_string_value('123') == 123
        assert parser.parse_string_value('12.3') == 12.3
        assert parser.parse_string_value('a123') == 'a123'
        assert parser.parse_string_value('$var') == '$var'
        assert parser.parse_string_value('$func()') == '$func()'

    def test_parse_function(self):
        assert parser.parse_function('func()') == {
            'func_name': 'func',
            'args': [],
            'kwargs': {}
        }
        assert parser.parse_function('func(5)') == {
            'func_name': 'func',
            'args': [5],
            'kwargs': {}
        }
        assert parser.parse_function('func(1, 2)') == {
            'func_name': 'func',
            'args': [1, 2],
            'kwargs': {}
        }
        assert parser.parse_function('func(a=1, b=2)') == {
            'func_name': 'func',
            'args': [],
            'kwargs': {
                'a': 1,
                'b': 2
            }
        }
        assert parser.parse_function('func(a = 1, b = 2 )') == {
            'func_name': 'func',
            'args': [],
            'kwargs': {
                'a': 1,
                'b': 2
            }
        }
        assert parser.parse_function('func(1, 2, a=3, b=4)') == {
            'func_name': 'func',
            'args': [1, 2],
            'kwargs': {
                'a': 3,
                'b': 4
            }
        }
        assert parser.parse_function('func($request,123)') == {
            'func_name': 'func',
            'args': ['$request', 123],
            'kwargs': {}
        }
        assert parser.parse_function('func(  )') == {
            'func_name': 'func',
            'args': [],
            'kwargs': {}
        }
        assert parser.parse_function('func(hello world, a=3, b=4)') == {
            'func_name': 'func',
            'args': ["hello world"],
            'kwargs': {
                'a': 3,
                'b': 4
            }
        }
        assert parser.parse_function('func($request, 12 3)') == {
            'func_name': 'func',
            'args': ["$request", "12 3"],
            'kwargs': {}
        }
