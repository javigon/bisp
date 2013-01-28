'''
Created on Dec 20, 2012

@author: mabj
'''
def is_exported_float(func):
    func.is_exported = 'float'
    return func

def is_exported_string(func):
    func.is_exported = 'string'
    return func

def is_exported_integer(func):
    func.is_exported = 'integer'
    return func

