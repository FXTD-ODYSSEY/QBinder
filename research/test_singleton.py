# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-10-30 19:42:26'

import inspect
import threading


class TwoWayDict(dict):

    """
    A dictionary that can also map in reverse: value to key.

    >>> twd = TwoWayDict( {3:'foobar'} )
    >>> twd[3]
    'foobar'
    >>> twd.get_key('foobar')
    3

    Entries in both sets (keys and values) must be unique within that set, but
    not necessarily across the two sets - ie, you may have 12 as both a key and
    a value, but you may not have two keys which both map to 12 (or, as with a
    regular dict, two key entries for 12).

    If a key is updated to a new value, get_key for the old value will raise
    a KeyError:

    >>> twd = TwoWayDict( {3:'old'} )
    >>> twd[3] = 'new'
    >>> twd[3]
    'new'
    >>> twd.get_key('new')
    3
    >>> twd.get_key('old')
    Traceback (most recent call last):
        ...
    KeyError: 'old'

    Similarly, if a key is updated to an already-existing value, then the old key
    will be removed from the dictionary!

    >>> twd = TwoWayDict( {'oldKey':'aValue'} )
    >>> twd['newKey'] = 'aValue'
    >>> twd['newKey']
    'aValue'
    >>> twd.get_key('aValue')
    'newKey'
    >>> twd['oldKey']
    Traceback (most recent call last):
        ...
    KeyError: 'oldKey'

    If a group of values is fed to the TwoWayDict (either on initialization, or
    through 'update', etc) that is not consistent with these conditions, then the
    resulting dictionary is indeterminate; however, it is guaranteed to be a valid/
    uncorrupted TwoWayDict.
    (This is similar to how dict will allow, for instance, {1:'foo', 1:'bar'}).

    >>> twd = TwoWayDict( {1:'foo', 1:'bar'} )
    >>> # Is twd[1] 'foo' or 'bar'?? Nobody knows!
    >>> # ...however, one of these is guaranteed to raise an error...
    >>> twd.get_key('foo') + twd.get_key('bar')   #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    KeyError: (either 'bar' or 'foo')
    >>> twd = TwoWayDict( {1:'foo', 2:'foo'} )
    >>> # Is twd.get_key('foo') 1 or 2? Nobody knows!
    >>> # ...however, one of these is guaranteed to raise an error...
    >>> twd[1] + twd[2]   #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    KeyError: (either 1 or 2)

    Obviously, such shenannigans should be avoided - at some point in the future, this may
    cause an error to be raised...
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self._reverse = {}
        self.update(*args, **kwargs)

    def __setitem__(self, k, v):
        # Maintain the 1-1 mapping
        if dict.__contains__(self, k):
            del self._reverse[self[k]]
        if v in self._reverse:
            dict.__delitem__(self, self.get_key(v))
        dict.__setitem__(self, k, v)
        self._reverse[v] = k

    def has_value(self, v):
        return self._reverse.has_key(v)

    def __delitem__(self, k):
        del self._reverse[self[k]]
        dict.__delitem__(self, k)

    def clear(self):
        self._reverse.clear()
        dict.clear(self)

    def copy(self):
        return TwoWayDict(self)

    def pop(self, k):
        del self._reverse[self[k]]
        return self.pop(k)

    def popitem(self, **kws):
        raise NotImplementedError()

    def setdefault(self, **kws):
        raise NotImplementedError()

    def update(self, *args, **kwargs):
        if not (args or kwargs):
            return
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' % len(args))
        # since args may be a couple different things, cast it to a dict to
        # simplify things...
        if args:
            tempDict = dict(args[0])
        else:
            tempDict = {}
        tempDict.update(kwargs)
        for key, val in tempDict.iteritems():
            self[key] = val

    def get_key(self, v):
        return self._reverse[v]

        
class SingletonType(type):
    _instance_lock = threading.Lock()
    
    
    def __init__(cls, name, bases, dic):
        super(SingletonType, cls).__init__(name, bases, dic)
        # print(cls,name,bases,dic)
        
        
    def __call__(cls, *args, **kwargs):
        # print(args)
        
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
                    
        cls._instance.__addvar__(*args)
        return cls._instance
    
    # def __new__(cls, name, bases, attrs):
    #     # print(name,bases,attrs)
    #     return super(SingletonType,cls).__new__(cls, name, bases, attrs)

        
class Binding(object):
    
    def __init__(self,val):
        self.__val = val
        
    # def __get__(self, instance, owner):
    #     return self.__val

    # def __set__(self, instance, val):
    #     self.__val = val

class GBinding(Binding):
    pass

class DataBinding(type):
    
    def __init__(cls, name, bases, attrs):
        super(DataBinding, cls).__init__(name, bases, attrs)
        for member,val in inspect.getmembers(cls):
            if isinstance(val,Binding):
                print(member,val)

def connect_binding(cls):
    """ https://stackoverflow.com/questions/11091609/setting-a-class-metaclass-using-a-decorator """
    __dict = dict(cls.__dict__)
    __dict["__metaclass__"] = DataBinding
    __dict["__wrapped__"] = cls
    return(DataBinding(cls.__name__, cls.__bases__, __dict))

@connect_binding
class Component(object):
    number = GBinding(1)
    temple = GBinding('temple')
    loc = Binding(True)
    
    def __init__(self,*args,**kwargs):
        super(Component, self).__init__(*args,**kwargs)
        number = self.number
        temple = self.temple
        print(number,temple)
    

comp = Component()

# print(dir(comp.temple))

