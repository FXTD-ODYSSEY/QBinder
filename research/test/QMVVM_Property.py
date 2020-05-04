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

# @QBinding.store({
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

class StateManager(QtCore.QObject):
    
    def __init__(self):
        super(StateManager,self).__init__()
    
    def getProperty(self,var):
        return getattr(self,"_%s" % var)

    def setProperty(self,var,val):
        setattr(self,"_%s" % var,val)
        signal = getattr(self,"_%s_signal" % var)
        signal.updated.emit()
    
    def add(self,var,val):
        setattr(self,"_%s" % var,val)
        setattr(self,"_%s_signal" % var,StateSignal())

        getter = partial(self.getProperty,var)
        setter = partial(self.setProperty,var)
        setattr(self,var,QtCore.Property(type(val), getter, setter))
    
    def get(self,var):
        return getattr(self,var)

    def bind(self,var,method,option):
        signal = getattr(self,"_%s_signal" % var)
        signal.updated.connect(partial(self.setSignal,method,option))

    def setSignal(self,method,option):
        if not option:
            val = self.__val
        elif option == "str":
            val = str(self.__val)
        elif option == "int":
            val = int(self.__val)
        elif option == "float":
            val = float(self.__val)
        elif callable(option):
            val = option(self.__val)
        elif type(option) == dict:
            callback_args = option.get("set_callback_args",[])
            arg_list = [self.__manager.get(arg) for arg in callback_args]
            arg_list = arg_list if arg_list else [self.__val]
            callback = option.get("set_callback")
            val = callback(*arg_list) if callback else self.__val
        print "val",val
        method(val)

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