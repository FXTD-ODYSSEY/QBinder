# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-05 09:07:49'


class ListGet(object):
    """ListGet 
    safe get list index like dict.get
    https://stackoverflow.com/a/26849807
    
    >>> a = [1,2,3]
    >>> val = a >> ListGet(2)
    >>> print(val)
    3
    """
    
    def __init__(self,index, defualt=None):
        self.index = index
        self.defualt = defualt
    
    def __rrshift__(self, d):
        d = d if isinstance(d,list) else [d]
        return next(iter(d[self.index:]), self.defualt)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()