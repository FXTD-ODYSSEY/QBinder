# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-10-30 19:42:26'

import inspect
import threading
from PySide2 import QtCore



    

class SingletonType(type):
    _instance_lock = threading.Lock()
    
    
    def __init__(cls, name, bases, dic):
        super(SingletonType, cls).__init__(name, bases, dic)
        # print(cls,name,bases,dic)
        
        
    def __call__(cls, *args, **kwargs):
        # print(args)
        
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
                    
        cls._instance.__addvar__(*args)
        return cls._instance
    
    # def __new__(cls, name, bases, attrs):
    #     # print(name,bases,attrs)
    #     return super(SingletonType,cls).__new__(cls, name, bases, attrs)

    
        
        
class Binding(object):
    
    def __init__(self,val):
        self.__val = val
        
    # def __get__(self, instance, owner):
    #     return self.__val

    # def __set__(self, instance, val):
    #     self.__val = val

class GBinding(Binding):
    pass

class DataBinding(type):
    
    def __init__(cls, name, bases, attrs):
        super(DataBinding, cls).__init__(name, bases, attrs)
        for member,val in inspect.getmembers(cls):
            if isinstance(val,Binding):
                print(member,val)

def connect_binding(cls):
    """ https://stackoverflow.com/questions/11091609/setting-a-class-metaclass-using-a-decorator """
    __dict = dict(cls.__dict__)
    __dict["__metaclass__"] = DataBinding
    __dict["__wrapped__"] = cls
    return(DataBinding(cls.__name__, cls.__bases__, __dict))

class StateDescriptor(QtCore.QObject):
                
    def __getitem__(self,key):
        return self.__dict__[key]

    def __setitem__(self,key,value):
        self.__dict__[key] = value
        
    def __setattr__(self, key, value):
        print("attr",key,value)
        self.__dict__[key] = value
        
@connect_binding
class Component(object):
    
    state = StateDescriptor()
    state.number = 1
    state.string = "1"
    state.loc = True
    
    def __init__(self,*args,**kwargs):
        super(Component, self).__init__(*args,**kwargs)
        number = self.state.number
        string = self.state.string
        print(number,string)
    

comp = Component()

# print(dir(comp.temple))

