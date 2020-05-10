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
from Qt import QtCore,QtWidgets,QtGui
from .hook import HOOKS
from .exception import SchemeParseError
from .type import StateProxyModel,State



def StateHandler(func,options=None):
    """
    # NOTE initialize the Qt Widget setter 
    """
    options = options if options is not None else {}
    typ = options.get("type")
    signals = options.get("signals",[])
    signals = [signals] if isinstance(signals,six.string_types) else signals
    def wrapper(self,value,*args, **kwargs):
        if callable(value):
            self.STATE_DICT = {} if not hasattr(self,"STATE_DICT") else self.STATE_DICT
            self.STATE_DICT.setdefault(self.STATE,{})
            callback = self.STATE_DICT.get(self.STATE).get(func)
            # NOTE clear old callback
            self.STATE._model.itemChanged.disconnect(callback) if callback else None
            
            callback = partial(lambda value,state:(func(self,typ(value()) if typ else value(),*args, **kwargs)),value)
            self.STATE_DICT[self.STATE][func] = callback
            self.STATE._model.itemChanged.connect(callback)

            value = value()
            value = typ(value) if typ else value

        res = func(self,value,*args,**kwargs)
        return res
    return wrapper

global default_hook_dict
default_hook_dict = {}
def hookInitialize():
    """
    # NOTE Dynamic wrap the Qt Widget setter base on the HOOKS Definition
    """
    global default_hook_dict
    for widget,(setter,func) in default_hook_dict.items():
        setattr(widget,setter,func)

    for widget,setters in HOOKS.items():
        for setter,options in setters.items():
            default_hook_dict[widget] = (setter,getattr(widget,setter))
            setattr(widget,setter,StateHandler(getattr(widget,setter),options))
            # NOTE example code -> setattr(QtWidgets.QCheckBox,"setText",StateHandler(QtWidgets.QCheckBox.setText))

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
        
        def parseStateVarString(element,var_dict):
            if not isinstance(element, six.string_types):
                return element
            var_dict = var_dict if isinstance(var_dict, dict) else {}
            pattern = r"""
                %(delim)s(?:
                (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
                (?P<named>%(id)s)      |   # delimiter and a Python identifier
                {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier
                (?P<invalid>)              # Other ill-formed delimiter exprs
                )
            """ % {"delim" : re.escape('$'), "id" : r'[_a-z][_a-z0-9]*'}
            pattern = re.compile(pattern, re.IGNORECASE | re.VERBOSE)
            
            for _,named,braced,_ in pattern.findall(element):
                target = named.strip() or braced.strip()
                _element = var_dict.get(target)
                if _element is None:
                    raise SchemeParseError("Computed State Unknown -> %s" % element)
                return _element
            return element
        
        def retrieveHandleStateVar(val,var_dict=None,initialize=True):
            itr = six.iteritems(val) if isinstance(val,dict) else enumerate(val) if isinstance(val,list) else []
            for k,v in itr:
                if isinstance(v, dict):
                    retrieveHandleStateVar(v,var_dict,initialize=False)
                    val[k] = v
                elif isinstance(v, list):
                    retrieveHandleStateVar(v,var_dict,initialize=False)
                    val[k] = v
                elif isinstance(v,six.string_types):
                    val[k] = parseStateVarString(v,var_dict)
            
            if initialize:
                return val
                    
        @six.wraps(func)
        def wrapper(self,*args, **kwargs):
            # NOTE Dynamic Create State Descriptor 
            class StateDescriptor(QtCore.QObject):
                
                _var_dict = {}
                
                for var,val in six.iteritems(options.get("state",{})):
                    _var_dict[var] = State(val)

                locals().update(_var_dict)

                _model = QtGui.QStandardItemModel()
                _model.appendColumn(_var_dict.values())

                for var,element_list in six.iteritems(options.get("computed",{})):
                    res = retrieveHandleStateVar(element_list,locals())
                    # NOTE model handle
                    if var.startswith("*"):
                        var = var[1:]
                        item_list = [item for item in res]
                        _var_dict[var] = StateProxyModel(item_list)
                    else:
                        _var_dict["__computed_%s" % var] = res
                        _var_dict[var] = property(partial(lambda var,self:getattr(self,"__computed_%s" % var),var))
                        
                locals().update(_var_dict)

                OPTIONS = options
                
                def __init__(self):
                    super(StateDescriptor, self).__init__()
                    # NOTE register to all the hook Qt Widget
                    for widget in HOOKS:
                        setattr(widget,"STATE",self)
                
                def __getitem__(self,key):
                    return self._var_dict[key]

                def __setitem__(self,key,val):
                    self._var_dict[key].set(val)
                
                def toJson(self):
                    # data = json.dumps({k:v.val if isinstance(v,State) else v.getter(self) if type(v) is property else v for k,v in self._var_dict.items()})
                    data = {k:v.get() if isinstance(v,State) or isinstance(v,StateProxyModel) else getattr(self,k) if type(v) is property else v for k,v in self._var_dict.items() if not k.startswith("__computed_")}
                    return json.dumps(ast.literal_eval(str(data)))

            self.state = StateDescriptor()
            
            # NOTE 获取函数中的 locals 变量 https://stackoverflow.com/questions/9186395
            self._locals = {}
            sys.setprofile(lambda f,e,a: self._locals.update({ "@%s" % k : v for k,v in six.iteritems(f.f_locals)}) if e=='return' else None)
            res = func(self,*args, **kwargs)
            sys.setprofile(None)

            signals = self.state.OPTIONS.get("signals",{})
            for signal,attrs in six.iteritems(signals):
                try:
                    attrs = attrs if isinstance(attrs, list) else [attrs]
                    widget,_signal = parseMethod(self,signal,False)
                    _signal = getattr(widget,_signal)
                    for attr in attrs:
                        _signal.connect(partial(attr,self,widget) if six.callable(attr) else cursorPositionFix(self.state._var_dict[attr[1:]].set,widget) if attr.startswith("$") else partial(getattr(self,attr),widget))
                except AttributeError as err:
                    raise SchemeParseError().parseErrorLine(signal,err)
            
            
            return res
        return wrapper
    return handler