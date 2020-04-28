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
from .type import NotifyList,NotifyDict,BaseState

class State(object):
    __repr__ = lambda self: self.val.__repr__()
    # __str__ = lambda self:self.val.__str__(),
    
    operator_list = {
        "__add__"      : lambda self,x:self.val.__add__(x),
        "__sub__"      : lambda self,x:self.val.__sub__(x),
        "__mul__"      : lambda self,x:self.val.__mul__(x),
        "__floordiv__" : lambda self,x:self.val.__floordiv__(x),
        "__truediv__"  : lambda self,x:self.val.__truediv__(x),
        "__mod__"      : lambda self,x:self.val.__mod__(x),
        "__pow__"      : lambda self,x:self.val.__pow__(x),
        "__lshift__"   : lambda self,x:self.val.__lshift__(x),
        "__rshift__"   : lambda self,x:self.val.__rshift__(x),
        "__and__"      : lambda self,x:self.val.__and__(x),
        "__xor__"      : lambda self,x:self.val.__xor__(x),
        "__or__"       : lambda self,x:self.val.__or__(x),

        "__iadd__"      : lambda self,x:self.val.__iadd__(x),
        "__isub__"      : lambda self,x:self.val.__isub__(x),
        "__imul__"      : lambda self,x:self.val.__imul__(x),
        "__idiv__"      : lambda self,x:self.val.__idiv__(x),
        "__ifloordiv__" : lambda self,x:self.val.__ifloordiv__(x),
        "__imod__"      : lambda self,x:self.val.__imod__(x),
        "__ipow__"      : lambda self,x:self.val.__ipow__(x),
        "__ilshift__"   : lambda self,x:self.val.__ilshift__(x),
        "__irshift__"   : lambda self,x:self.val.__irshift__(x),
        "__iand__"      : lambda self,x:self.val.__iand__(x),
        "__ixor__"      : lambda self,x:self.val.__ixor__(x),
        "__ior__"       : lambda self,x:self.val.__ior__(x),
        
        "__neg__"     : lambda self,x:self.val.__neg__(x),
        "__pos__"     : lambda self,x:self.val.__pos__(x),
        "__abs__"     : lambda self,x:self.val.__abs__(x),
        "__invert__"  : lambda self,x:self.val.__invert__(x),
        "__complex__" : lambda self,x:self.val.__complex__(x),
        "__int__"     : lambda self,x:self.val.__int__(x),
        "__long__"    : lambda self,x:self.val.__long__(x),
        "__float__"   : lambda self,x:self.val.__float__(x),
        "__oct__"     : lambda self,x:self.val.__oct__(x),
        "__hex__"     : lambda self,x:self.val.__hex__(x),
        
        "__lt__" : lambda self,x:self.val.__lt__(x),
        "__le__" : lambda self,x:self.val.__le__(x),
        "__eq__" : lambda self,x:self.val.__eq__(x),
        "__ne__" : lambda self,x:self.val.__ne__(x),
        "__ge__" : lambda self,x:self.val.__ge__(x),
        "__gt__" : lambda self,x:self.val.__gt__(x),
    }
    def __init__(self,var,widget,val,writable=True):
        super(State,self).__init__()
        self.var = var
        self.widget = widget
        self.val = self.retrieve2Notify(val)
        self.writable = writable
        self.overrideInit(val)

    def __get__(self, instance, owner):
        return self.val() if callable(self.val) else self.val

    def __set__(self,instance, value):
        self.val = self.retrieve2Notify(value)
        self.sync()
        self.overrideInit(value)
    
    def overrideInit(self,val):
        """ sync the val operator and method """
        self.overrideOperator(val)
        self.overrideDataHandler(val)

    @classmethod
    def overrideOperator(cls,val):
        for attr in dir(val):
            func = cls.operator_list.get(attr)
            if func is not None:
                setattr(cls,attr,func)
    
    def overrideDataHandler(self,val):
        for attr in dir(val):
            if not attr.startswith("_"):
                setattr(self,attr,getattr(self.val,attr))

    def sync(self):
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def setVal(self,value):
        self.val = self.retrieve2Notify(value)
        self.sync()

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
                
        # NOTE 获取可用的 descriptor 
        class StateDescriptor(QtCore.QObject):
            
            __signal_dict = {}
            _var_dict = {}
            
            for var,val in options.get("state",{}).items():
                __signal_dict["_%s_signal" % var] = QtCore.Signal()
                _var_dict[var] = State(var,manager.parent,val)

            locals().update(__signal_dict)
            locals().update(_var_dict)

            # # TODO handle container state injection 
            # for var,element_list in options.get("computed",{}).items():
            #     __signal_dict["_%s_signal" % var] = QtCore.Signal()
            #     def temp(var,element_list,_var_dict,*args):
            #         print var,locals().get(var)
            #         if hasattr(self,var):
            #             print "TEMP",getattr(self,var)
            #         if isinstance(element_list,list):
            #             res_list = []
            #             for element in element_list:
            #                 element = self.parseFromatString(element,_var_dict)
            #                 element = element() if callable(element) else element
            #                 res_list.append(element)
            #             return res_list
            #         elif isinstance(element_list,dict):
            #             res_dict = {} if type(element_list) is dict else OrderedDict() 
            #             for key,val in element_list.items():
            #                 key = self.parseFromatString(key,_var_dict)
            #                 key = key() if callable(key) else key
            #                 val = self.parseFromatString(val,_var_dict)
            #                 val = val() if callable(val) else val
            #                 res_dict[key] = val
            #             return res_dict

            #     _var_dict[var] = property(partial(temp,var,element_list,_var_dict))
            
            # locals().update(__signal_dict)
            # locals().update(_var_dict)

        self.parent.state = StateDescriptor()
    
    def bind(self,var,method,option=None,typ=None):
        setter = lambda:self.setSignal(var,method,option,typ)
        setter()
        getattr(self.parent.state,"_%s_signal" % var).connect(setter)

    def parseFromatString(self,callback):
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
        return callback
        
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
        callback = self.parseFromatString(callback)
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


def elapsedTime(func):
    def wrapper(*args, **kwargs):
        import time
        elapsed = time.time()
        res = func(*args, **kwargs)
        print "elpased time :",time.time() - elapsed
        return res
    return wrapper

@elapsedTime
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