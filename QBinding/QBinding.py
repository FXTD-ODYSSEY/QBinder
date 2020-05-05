# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 14:44:34'

"""

"""

import re
import sys
import ast
import six
import json
import inspect

from functools import partial
from collections import OrderedDict
from textwrap import dedent
# from collections.abc import Iterable
from Qt import QtCore,QtWidgets,QtGui
from .hook import HOOKS
from .exception import SchemeParseError
from .type import NotifyList,NotifyDict

class State(QtGui.QStandardItem):
    # __repr__ = lambda self: "State(%s)" % self.val.__repr__()
    __repr__ = lambda self: self.val.__repr__()
    # __str__ = lambda self:self.val.__str__(),
    
    operator_list = {
        "__add__"       : lambda self,x:self.val.__add__(x),
        "__sub__"       : lambda self,x:self.val.__sub__(x),
        "__mul__"       : lambda self,x:self.val.__mul__(x),
        "__floordiv__"  : lambda self,x:self.val.__floordiv__(x),
        "__truediv__"   : lambda self,x:self.val.__truediv__(x),
        "__mod__"       : lambda self,x:self.val.__mod__(x),
        "__pow__"       : lambda self,x:self.val.__pow__(x),
        "__lshift__"    : lambda self,x:self.val.__lshift__(x),
        "__rshift__"    : lambda self,x:self.val.__rshift__(x),
        "__and__"       : lambda self,x:self.val.__and__(x),
        "__xor__"       : lambda self,x:self.val.__xor__(x),
        "__or__"        : lambda self,x:self.val.__or__(x),

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
        
        "__neg__"       : lambda self,x:self.val.__neg__(x),
        "__pos__"       : lambda self,x:self.val.__pos__(x),
        "__abs__"       : lambda self,x:self.val.__abs__(x),
        "__invert__"    : lambda self,x:self.val.__invert__(x),
        "__complex__"   : lambda self,x:self.val.__complex__(x),
        "__int__"       : lambda self,x:self.val.__int__(x),
        "__long__"      : lambda self,x:self.val.__long__(x),
        "__float__"     : lambda self,x:self.val.__float__(x),
        "__oct__"       : lambda self,x:self.val.__oct__(x),
        "__hex__"       : lambda self,x:self.val.__hex__(x),
        
        "__lt__"        : lambda self,x:self.val.__lt__(x),
        "__le__"        : lambda self,x:self.val.__le__(x),
        "__eq__"        : lambda self,x:self.val.__eq__(x),
        "__ne__"        : lambda self,x:self.val.__ne__(x),
        "__ge__"        : lambda self,x:self.val.__ge__(x),
        "__gt__"        : lambda self,x:self.val.__gt__(x),
    }
    def __init__(self,val = None):
        super(State,self).__init__()
        self.val = self.retrieve2Notify(val)
        self.val_type = six.string_types if isinstance(self.val,six.string_types) else type(self.val).__base__
        self.__override_attr_list = []
        self.overrideMethod(val)

    def __get__(self, instance, owner):
        return self.val() if callable(self.val) else self.val

    def __set__(self, instance, value):
        self.setVal(value)

    def setVal(self,value):
        if not isinstance(value,self.val_type):
            QtWidgets.QMessageBox.warning(QtWidgets.QApplication.activeWindow(),"warning","dynamic change state type not support")
            return
        self.val = self.retrieve2Notify(value)
        self.overrideMethod(value)
        self.emitDataChanged()

    def overrideMethod(self,val):
        """ sync the val operator and method """
        [delattr(self,attr) for attr in self.__override_attr_list if hasattr(self,attr)]
        self.__override_attr_list = [attr for attr in dir(val) if not attr.startswith("_")]
        for attr in self.__override_attr_list:
            setattr(self,attr,getattr(self.val,attr))
        self.overrideOperator(val)

    @classmethod
    def overrideOperator(cls,val):
        for attr in dir(val):
            func = cls.operator_list.get(attr)
            if func is not None:
                setattr(cls,attr,func)

    def retrieve2Notify(self,val,initialize=True):
        """ convert to Notify type """
        itr = six.iteritems(val) if type(val) is dict else enumerate(val) if type(val) is list else []
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
    
    def data(self,role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return str(self.val)

    def setData(self,value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.setVal(value)
            return True            
        return False   


# NOTE initialize the Qt Widget setter 
def StateHandler(func,options=None):
    options = options if options is not None else {}
    typ = options.get("type")
    signals = options.get("signals",[])
    signals = [signals] if isinstance(signals,six.string_types) else signals
    def wrapper(self,value,*args, **kwargs):
        if callable(value):
            self.STATE_DICT = {} if not hasattr(self,"STATE_DICT") else self.STATE_DICT
            self.STATE_DICT.setdefault(self.STATE,{})
            callback = self.STATE_DICT.get(self.STATE).get(func)
            self.STATE._model.itemChanged.disconnect(callback) if callback else None
            
            callback = partial(lambda value,state:(func(self,typ(value()) if typ else value(),*args, **kwargs)),value)
            self.STATE_DICT[self.STATE][func] = callback
            self.STATE._model.itemChanged.connect(callback)

            value = value()

        value = typ(value) if typ else value
        res = func(self,value,*args,**kwargs)
        return res
    return wrapper

for widget,setters in HOOKS.items():
    for setter,options in setters.items():
        setattr(widget,setter,StateHandler(getattr(widget,setter),options))
        # setattr(QtWidgets.QCheckBox,"setText",StateHandler(QtWidgets.QCheckBox.setText))

def elapsedTime(func):
    def wrapper(*args, **kwargs):
        import time
        elapsed = time.time()
        res = func(*args, **kwargs)
        print("elpased time :",time.time() - elapsed)
        return res
    return wrapper

@elapsedTime
def store(options):
    def handler(func):
        
        def parseMethod(self,method,parse=True):
            if method.startswith("@"):
                data = method.split(".")
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

        def cursorPositionFix(func,widget):
            '''fix the cusorPosition after setting the value'''
            def wrapper(*args,**kwargs):
                pos = widget.property("cursorPosition")
                res = func(*args,**kwargs)
                widget.setProperty("cursorPosition",pos) if pos else None
                return res
            return wrapper
            
        @six.wraps(func)
        def wrapper(self,*args, **kwargs):
            # NOTE Dynamic Create State Descriptor 
            class StateDescriptor(QtCore.QObject):
                
                _var_dict = {}
                
                for var,val in six.iteritems(options.get("state",{})):
                    _var_dict[var] = State(val)

                locals().update(_var_dict)
                
                _model = QtGui.QStandardItemModel()
                _model.appendRow(_var_dict.values())

                _options = options
                
                def __init__(self):
                    super(StateDescriptor, self).__init__()
                    for widget in HOOKS:
                        setattr(widget,"STATE",self)

            self.state = StateDescriptor()
            
            # NOTE 获取函数中的 locals 变量 https://stackoverflow.com/questions/9186395
            self._locals = {}
            sys.setprofile(lambda f,e,a: self._locals.update({ "@%s" % k : v for k,v in six.iteritems(f.f_locals)}) if e=='return' else None)
            res = func(self,*args, **kwargs)
            sys.setprofile(None)

            state = options.get("state",{})

            methods = options.get("methods",{})
            for method,option in six.iteritems(methods):
                option = {"action":option} if isinstance(option, six.string_types) else option
                if type(option) is not dict:
                    raise SchemeParseError("Invalid Scheme Args").parseErrorLine(method)
                
                widget,setter = parseMethod(self,method,False)
                ref = HOOKS.get(type(widget))
                if ref is None:
                    for widget_type,ref in six.iteritems(HOOKS):
                        if isinstance(widget_type,widget):
                            break
                    else:
                        continue
                hook = ref.get(setter)

                action = option.get("action")

                signals = option.get("signals")
                signals = [signals] if isinstance(signals, six.string_types) else signals
                # NOTE get hook.py config as default signals
                if signals is None:
                    signals = hook.get("signals",[])
                    signals = [signals] if isinstance(signals, six.string_types) else signals

                # NOTE 获取 updater
                updaters = option.get("updaters",{})
                default_updater = None if type(action) is not str else None if action.startswith("$") or action.startswith("`") else self.state._var_dict[action].setVal
                updaters.setdefault("default",updaters if isinstance(updaters, six.string_types) else default_updater)

                for i,signal in enumerate(signals):
                    updater = updaters.get(signal,updaters.get("default"))
                    if not updater: continue
                    updater = updater if six.callable(updater) else getattr(self,updater[1:]) if updater.startswith("$") else getattr(self,updater)
                    signal = getattr(widget,signal)
                    signal.connect(updater)
                    
                setter = hook.get("setter",setter)
                setter = getattr(widget,setter)
                typ = hook.get("type")
                state_list = option.get("bindings",state)
                try:
                    if isinstance(state_list, six.string_types):
                        self.__state_manager.bind(state_list,widget,setter,option=option,typ=typ)
                    else:
                        # NOTE 默认自动将方法绑定到所有的 state 里面
                        for var in state_list:
                            self.__state_manager.bind(var,widget,setter,option=option,typ=typ)
                except AttributeError as err:
                    raise SchemeParseError().parseErrorLine(method,err)

            signals = options.get("signals",{})
            for signal,attrs in six.iteritems(signals):
                try:
                    attrs = attrs if isinstance(attrs, list) else [attrs]
                    widget,_signal = parseMethod(self,signal,False)
                    _signal = getattr(widget,_signal)
                    for attr in attrs:
                        _signal.connect(partial(attr,self,widget) if six.callable(attr) else partial(getattr(self,attr[1:]),widget) 
                                        if attr.startswith("$") else cursorPositionFix(self.state._var_dict[attr].setVal,widget))
                except AttributeError as err:
                    raise SchemeParseError().parseErrorLine(signal,err)
            
            # # TODO read the dynamic Property 
            # self._locals.update({attr:getattr(self,attr)  for attr in dir(self)})
            # for name,widget in six.iteritems(self._locals):
            #     if not isinstance(widget,QtWidgets.QWidget): continue
            #     config = widget.property("QBinding")
            #     # print (widget.dynamicPropertyNames())
            #     # print (type(config),config)
            #     if not config: continue
            #     # config = ast.literal_eval(dedent(config))
            #     config = json.loads(config,encoding="utf-8")
            #     # print (type(config),config)
            #     # print ("asd")

                        
            return res
        return wrapper
    return handler