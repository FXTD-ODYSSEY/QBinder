# -*- coding: utf-8 -*-
"""
https://www.cnblogs.com/PyKK2019/p/11059444.html
https://blog.csdn.net/qq_41359051/article/details/86764867
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-24 23:52:18'

import abc

class Base(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def my_protocol(self):
        """自定义协议"""

    @classmethod
    def __subclasshook__(cls, subclass):
        print("subclass",subclass)
        # if cls is Base:
        #     print(subclass)
            # if any("my_protocol" in B.__dict__ for B in subclass):
            #     return True

        return NotImplemented
    
#并没有显式继承Base
class MyClass:
    def my_protocol(self):
        pass

class Test:
    def my_protocol(self):
        pass

if __name__ == '__main__':
    k = MyClass()
    b = Test()
    print(isinstance(k, Base))  
    #True
    # print(issubclass(MyClass, Base))
    #True
    # print(Base._abc_impl)
    