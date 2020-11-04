# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-04 15:30:25"

import inspect
from contextlib import contextmanager
from collections import OrderedDict
from .binding import Binding, FnBinding


class BinderDispatcher(object):
    # NOTE Singleton
    __instance = None

    def __new__(cls, binder):
        cls.binder = binder
        if cls.__instance is None:
            cls.__instance = super(BinderDispatcher, cls).__new__(cls)
        return cls.__instance

    def dispatch(self, command, *args, **kwargs):
        method_dict = inspect.getmembers(self, predicate=inspect.ismethod)
        method_dict = OrderedDict(method_dict)
        method_dict.pop("dispatch")
        func = method_dict.get(command)
        if not func:
            raise RuntimeError("Binder Action %s not found" % command)
        return func(*args, **kwargs)

    def dump(self, *args, **kwargs):
        # TODO dump data
        print("dump", self.binder, args)

    def dispatcher(self, *args, **kwargs):
        return self


class BinderBase(object):
    _var_dict_ = {}
    def __getitem__(self, key):
        return self._var_dict_.get(key)

    def __setitem__(self, key, value):
        var = self._var_dict_.get(key)
        var.set(value) if var else None

    def __setattr__(self, key, value):
        print('__setattr__',key,value)
        binding = self._var_dict_.get(key)
        if binding:
            binding.set(value)
        else:
            # NOTE assign binding to class static member
            binding = Binding(value)
            self._var_dict_[key] = binding
            setattr(self.__class__, key, binding)

    def __call__(self, *args):
        # NOTE __call__ dispatch function avoid polluting local scope
        return BinderDispatcher(self).dispatch(*args)


class Binder(BinderBase):
    def __new__(cls, *args, **kw):
        # NOTE spawn differenct class instance to contain static member
        class BinderInstance(BinderBase):
            _var_dict_ = {}

        return cls.__new__(BinderInstance, *args, **kw)


class GBinder(BinderBase):
    # NOTE Global Singleton
    __instance = None
    _var_dict_ = {}

    def __new__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = BinderBase.__new__(cls, *args, **kw)
        return cls.__instance
    
# TODO bind function
# TODO record all the exist binder

@contextmanager
def init_binder():
    binder = BinderBase()
    yield binder

    # NOTE get the outer frame
    stacks = inspect.stack()
    frame = stacks[2][0]

    _var_dict_ = {n: s for n, s in inspect.getmembers(binder) if isinstance(s, Binding)}
    # TODO bind function
    # _func_dict_ = {n: s for n, s in inspect.getmembers(binder) if isinstance(s, Binding)}

    # TODO record all the exist binder

    _var_dict_.update({"_var_dict_": _var_dict_})

    class Binder(BinderBase):

        locals().update(_var_dict_)

        def __setattr__(self, key, value):
            binding = self._var_dict_.get(key)
            binding.set(value)

    cls = Binder

    # NOTE add to the local scope
    for k, v in frame.f_locals.items():
        if binder is v:
            binder = cls()
            frame.f_locals.update({k: binder})
            break
        
# TODO fn binding
def fn(func_name):
    return FnBinding(func_name)