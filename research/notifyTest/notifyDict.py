# coding:utf-8
from __future__ import print_function
__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-27 13:05:52'

import sys
from fnmatch import fnmatch as _fnmatch
class NotifyDict(dict):
    """
    https://stackoverflow.com/questions/5186520/python-property-change-listener-pattern
    """
    def __init__(self, val):
        dict.__init__(self,val)
    def _wrap(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            print("modify")
            return result
        return wrapper
    __delitem__ = _wrap(dict.__delitem__)
    __setitem__ = _wrap(dict.__setitem__)
    clear = _wrap(dict.clear)
    pop = _wrap(dict.pop)
    popitem = _wrap(dict.popitem)
    setdefault = _wrap(dict.setdefault)
    update =  _wrap(dict.update)


def main():
    a = NotifyDict({"a":"1"})
    a.update({1:"12"})
    print (a)

if __name__ == "__main__":
    main()