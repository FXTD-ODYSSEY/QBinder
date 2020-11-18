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
    
class HandlerBase(object):
    pass

class Constructor(HandlerBase):
    def __init__(self,val):
        self.val = val

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