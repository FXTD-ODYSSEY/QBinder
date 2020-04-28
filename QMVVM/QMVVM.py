# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 14:44:34'

"""

"""

import re
import sys
import inspect

from functools import wraps
from functools import partial
from Qt import QtCore
from .hook import HOOKS
from .exception import SchemeParseError
from collections import OrderedDict

def notify(func):
    def wrapper(self,*args,**kwargs):
        # NOTE 更新数据
        res = func(self,*args,**kwargs)
        # NOTE 更新组件数据
        if hasattr(self,"STATE"):
            getattr(self.STATE.widget.state,"_%s_signal" % self.STATE.var).emit()
        return res
    return wrapper

class NotifyList(list):
    """
    https://stackoverflow.com/questions/13259179/list-callbacks
    监听数组的内置函数更新组件数据
    """
    def __init__(self,val,STATE):
        super(NotifyList, self).__init__(val)
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
        if isinstance(value, dict):
            value = NotifyDict(value,self.STATE)
        elif isinstance(value, list):
            value = NotifyList(value,self.STATE)
        list.__setitem__(self,key,value)
        
class NotifyDict(OrderedDict):
    """
    https://stackoverflow.com/questions/5186520/python-property-change-listener-pattern
    """
    def __init__(self,val,STATE):
        super(NotifyDict, self).__init__(val)
        self.STATE = STATE

    clear = notify(OrderedDict.clear)
    pop = notify(OrderedDict.pop)
    popitem = notify(OrderedDict.popitem)
    setdefault = notify(OrderedDict.setdefault)
    update =  notify(OrderedDict.update)
    __delitem__ = notify(OrderedDict.__delitem__)

    @notify
    def __setitem__(self,key,value):
        if hasattr(self,"STATE"):
            if isinstance(value, dict):
                value = NotifyDict(value,self.STATE)
            elif isinstance(value, list):
                value = NotifyList(value,self.STATE)
        return OrderedDict.__setitem__(self,key,value)
    

class State(object):

    def __init__(self,var,widget,val):
        super(State,self).__init__()
        self.var = var
        self.widget = widget
        self.val = self.retrieve2Notify(val)

    def __get__(self, instance, owner):
        return self.val().get("default") if callable(self.val) else self.val

    def __set__(self,instance, value):
        self.val = self.retrieve2Notify(value)
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def setVal(self,value):
        self.val = self.retrieve2Notify(value)
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def retrieve2Notify(self,val,initialize=True):
        """
        遍历所有字典和数组对象，转换为 Notify 对象
        """
        itr = val.items() if type(val) is dict else enumerate(val) if type(val) is list else []
        for k,v in itr:        
            if isinstance(v, dict):
                self.retrieve2Notify(v,initialize=False)
                val[k] = NotifyDict(v,self)
            elif isinstance(v, list):            
                self.retrieve2Notify(v,initialize=False)
                val[k] = NotifyList(v,self)
        
        if initialize:
            if isinstance(val, dict):
                return NotifyDict(val,self)
            elif isinstance(val, list):
                return NotifyList(val,self)
            else:
                return val

class StateManager(object):
    
    def __init__(self,parent):
        self.parent = parent

    def add(self,options):
        
        manager = self
        container_list = {}
        state_list = {}
        # for var,val in options["state"].items():
        #     if type(val) is list or type(val) is dict:
        #         container_list[var] = val 
        #     else:
        #         state_list[var] = val 
                
        # NOTE 获取可用的 descriptor 
        class StateDescriptor(QtCore.QObject):
            
            __signal_dict = {}
            _var_dict = {}
            for var,val in options["state"].items():
                __signal_dict["_%s_signal" % var] = QtCore.Signal()
                _var_dict[var] = State(var,manager.parent,val)

            # TODO handle container state injection 

            locals().update(__signal_dict)
            locals().update(_var_dict)

        self.parent.state = StateDescriptor()
    
    def bind(self,var,method,option=None,typ=None):
        setter = lambda:self.setSignal(var,method,option,typ)
        setter()
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
        if type(callback) is str and callback.startswith("`") and callback.endswith("`"):
            def callbackHandler(m):
                # NOTE remove ${ } pattern
                match = m.group()[2:-1].strip()
                if re.match(r"^\$[0-9]+",match):
                    return re.sub(r"^\$[0-9]+",lambda m: "{%s}" % m.group()[1:],match)
                var = getattr(self.parent,match[1:]) if match.startswith("$") else getattr(self.parent.state,match)
                return str(var)
            res_str = re.sub(r"\$\{(\S*?)\}",callbackHandler,callback[1:-1])
            callback = lambda *args:res_str.format(*args)

        callback = callback if type(callback) is not str else getattr(self.parent,callback[1:]) if callback.startswith("$") else getattr(self.parent.state,callback)
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

            methods = options.get("methods",{})
            for method,option in methods.items():
                option = {"action":option} if type(option) is str else option
                if type(option) is not dict:
                    raise SchemeParseError("Invalid Scheme Args").parseErrorLine(method)
                
                widget,setter = parseMethod(self,method,False)
                ref = HOOKS.get(type(widget))
                if ref is None:
                    for widget_type,ref in HOOKS.items():
                        if isinstance(widget_type,widget):
                            break
                    else:
                        continue
                hook = ref.get(setter)

                action = option.get("action")

                signals = option.get("signals")
                signals = [signals] if type(signals) is str else signals
                # NOTE get hook.py config as default signals
                if signals is None:
                    signals = hook.get("signals",[])
                    signals = [signals] if type(signals) is str else signals

                # NOTE 获取 updater
                updaters = option.get("updaters",{})
                default_updater = None if type(action) is not str else None if action.startswith("$") or action.startswith("`") else self.state._var_dict[action].setVal
                updaters.setdefault("default",updaters if type(updaters) is str else default_updater)

                for i,signal in enumerate(signals):
                    updater = updaters.get(signal,updaters.get("default"))
                    if not updater: continue
                    updater = updater if callable(updater) else getattr(self,updater[1:]) if updater.startswith("$") else getattr(self,updater)
                    signal = getattr(widget,signal)
                    signal.connect(updater)
                    
                setter = hook.get("setter",setter)
                setter = getattr(widget,setter)
                typ = hook.get("type")
                state_list = option.get("bindings",state)
                try:
                    if type(state_list) is str:
                        self.__state_manager.bind(state_list,setter,option=option,typ=typ)
                    else:
                        # NOTE 默认自动将方法绑定到所有的 state 里面
                        for var in state_list:
                            self.__state_manager.bind(var,setter,option=option,typ=typ)
                except AttributeError as err:
                    raise SchemeParseError().parseErrorLine(method,err)

            signals = options.get("signals",{})
            try:
                for signal,attrs in signals.items():
                    attrs = [attrs] if type(attrs) is str else attrs
                    widget,_signal = parseMethod(self,signal,False)
                    _signal = getattr(widget,_signal)
                    for attr in attrs:
                        _signal.connect(partial(getattr(self,attr[1:]),widget) if attr.startswith("$") else self.state._var_dict[attr].setVal)
            except AttributeError as err:
                raise SchemeParseError().parseErrorLine(signal,err)
                        
            return res
        return wrapper
    return handler