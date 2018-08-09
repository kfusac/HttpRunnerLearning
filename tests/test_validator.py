#!/usr/bin/python
#-*- coding: utf-8 -*-

import pytest

from httprunner import validator


class TestValidator:
    def test_is_variable(self):
        var1 = 123
        var2 = 'abc'
        assert validator.is_variable(('var1', var1))
        assert validator.is_variable(('var2', var2))

        __var = 123
        assert not validator.is_variable(('__var', __var))
        func = lambda x: x + 1
        assert not validator.is_variable(('func', func))
        assert not validator.is_variable(('pytest', pytest))

    def test_is_function(self):
        func = lambda x: x + 1
        assert validator.is_function(('func', func))
        assert validator.is_function(('func', validator.is_variable))
