# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-15 20:11:41'

from functools import partial

from .binding import Binding
from .util import ListGet
from Qt import QtWidgets

class HandlerBase(object):
    pass

class ItemConstructor(HandlerBase):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs

    def __rrshift__(self,item):
        
        __filter__ = []
        data = self.kwargs.pop('__data__',item.__data__)
        # NOTE trace lamda function 
        if callable(data):
            with Binding.set_trace():
                data = data()
            for binding in Binding._trace_list_:
                val = binding.val
                if not isinstance(val,list):
                    continue
                item.__data__ = val
                compare = {id(d):i for i,d in enumerate(item.__data__)}
                __filter__ = [compare.get(id(d),-1) for d in data]
                break
        else:
            item.__data__ = data
            __filter__ = [i for i in range(len(data))]
        
        item.__layout__ = self.kwargs.pop('__layout__',item.__layout__)
        item.__binder__ = self.kwargs.pop('__binder__',item.__binder__) 
  
        for i,data in enumerate(item.__data__):
            widget = item.__items__ >> ListGet(i)
            if not widget:
                widget = item(*self.args,**self.kwargs)
                item.__layout__.addWidget(widget)
                item.__items__.append(widget)
                widget.__index__ = i

            widget.setVisible(i in __filter__)
            
            if hasattr(widget,item.__binder__):
                binder = getattr(widget,item.__binder__)
                for k,v in data.items():
                    val = getattr(binder,k)
                    if val != v:
                        setattr(binder,k,v)
        
        for i in range(len(item.__data__),len(item.__items__)):
            widget = item.__items__[i]
            widget.deleteLater()
        item.__items__ = item.__items__[:len(item.__data__)]

class GroupBoxBind(HandlerBase):
    def __init__(self, group):
        self.group = group        

    def __rrshift__(self,binding):
        self.binding = Binding._inst_.pop()
        for rb in self.group.findChildren(QtWidgets.QRadioButton):
            rb.toggled.connect(partial(self.filter_state,rb))
        self.binding.connect(self.check_state) >> Call()
        
        return self.binding

    def filter_state(self, rb,state):
        if state:
            self.binding.set(rb.text().strip())
            
    def check_state(self):
        for rb in self.group.findChildren(QtWidgets.QRadioButton):
            if rb.text().strip() == self.binding.val:
                rb.setChecked(True)

class Call(HandlerBase):  
    
    def __init__(self, *args, **kwargs):
        self.args = args        
        self.kwargs = kwargs        
    
    def __rrshift__(self,func):
        return func(*self.args, **self.kwargs)

class Set(HandlerBase):
    
    def __init__(self,val):
        self.val = val
    
    def __rrshift__(self,binding):
        binding = Binding._inst_.pop()
        binding.set(self.val)
        return binding

        
class Anim(HandlerBase):
    # TODO support anim value change
    def __init__(self,val):
        self.val = val
    
    def __rrshift__(self,binding):
        Binding._inst_
        return binding