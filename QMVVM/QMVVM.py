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
from .hook import HOOKS
from .exception import SchemeParseError

def notify(func):
    def wrapper(self,*args,**kwargs):
        print "notify",args
        # NOTE 更新数据
        res = func(self,*args,**kwargs)
        # NOTE 更新组件信息
        getattr(self.STATE.widget.state,"_%s_signal" % self.STATE.var).emit()
        return res
    return wrapper

class NotifyList(list):
    """
    https://stackoverflow.com/questions/13259179/list-callbacks
    监听数组的内置函数更新组件数据
    """
    def __init__(self,val,STATE):
        list.__init__(self,val)
        self.STATE = STATE

    extend = notify(list.extend)
    append = notify(list.append)
    remove = notify(list.remove)
    pop = notify(list.pop)
    __iadd__ = notify(list.__iadd__)
    __imul__ = notify(list.__imul__)

    #Take care to return a new NotifyList if we slice it.
    if sys.version_info[0] < 3:
        __setslice__ = notify(list.__setslice__)
        __delslice__ = notify(list.__delslice__)
        def __getslice__(self,*args):
            return self.__class__(list.__getslice__(self,*args))

    __delitem__ = notify(list.__delitem__)
    
    def __getitem__(self,item):
        if isinstance(item,slice):
            return self.__class__(list.__getitem__(self,item))
        else:
            return list.__getitem__(self,item)

    @notify
    def __setitem__(self,key,value):
        if type(value) is dict:
            value = NotifyDict(value,self.STATE)
        elif type(value) is list:
            value = NotifyList(value,self.STATE)
        list.__setitem__(self,key,value)

class NotifyDict(dict):
    """
    https://stackoverflow.com/questions/5186520/python-property-change-listener-pattern
    """
    def __init__(self,val,STATE):
        dict.__init__(self,val)
        self.STATE = STATE

    # __setitem__ = notify(dict.__setitem__)
    clear = notify(dict.clear)
    pop = notify(dict.pop)
    popitem = notify(dict.popitem)
    setdefault = notify(dict.setdefault)
    update =  notify(dict.update)
    __delitem__ = notify(dict.__delitem__)

    @notify
    def __setitem__(self,key,value):
        if type(value) is dict:
            value = NotifyDict(value,self.STATE)
        elif type(value) is list:
            value = NotifyList(value,self.STATE)
        dict.__setitem__(self,key,value)
    

class State(object):
    __map_type = {
        list:NotifyList,
        dict:NotifyDict,
    }
    def __init__(self,var,widget,val):
        super(State,self).__init__()
        self.var = var
        self.widget = widget

        self.retrieveVal(val,self)
        self.val = self.__map_type.get(type(val),lambda *arg:arg[0])(val,self)
        # self.val = val

    def __get__(self, instance, owner):
        return self.val().get("default") if callable(self.val) else self.val

    def __set__(self,instance, value):
        self.val = value
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def setUpdater(self,updaters):
        for updater in updaters:
            updater.connect(self.setVal)
            
    def setVal(self,val):
        self.val = val
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def retrieveVal(self,val,STATE):
        """
        遍历所有字典和数组对象，转换为 Notify 对象
        """
        itr = val.items() if type(val) is dict else enumerate(val) if type(val) is list else []
        for k,v in itr:        
            if isinstance(v, dict):
                self.retrieveVal(v,STATE)
                val[k] = NotifyDict(v,STATE)
            elif isinstance(v, list):            
                self.retrieveVal(v,STATE)
                val[k] = NotifyList(v,STATE)

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
    
    def bind(self,var,method,option=None,typ=None):
        # NOTE 赋予初值
        setter = lambda:self.setSignal(var,method,option,typ)
        setter()
        # NOTE 连接信号槽
        getattr(self.parent.state,"_%s_signal" % var).connect(setter)

    def parseAction(self,option):
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

        callback = option.get("action")
        # NOTE 如果 callback 是字符串则获取 parent 的方法
        callback = callback if type(callback) is not str else getattr(self.parent,callback[1:]) if callback.startswith("$") else getattr(self.parent.state,callback)
        # NOTE 如果 callback 是字符串则获取 parent 的方法
        val = callback(*arg_list) if callable(callback) else callback
        return val
        
    def setSignal(self,var,method,option,typ):
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
            val = self.parseAction(option)
        method(typ(val) if typ else val)

def store(options):
    def handler(func):
        
        def parseMethod(self,method,parse=True):
            if method.startswith("@"):
                data = method[1:].split(".")
                widget = self._locals[data[0]]
            else:
                data = method.split(".")
                widget = getattr(self,data[0])
            
            for attr in data[1:-1]:
                widget = getattr(widget,attr)
            if parse:
                return getattr(widget,data[-1])
            else:
                return (widget,data[-1]) 


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

            # # NOTE 根据设置进行绑定
            # bindings = options.get("bindings",{})
            # for var,data in bindings.items():
            #     if type(data) == dict:
            #         for method,option in data.items():
            #             setter = parseMethod(self,method)
            #             self.__state_manager.bind(var,setter,option=option)
            #     elif type(data) == list or type(data) == tuple:
            #         for method in data:
            #             setter = parseMethod(self,method)
            #             self.__state_manager.bind(var,setter)

            methods = options.get("methods",{})
            for method,option in methods.items():
                option = {"action":option} if type(option) is str else option
                # NOTE 如果 option 非字符串和字典 报错
                if type(option) is not dict:
                    raise SchemeParseError("Invalid Scheme Args").parseErrorLine(method)

                widget,setter = parseMethod(self,method,False)
                ref = HOOKS.get(type(widget))
                # NOTE 过滤不在 HOOKS 里面的绑定 
                if ref is None or setter not in ref: continue
                hook = ref[setter]

                action = option.get("action")
                # NOTE 获取 updater
                updater = hook.get("updater")
                if updater is not None and type(updater) is str:
                    updater = getattr(widget,updater)
                    # NOTE 如果 callback 是字符串则获取 parent 的方法
                    var = None if type(action) is not str else None if action.startswith("$") else self.state._var_dict[action]
                    if var:
                        var.setUpdater([updater])

                # NOTE 获取 setter
                setter = hook.get("setter",setter)
                setter = getattr(widget,setter)
                typ = hook.get("type")
                # NOTE 默认自动将方法绑定到所有的 state setter 里面
                state_list = option.get("bindings",state)
                try:
                    if type(state_list) is str:
                        self.__state_manager.bind(state_list,setter,option=option,typ=typ)
                    else:
                        for var in state_list:
                            self.__state_manager.bind(var,setter,option=option,typ=typ)
                except AttributeError:
                    raise SchemeParseError("Unknown Action Attribute").parseErrorLine(method)

                    
            return res
        return wrapper
    return handler