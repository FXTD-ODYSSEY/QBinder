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
    
    container = set()
    
    def __init__(self,val):
        self._val = val
    
    def __get__(self, instance, owner):
        print("__get__",owner)
        self.container.add(self)
        return self._val

    def __set__(self, instance, val):
        print("__set__",val)
        self._val = val
        
class StateDescriptor(QtCore.QObject):
    
    _var_dict = {}
    
    def __getitem__(self,key):
        return self._var_dict[key]

    # def __setitem__(self,key,value):
    #     self._var_dict[key] = value
    
    def __setattr__(self, key, value):
        print("attr",key,value)
        value = value if isinstance(value,State) else State(value)
        print(key,value)
        self.__dict__[key] = value

    def __getattr__(self, key):
        print("__getattr__")
        return self.__dict__[key]._val
    
    def __(self, instance, val):
        print("__set__",val)
        # self.__val = val

    # def __get__(self, *args, **kwargs):
    #     print("StateDescriptor __get__",args,kwargs)
        # return self.__dict__[key]
        # return self.__val


def connect_binding(cls):
    """ https://stackoverflow.com/questions/11091609/setting-a-class-metaclass-using-a-decorator """

    for name,descriptor in inspect.getmembers(cls):
        if isinstance(descriptor,StateDescriptor):
            break
    else:
        raise RuntimeError()

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
        print(self.state.)
        print(self.state["member"])
        
        # self.a_str = 'a'
        # callback = lambda: "%s test %s : %s %s" % (self.state.member,self.state.number,self.a_str)
        
        # self.test_call(callback)

    @staticmethod
    def test_call(callback):
        State.container.clear()
        val = callback()
        print(State.container)
        print(val)


case = TestCase()
# print(getattr(name))
