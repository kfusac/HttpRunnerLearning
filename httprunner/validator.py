#!/usr/bin/python
#-*- coding: utf-8 -*-

import types


def is_function(tup):
    '''
    takes (name, object) tuple, return True if object is a function.
    '''

    name, item = tup
    return isinstance(item, types.FunctionType)

def is_variable(tup):
    '''
    takes (name, object) tuple, return True if opject is a variable.
    '''
    
    name,item=tup

    if callable(item):
        # function or class
        return False
    
    if isinstance(item,types.ModuleType):
        # imported module
        return False
    
    if name.startswith('_'):
        # private property
        return False
    
    return True
