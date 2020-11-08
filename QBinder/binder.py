# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-04 15:30:25"

import sys
import uuid
import random
import inspect
from functools import partial
from collections import OrderedDict, defaultdict

from Qt import QtCore, QtWidgets
from .binding import Binding, FnBinding, BindingProxy

# NOTE https://stackoverflow.com/a/8702435
nested_dict = lambda: defaultdict(nested_dict)

# TODO collect all the exist binder for dumping
class BinderCollector(object):
    Binders = defaultdict(list)
    GBinders = nested_dict()


class BinderDispatcher(QtCore.QObject):
    __instance = None
    __init_flag = False
    __trace_dict = nested_dict()

    def __new__(cls, binder):
        cls.binder = binder
        if cls.__instance is None:
            cls.__instance = super(BinderDispatcher, cls).__new__(cls)
            cls.__init_flag = True

        return cls.__instance

    def __init__(self, binder):
        if self.__init_flag:
            self.__init_flag = False
            super(BinderDispatcher, self).__init__()
            self.installEventFilter(self)

        # NOTE
        # post Qt event loop so that I can wait until qapp instantiate
        # using event filter receive event
        event = QtCore.QEvent(QtCore.QEvent.User)
        QtWidgets.QApplication.postEvent(self, event)

    def eventFilter(self, reciver, event):
        if reciver is self and reciver.__trace_dict:
            for module, data in reciver.__trace_dict.items():
                for cls_name, _data in data.items():
                    cls = getattr(module, cls_name)
                    for _, binding in _data.items():
                        binding.cls = cls
            reciver.__trace_dict.clear()
        return False

    def dispatch(self, command, *args, **kwargs):
        method_dict = inspect.getmembers(self, predicate=inspect.ismethod)
        method_dict = OrderedDict(method_dict)
        method_dict.pop("dispatch")
        func = method_dict.get(command)
        if func is None:
            raise RuntimeError("Binder Action %s not found" % command)
        return func(*args, **kwargs)

    def dump(self, *args, **kwargs):
        # TODO dump data
        print("dump", self.binder, args)

    def fn_bind(self, attr=None):
        """fn_bind
        https://stackoverflow.com/a/13699329
        """

        def decorator(func):
            binding = FnBinding(self.binder, func)
            function = func if callable(func) else func.__func__
            fn_name = attr if attr else function.__name__
            setattr(self.binder.__class__, fn_name, binding)

            stack = inspect.stack()[1]
            cls_name = stack[3]
            frame = stack[0]
            module = inspect.getmodule(frame)

            self.__trace_dict[module][cls_name][fn_name] = binding

            return func

        return decorator

    def dispatcher(self):
        return self


class BinderProxy(object):
    _var_dict_ = {}

    def __getitem__(self, key):
        return self._var_dict_.get(key)

    def __setitem__(self, key, value):
        var = self._var_dict_.get(key)
        var.set(value) if var else None

    def __setattr__(self, key, value):
        self._var_dict_[key] = value
        value = value if isinstance(value, Binding) else Binding(value)
        self.__dict__[key] = value


class BinderBase(object):
    _var_dict_ = {}

    def __getitem__(self, key):
        val = self._var_dict_.get(key)
        if val is not None:
            return val
        else:
            return BindingProxy(self, key)

    def __setitem__(self, key, value):
        var = self._var_dict_.get(key)
        var.set(value) if var else None

    # def __getattr__(self, key):
    #     return BindingProxy(self, key)

    def __setattr__(self, key, value):
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

    def __enter__(self):
        # NOTE support with statement for group indent
        self.proxy = BinderProxy()
        return self.proxy

    def __exit__(self, *args):
        # NOTE get the outer frame
        frame = inspect.currentframe().f_back

        for k, v in frame.f_locals.items():
            if self.proxy is v:
                for n, s in inspect.getmembers(self.proxy):
                    if isinstance(s, Binding):
                        self._var_dict_[n] = s
                        setattr(self.__class__, n, s)
                # NOTE overwrite the local scope like `return` action
                frame.f_locals.update({k: self})
                break


class Binder(BinderBase):
    def __new__(cls, *args, **kw):
        # NOTE spawn differenct class instance to contain static member
        class BinderInstance(BinderBase):
            _var_dict_ = {}

        instance = cls.__new__(BinderInstance)
        # print(instance)
        frame = inspect.currentframe().f_back
        code = frame.f_code

        rd = random.Random()
        rd.seed(1024)
        hex = uuid.UUID(int=rd.getrandbits(128)).hex

        # print(dir(code))
        # print(code.co_filename)
        # print(code.co_name)
        # print(code.co_flags)
        # print(code.co_stacksize)
        # print(code.co_varnames)
        # print(dir(frame))
        # print(instance.__module__)

        # # TODO 通过 frame 获取唯一表示符 给 collector
        # binders = BinderCollector.Binders
        # binders.append(instance) if instance not in binders else None
        return instance


class GBinder(BinderBase):
    # NOTE Global Singleton
    __instance = None
    _var_dict_ = {}

    # TODO Group by arg string
    def __new__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = BinderBase.__new__(cls)
        return cls.__instance
