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
from Qt import QtCore
from hook import HOOKS
class State(object):

    def __init__(self,var,widget,val):
        super(State,self).__init__()
        self.var = var
        self.val = val
        self.widget = widget

    def __get__(self, instance, owner):
        # print 'asd'
        return self.val() if callable(self.val) else self.val

    def __set__(self,instance, value):
        self.val = value
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def setUpdater(self,updaters):
        for updater in updaters:
            updater.connect(self.setVal)
            
    def setVal(self,val):
        self.val = val
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

class StateManager(object):
    
    def __init__(self,parent):
        self.parent = parent

    def add(self,options):
        
        manager = self
        # NOTE 获取可用的 descriptor 
        class StateDescriptor(QtCore.QObject):
            __signal_dict = {}
            _var_dict = {}
            for var,val in options["state"].items():
                __signal_dict["_%s_signal" % var] = QtCore.Signal()
                _var_dict[var] = State(var,manager.parent,val)
            locals().update(__signal_dict)
            locals().update(_var_dict)

        self.parent.state = StateDescriptor()
    
    def bind(self,var,method,option=None):
        # NOTE 赋予初值
        self.setSignal(var,method,option)
        # NOTE 连接信号槽
        getattr(self.parent.state,"_%s_signal" % var).connect(partial(self.setSignal,var,method,option))

    def setSignal(self,var,method,option):
        state = self.parent.state
        val = getattr(state,var)
        if option == "str":
            val = str(val)
        elif option == "int":
            val = int(val)
        elif option == "float":
            val = float(val)
        elif callable(option):
            val = option(val)
        elif type(option) is dict:
            callback_args = option.get("args",[])
            # NOTE 从 state 获取变量 | 获取不到则从 self 里面获取
            arg_list = []
            for arg in callback_args:
                if arg.startswith("$"):
                    arg = getattr(self.parent,arg[1:])
                elif hasattr(self.parent.state,arg):
                    arg = getattr(self.parent.state,arg)
                else:
                    arg = getattr(self.parent,arg)
                arg_list.append(arg)

            # arg_list = [getattr(self.parent.state,arg) if hasattr(self.parent.state,arg) else getattr(self.parent,arg) for arg in callback_args if not arg.startswith("$")]
            # arg_list.extend([getattr(self.parent,arg[1:]) for arg in callback_args if arg.startswith("$")])
            # arg_list = arg_list if arg_list else [val]
            callback = option.get("action")
            # NOTE 如果 callback 是字符串则获取 parent 的方法
            callback = getattr(self.parent,callback) if type(callback) is str else callback
            # NOTE 如果 callback 是字符串则获取 parent 的方法
            val = callback(*arg_list) if callable(callback) else val
        method(val)

def store(options):
    def handler(func):
        
        def parseMethod(self,method,ret_widget=False):
            if method.startswith("@"):
                data = method[1:].split(".")
                widget = self._locals[data[0]]
            else:
                data = method.split(".")
                widget = getattr(self,data[0])
            
            for attr in data[1:-1]:
                widget = getattr(widget,attr)
            
            return (getattr(widget,data[-1]),widget) if ret_widget else getattr(widget,data[-1])

        def parseGetter(self,val):
            default = None
            data = val()
            if type(data) is str:
                return [parseMethod(self,data)],default
            elif type(data) is dict:
                default = data["default"]
                updater = data["updater"]
                if type(updater) is str:
                    return [parseMethod(self,updater)],default
                elif type(updater) is tuple or type(updater) is list:
                    return [parseMethod(self,u) for u in updater],default

            elif type(data) is tuple or type(data) is list:
                return [parseMethod(self,u) for u in data],default
            else:
                raise NotImplementedError('unknown return val')

        @wraps(func)
        def wrapper(self,*args, **kwargs):
            self.__state_manager = StateManager(self)

            # NOTE 初始化变量 | 初始化 self.state 变量
            self.__state_manager.add(options)
            
            # NOTE https://stackoverflow.com/questions/9186395
            # NOTE 获取函数中的 locals 变量
            self._locals = {}
            sys.setprofile(lambda f,e,a: self._locals.update(f.f_locals) if e=='return' else None)
            res = func(self,*args, **kwargs)
            sys.setprofile(None)

            state = options.get("state",{})
            for var,val in state.items():
                if not callable(val):continue
                updaters,default = parseGetter(self,val) 
                self.state._var_dict[var].setUpdater(updaters)
                # NOTE 根据 state 设定初值
                if options["state"][var] == self.state._var_dict[var].val:
                    self.state._var_dict[var].val = default

            # NOTE 根据设置进行绑定
            bindings = options.get("bindings",{})
            for var,data in bindings.items():
                if type(data) == dict:
                    for method,option in data.items():
                        method = parseMethod(self,method)
                        self.__state_manager.bind(var,method,option)
                elif type(data) == list or type(data) == tuple:
                    for method in data:
                        method = parseMethod(self,method)
                        self.__state_manager.bind(var,method)

            methods = options.get("methods",{})
            for _method,option in methods.items():
                method,widget = parseMethod(self,_method,True)
                rel = HOOKS.get(type(widget),None)
                # NOTE 过滤不在 HOOKS 里面的绑定 
                if rel is None: continue
                
                # TODO 判断是否在 hooks 里面记录的类型
                # print type(method)
                # if str(type(method)) != "<type 'builtin_function_or_method'>":
                #     continue
                # NOTE 默认自动将方法绑定到所有的 state setter 里面
                for var in option.get("bindings",state):
                    self.__state_manager.bind(var,method,option)
                
            return res
        return wrapper
    return handler