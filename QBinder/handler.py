# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-15 20:11:41'

import six
import inspect
from .binding import Binding
from .binder import Binder,BinderBase
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
            _binder = None
            for name,binder in binder_dict.items():
                _binder = Binder()
                for k,v in binder._var_dict_.items():
                    setattr(_binder,k,v)
                setattr(self,name,_binder)
            
            data = kwargs.pop('__data__',{})
            binder = binder_dict.get(kwargs.pop('__binder__','')) 
            binder = binder if binder else _binder

            res = func(self,*args, **kwargs)

            if binder:
                for k,v in data.items():
                    setattr(binder,k,v)
                    
        return wrapper

class ItemMixin(six.with_metaclass(ItemMeta)):
    
    __instance = None
    __instance_list = []
   
   
    def __new__(cls,*args,**kwargs):
        print('__new__',args,kwargs)
        data = kwargs.pop('__data__',[])
        layout = kwargs.pop('__layout__')
        if not layout:
            raise RuntimeError("need to pass __layout__ parameter to the ItemMixin")
        
        for i in range(len(cls.__instance_list),len(data)):
            super(ItemMixin, cls).__new__(cls)
        
        for item in data:
            pass
        
        if cls.__instance is None:
            cls.__instance = super(ItemMixin, cls).__new__(cls)
        return cls.__instance
    


class Set(object):
    
    def __init__(self,val):
        self.val = val
    
    def __rrshift__(self,binding):
        binding = Binding._inst_.pop()
        binding.set(self.val)
        return binding

        
class Anim(object):
    # TODO support anim value change
    def __init__(self,val):
        self.val = val
    
    def __rrshift__(self,binding):
        Binding._inst_
        return binding