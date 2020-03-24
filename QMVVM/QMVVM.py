# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 14:44:34'

"""

"""

import sys
import inspect

from functools import wraps
from functools import partial
from PySide2 import QtCore
from state import StateFactory

# @QMVVM.store({
#     "state":{
#         "count":0,
#     },
#     "binding":{
#         "count":{
#             "label.setText":"str",
#             "@label2.setText":{
#                 "set_callback_args":["count"],
#                 "set_callback":lambda count: "<center>%s</center>"%count,
#             },
#             "@label3.setText":lambda count: "<center>%s</center>" % count,
#         },
#     },
# })

class StateSignal(QtCore.QObject):

    updated = QtCore.Signal()

    def __init__(self):
        super(StateSignal,self).__init__()

class State(object):

    def __init__(self,manager,val):
        super(State,self).__init__()
        self.val = val
        self.manager = manager
        self.singal = StateSignal()

    def __get__(self, instance, owner):
        print "get"
        return self.val

    def __set__(self,instance, value):
        print "set",value
        self.val = value
        self.singal.updated.emit()

    def bind(self,method,option):
        self.setSignal(method,option)
        self.singal.updated.connect(partial(self.setSignal,method,option))
    
    def setSignal(self,method,option):
        if not option:
            val = self.val
        elif option == "str":
            val = str(self.val)
        elif option == "int":
            val = int(self.val)
        elif option == "float":
            val = float(self.val)
        elif callable(option):
            val = option(self.val)
        elif type(option) == dict:
            callback_args = option.get("set_callback_args",[])
            arg_list = [self.manager.get(arg).val for arg in callback_args]
            arg_list = arg_list if arg_list else [self.val]
            callback = option.get("set_callback")
            val = callback(*arg_list) if callback else self.val
        method(val)

class StateManager(object):
    
    def __init__(self):
        pass

    def add(self,var,val):
        setattr(self,var,State(self,val))
        # setattr(self,"%s_signal" % var,val)
    
    def get(self,var):
        return getattr(self,var)

    def bind(self,var,method,option):
        getattr(self,var).bind(method,option)

def store(options):
    def handler(func):
        
        def parseMethod(self,method):
            if method.startswith("@"):
                data = method[1:].split(".")
                method = self._locals[data[0]]
            else:
                data = method.split(".")
                method = getattr(self,data[0])
            for attr in data[1:]:
                method = getattr(method,attr)
            return method
        

        @wraps(func)
        def wrapper(self,*args, **kwargs):
            self.state = StateManager()
            for var,val in options["state"].items():
                self.state.add(var,val)
            
            # NOTE https://stackoverflow.com/questions/9186395
            # NOTE 获取函数中的 locals 变量
            self._locals = {}
            sys.setprofile(lambda f,e,a: self._locals.update(f.f_locals) if e=='return' else None)
            res = func(self,*args, **kwargs)
            sys.setprofile(None)

            for var,data in options["binding"].items():
                for method,option in data.items():
                    # NOTE 获取 local 或 self 相关处理 method 
                    method = parseMethod(self,method)
                    
                    # method(val)
                    self.state.bind(var,method,option)
                    
                
            return res
        return wrapper
    return handler