# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-04 15:30:25"

import os
import six
import sys
import time
import uuid
import json
import random
import hashlib
import inspect
import tempfile
from functools import partial
from collections import OrderedDict
from Qt import QtCore, QtWidgets
from .binding import Binding,FnBinding, BindingProxy
from .util import nestdict
from collections import OrderedDict
from .eventhook import QEventHook, Iterable

event_hook = QEventHook()


class BinderCollector(QtCore.QObject):
    Binders = OrderedDict()
    __flag__ = True

    def get_current_Binders(self):
        uid = uuid.uuid4()
        if self.Binders:
            last_uid = list(self.Binders.keys())[-1]
            if self.__flag__:
                uid = last_uid
                self >> event_hook(QtCore.QEvent.User, lambda: self.set_flag(False))
                event = QtCore.QEvent(QtCore.QEvent.User)
                QtWidgets.QApplication.postEvent(self, event)
            else:
                self.set_flag(True)

        BinderCollector.Binders.setdefault(uid, [])
        return BinderCollector.Binders[uid]

    @classmethod
    def set_flag(cls, flag):
        cls.__flag__ = flag

    @classmethod
    def get_last_key(cls):
        return list(cls.Binders.keys())[-1]

class BinderDumper(QtCore.QObject):
    _dumper_dict_ = {}
    __init_flag = False

    def __new__(cls, binder, *args, **kwargs):
        instance = cls._dumper_dict_.get(id(binder))
        cls.__init_flag = not instance
        if cls.__init_flag:
            instance = super(BinderDumper, cls).__new__(cls, binder, *args, **kwargs)
            cls._dumper_dict_[id(binder)] = instance
        
        return instance

    def __init__(self, binder, db_name, filters=None):
        if not self.__init_flag:
            return
        super(BinderDumper, self).__init__()
        self.binder = binder
        self.db_name = db_name
        self._filters_ = (
            {filters}
            if isinstance(filters, str)
            else set(filters)
            if isinstance(filters, Iterable)
            else set()
        )
        folder = os.path.join(tempfile.gettempdir(), "QBinder")
        if not os.path.isdir(folder):
            os.mkdir(folder)
        self.path = os.path.join(folder, "%s.json" % db_name)

        # NOTE using timer call the __prepare__ in the next evnet loop (for loading delay)
        self >> event_hook(
            QtCore.QEvent.User, lambda: QtCore.QTimer.singleShot(0, self.__prepare__)
        )
        event = QtCore.QEvent(QtCore.QEvent.User)
        QtWidgets.QApplication.postEvent(self, event)
        
        self.auto_load = True

    def set_auto_load(self,enabeld):
        self.auto_load = enabeld

    def __prepare__(self):
        if self.auto_load:
            for k, binding in self.binder._var_dict_.items():
                if k in self._filters_:
                    binding.connect(self.save)
            self.load()

    def __enter__(self):
        BinderBase._trace_flag_ = True
        return self

    def __exit__(self, *args):
        BinderBase._trace_flag_ = False
        self._filters_.update(BinderBase._trace_setattr_)

    def __del__(self):
        self.__dumper_list.remove(self)
        super(BinderDumper, self).__del__()

    def save(self, path="", indent=None):
        path = path if path else self.path
        data = {
            k: v.val for k, v in self.binder._var_dict_.items() if k in self._filters_
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=indent)

    def load(self, path=""):
        path = path if path else self.path
        if not os.path.exists(path):
            return
        QtCore.QTimer.singleShot(0, partial(self.read, path))

    def read(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f, encoding="utf-8")
            for k, v in data.items():
                setattr(self.binder, k, v)
        except:
            # NOTE May be the file broken
            os.remove(path)


class BinderDispatcher(QtCore.QObject):
    _trace_dict_ = nestdict()
    __instance = None
    __init_flag = False

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
            self >> event_hook(QtCore.QEvent.User, self.__bind_cls__)
        event = QtCore.QEvent(QtCore.QEvent.User)
        QtWidgets.QApplication.postEvent(self, event)

    def __bind_cls__(self):
        for module, data in self._trace_dict_.items():
            for cls_name, _data in data.items():
                if hasattr(module, cls_name):
                    cls = getattr(module, cls_name)
                    for _, binding in _data.items():
                        binding.cls = cls
        self._trace_dict_.clear()

    def dispatch(self, command, *args, **kwargs):
        method_dict = OrderedDict(inspect.getmembers(self, predicate=inspect.ismethod))
        method_dict.pop("dispatch")
        func = method_dict.get(command)
        if func is None:
            raise RuntimeError("Binder Action %s not found" % command)
        return func(*args, **kwargs)

    def dumper(self, db_name=None, filters=None):
        dumper = BinderDumper._dumper_dict_.get(id(self.binder))
        db_name = dumper.db_name if dumper else db_name
        if not db_name:
            uid = BinderCollector.get_last_key()
            binder_list = BinderCollector.Binders[uid]
            index = binder_list.index(self.binder)
            rd = random.Random()
            rd.seed(index)
            hex = uuid.UUID(int=rd.getrandbits(128)).hex
            path = inspect.stack()[-1][1]
            md5 = hashlib.md5("".join((path, hex)).encode("utf-8")).hexdigest()
            db_name = md5

        return BinderDumper(self.binder, db_name, filters)

    def fn_bind(self, attr=None):
        """fn_bind
        https://stackoverflow.com/a/13699329
        """

        def wrapper(func):
            binding = FnBinding(self.binder, func)
            function = func if six.callable(func) else func.__func__
            fn_name = attr if attr else function.__name__
            setattr(self.binder.__class__, fn_name, binding)

            stack = inspect.stack()[-2]
            cls_name = stack[3]
            frame = stack[0]
            module = inspect.getmodule(frame)

            self._trace_dict_[module][cls_name][fn_name] = binding

            return func

        return wrapper

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
    _trace_flag_ = False
    _trace_setattr_ = []

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
        if self._trace_flag_:
            self._trace_setattr_.append(key)
        binding = self._var_dict_.get(key)
        if binding:
            binding.set(value)
        else:
            # NOTE assign binding to class static member
            binding = Binding(value)
            binding.__binder__ = self
            self._var_dict_[key] = binding
            setattr(self.__class__, key, binding)
            if isinstance(value, FnBinding):
                value.connect_binder(key, self)

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
        binder_list = BinderCollector().get_current_Binders()
        binder_list.append(instance)
        return instance


class GBinder(BinderBase):
    # NOTE Global Singleton
    __instance = None
    _var_dict_ = {}

    # TODO Group by arg string
    def __new__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = BinderBase.__new__(cls)
            binder_list = BinderCollector().get_current_Binders()
            binder_list.append(
                cls.__instance
            ) if cls.__instance not in binder_list else None
        return cls.__instance

class BinderTemplate(object):
    
    def __new__(cls,*args,**kwargs):
        binder = Binder()
        cls.__init__(binder,*args,**kwargs)
        for name,member in inspect.getmembers(cls):
            if name.startswith("__"):
                continue
            if inspect.isroutine(member):
                setattr(binder,name,partial(member,binder))
            else:
                setattr(binder,name,member)
        return binder

