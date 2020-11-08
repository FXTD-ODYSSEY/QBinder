# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-07 22:26:11'

# class Property(object):
#     def __init__(self,val,fset=None,fget=None):
#         self.fset = fset
#         self.fget = fget
#         self.__val__ = val

#     def __set__(self,instance,val):
#         print('__set__')
#         self.__val__ = val
#         self.fset(val) if callable(self.fset) else None

#     def __get__(self,instance,owner):
#         print('__get__')
#         self.fget() if callable(self.fget) else None
#         return self.__val__

# class PropertyContainer(object):
#     SHOW_INFO_PANEL = Property(False)

# container = PropertyContainer()
# SHOW_INFO_PANEL = container.SHOW_INFO_PANEL
# print(container.SHOW_INFO_PANEL)
# container.SHOW_INFO_PANEL = True
# SHOW_INFO_PANEL = True


AUTO_LOAD_CONFIG = True


