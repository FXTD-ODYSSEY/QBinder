# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-01 17:59:06'

import inspect
from PySide2 import QtCore

class State(object):
    
    def __init__(self,val):
        self.__val = val
    
    def __get__(self, instance, owner):
        print("__get__",owner)
        return self.__val

    def __set__(self, instance, val):
        print("__set__",val)
        self.__val = val
        
class StateDescriptor(QtCore.QObject):
    
    def __getitem__(self,key):
        print(self.__dict__)
        return self.__dict__[key]

    def __setitem__(self,key,value):
        self.__dict__[key] = value
    
    def __setattr__(self, key, value):
        print("attr",key,value)
        value = value if isinstance(value,State) else State(value)
        print(key,value)
        self.__dict__[key] = value

    def __getattr__(self, key):
        print("__getattr__")
        return self.__dict__[key].__val
    
    def _set_(self, instance, val):
        print("__set__",val)
        # self.__val = val

    # def __get__(self, *args, **kwargs):
    #     print("StateDescriptor __get__",args,kwargs)
        # return self.__dict__[key]
        # return self.__val


def connect_binding(cls):
    for name,descriptor in inspect.getmembers(cls):
        if isinstance(descriptor,StateDescriptor):
            break
    else:
        raise RuntimeError("No StateDescriptor Found")
    
    class StateDescriptorInstance(StateDescriptor):
        _var_dict = {n:s for n,s in inspect.getmembers(descriptor) if isinstance(s,State)}
        locals().update(_var_dict)
    
    setattr(cls,name,StateDescriptorInstance())
    return cls

@connect_binding
class TestCase(object):
    state = StateDescriptor()
    state.member = "member"
    state.number = 1
    
    # class StateDescriptor(QtCore.QObject):
    #     member = State("memeber")
    #     def __getitem__(self,key):
    #         return self.__dict__[key]

    #     def __setitem__(self,key,value):
    #         self.__dict__[key] = value

    def __init__(self):
        super(TestCase, self).__init__()
        print("start")
        self.a_str = 'a'
        self.member = StateDescriptor()
        callback = lambda: "%s test %s : %s %s" % (self.state.member,self.state.number,self.a_str,self.member)

        closure = callback.__closure__
        code = callback.__code__ 
        # print(dir(closure))
        for c in closure:
            print(c.cell_contents)
        
        res = inspect.getargspec (callback)
        print(res)
        # print(code.co_varnames)
        # print(dir(code))
        # for attr in dir(code):
        #     if not attr.startswith('__'):
        #         try:
        #             print(attr,getattr(code, attr))
        #         except:
        #             print(attr,'error')
        #             continue
                
case = TestCase()
# print(getattr(name))
