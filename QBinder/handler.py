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
from .binder import Binder
from Qt import QtWidgets

class ItemMeta(type):
    def __new__(cls, name, bases, attrs):
        print(name,bases,attrs)
        return super(ItemMeta,cls).__new__(cls,name,bases,attrs)

    
    def inject(binder):
        frame = inspect.currentframe().f_back
        for name,v in frame.f_locals.items():
            if v is binder:
                break
        def caller(func):
            @wraps(func)
            def wrapper(self,*args, **kwargs):
                # NOTE inject class binder to self binder
                _binder = Binder()
                for k,v in binder._var_dict_.items():
                    setattr(_binder,k,v)
                setattr(self,name,_binder)
                res = func(self,*args, **kwargs)
                
                return res
            return wrapper
        return caller
    
# NOTE fix metalclass conflict
class ItemMixMeta(ItemMeta,type(QtWidgets.QWidget)):
    pass

class ItemMixin(object,six.with_metaclass(ItemMixMeta)):
    
    __instance = None

    # def __new__(cls):
    #     if cls.__instance is None:
    #         cls.__instance = super(ItemMixin, cls).__new__(cls)
    #     return cls.__instance


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