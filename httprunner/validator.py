#!/usr/bin/python
#-*- coding: utf-8 -*-

import types


def is_function(tup):
    '''
    takes (name, object) tuple, return True if object is a function.
    '''

    name, item = tup
    return isinstance(item, types.FunctionType)
