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

class State(object):

    def __init__(self,var,this,val):
        super(State,self).__init__()
        self.var = var
        self.val = val
        self.this = this

    def __get__(self, instance, owner):
        return self.val

    def __set__(self,instance, value):
        self.val = value
        getattr(self.this.state,"%s_signal" % self.var).emit()

class StateManager(object):
    
    def __init__(self,parent):
        self.parent = parent

    def add(self,options):
        
        manager = self
        # NOTE 获取可用的 descriptor 
        class StateDescriptor(QtCore.QObject):
            signal_dict = {}
            var_dict = {}
            for var,val in options["state"].items():
                signal_dict["%s_signal" % var] = QtCore.Signal()
                var_dict[var] = State(var,manager.parent,val)
            locals().update(signal_dict)
            locals().update(var_dict)

        self.parent.state = StateDescriptor()
    
    def get(self,var):
        return getattr(self.parent.state,var)

    def bind(self,var,method,option):
        self.setSignal(var,method,option)
        getattr(self.parent.state,"%s_signal" % var).connect(partial(self.setSignal,var,method,option))
    
    def setSignal(self,var,method,option):
        state = self.parent.state
        if option == "str":
            val = str(getattr(state,var))
        elif option == "int":
            val = int(getattr(state,var))
        elif option == "float":
            val = float(getattr(state,var))
        elif callable(option):
            val = option(getattr(state,var))
        elif type(option) == dict:
            callback_args = option.get("set_callback_args",[])
            arg_list = [self.get(arg) for arg in callback_args]
            arg_list = arg_list if arg_list else [getattr(state,var)]
            callback = option.get("set_callback")
            val = callback(*arg_list) if callback else getattr(state,var)
        else:
            val = getattr(state,var)
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
            self.manager = StateManager(self)

            # NOTE 初始化变量
            self.manager.add(options)
            
            
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
                    self.manager.bind(var,method,option)
                
            return res
        return wrapper
    return handler