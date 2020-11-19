# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-19 00:05:51'

import six
import inspect
from .binding import Binding
from .binder import Binder,BinderBase
from .util import ListGet
from Qt import QtCore,QtWidgets

class ItemMeta(type(QtCore.QObject)):
    def __new__(cls, name, bases, attrs):
        init = attrs.get('__init__')
        if init:
            binder_dict = {name:binder for name,binder in attrs.items() if isinstance(binder,BinderBase)}
            attrs['__init__'] = cls.init_deco(init,binder_dict)

        return super(ItemMeta,cls).__new__(cls,name,bases,attrs)

    @classmethod
    def init_deco(cls,func,binder_dict):
        @six.wraps(func)
        def wrapper(self,*args, **kwargs):
            # NOTE inject class binder to self binder
            cls = self.__class__
            name = ""
            for name,binder in binder_dict.items():
                _binder = Binder()
                for k,v in binder._var_dict_.items():
                    setattr(_binder,k,v)
                setattr(self,name,_binder)
            
            if not cls.__binder__:
                cls.__binder__ = name 
            
            # data = kwargs.pop('__data__',{})
            # cls_data = getattr(self.__class__,"__data__") if hasattr(self.__class__,"__data__") else None
            # data = data if data else cls_data if cls_data else {}
            
            # binder = binder_dict.get(kwargs.pop('__binder__',None)) 
            # cls_binder = getattr(self.__class__,"__binder__") if hasattr(self.__class__,"__binder__") else None
            # binder = binder if binder else cls_binder if cls_binder else _binder

            res = func(self,*args, **kwargs)

            # if binder:
            #     for k,v in data.items():
            #         setattr(binder,k,v)
        return wrapper
    
    def __rrshift__(self,data):
        self.__data__ = data
        return self
    
    def __rshift__(self,layout):
        # TODO reconstruct item not optimized
        for i,data in enumerate(self.__data__):
            widget = self.__items__ >> ListGet(i)
            if not widget:
                widget = self(*self.__args__)
                layout.addWidget(widget)
                self.__items__.append(widget)
                
            binder = getattr(widget,self.__binder__)
            for k,v in data.items():
                setattr(binder,k,v)
            
        for i in range(len(self.__data__),len(self.__items__)):
            widget = self.__items__ >> ListGet(i)
            widget.hide()
        # for todo in self.__data__:
        #     self()
        
        return self
    
    def __getitem__(self,binder):
        self.__binder__ = binder
        return self
    
    def __mod__(self,args):
        self.__args__ = args
        return self

class ItemMixin(six.with_metaclass(ItemMeta)):
    __binder__ = ""   
    __data__ = {}   
    __items__ = []   
    __args__ = ()   