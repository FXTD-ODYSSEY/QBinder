# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-15 20:11:41'


from .binding import Binding
from .util import ListGet
    
class HandlerBase(object):
    pass

class ItemConstructor(HandlerBase):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs

    def __rrshift__(self,item):
        
        item.__data__ = self.kwargs.pop('__data__',item.__data__)
        item.__layout__ = self.kwargs.pop('__layout__',item.__layout__)
        item.__binder__ = self.kwargs.pop('__binder__',item.__binder__) 
        
        # TODO reconstruct setattr trigger multiple time 
        for i,data in enumerate(item.__data__):
            widget = item.__items__ >> ListGet(i)
            if not widget:
                widget = item(*self.args,**self.kwargs)
                item.__layout__.addWidget(widget)
                item.__items__.append(widget)
            else:
                widget.show() if not widget.isVisible() else None
            
            widget.__index__ = i
            if hasattr(widget,item.__binder__):
                binder = getattr(widget,item.__binder__)
                for k,v in data.items():
                    val = getattr(binder,k)
                    if val != v:
                        setattr(binder,k,v)
            
        for i in range(len(item.__data__),len(item.__items__)):
            widget = item.__items__ >> ListGet(i)
            widget.hide() if widget.isVisible() else None
        
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