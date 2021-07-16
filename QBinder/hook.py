# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from types import BuiltinMethodType, MethodType

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 23:47:53"

import sys
import six
import types
import inspect
from functools import partial

import Qt
from Qt import QtCore, QtWidgets, QtGui

from .util import nestdict
from .hookconfig import CONFIG

HOOKS = nestdict()
_HOOKS_REL = nestdict()
qt_dict = {"QtWidgets.%s" % n: m for n, m in inspect.getmembers(QtWidgets)}
qt_dict.update({"QtCore.%s" % n: m for n, m in inspect.getmembers(QtCore)})
qt_dict.update({"QtGui.%s" % n: m for n, m in inspect.getmembers(QtGui)})


def byte2str(text):
    # NOTE compat python 2 and 3
    return str(text, encoding="utf-8") if sys.hexversion >= 0x3000000 else str(text)


def get_method_name(method):
    # NOTE compat Qt 4 and 5
    version = QtCore.qVersion()
    name = ""
    count = False
    if version.startswith("5"):
        name = method.name()
        count = method.parameterCount()
    elif version.startswith("4"):
        name = method.signature()
        name = name.split("(")[0]
        count = method.parameterNames()
    return byte2str(name), count


for name, member in qt_dict.items():
    # NOTE filter qt related func
    if name == "QtGui.QMatrix" or not hasattr(member, "staticMetaObject"):
        continue
    data = CONFIG.get(name, {})
    for method_name, method in inspect.getmembers(member, inspect.isroutine):
        if data.get(method_name):
            HOOKS[name][method_name] = {}
            if method_name.startswith("set"):
                _HOOKS_REL[method_name.lower()] = method_name

    # for i in range(meta_obj.methodCount()):
    #     method = meta_obj.method(i)
    #     method_name, count = get_method_name(method)
    #     if count and method.methodType() != QtCore.QMetaMethod.Signal:
    #         if hasattr(member, method_name):
    #             HOOKS[name][method_name] = {}
    #             _HOOKS_REL[name][method_name.lower()] = method_name

    # NOTE auto bind updater
    meta_obj = getattr(member, "staticMetaObject")
    if not meta_obj:
        continue
    for i in range(meta_obj.propertyCount()):
        property = meta_obj.property(i)
        if not property.hasNotifySignal():
            continue
        property_name = property.name()
        method_name = _HOOKS_REL.get("set%s" % property_name.lower())
        data = HOOKS[name].get(method_name)
        if isinstance(data, dict):
            updater, _ = get_method_name(property.notifySignal())
            if updater:
                data.update({"updater": updater, "property": property_name})


class HookMeta(type):
    def __call__(self, func=None):
        if callable(func):
            return self()(func)
        else:
            return super(HookMeta, self).__call__(func)


class HookBase(six.with_metaclass(HookMeta, object)):
    def __init__(self, options=None):
        self.options = options if options else {}

    @classmethod
    def combine_args(cls, val, args):
        if isinstance(val, tuple):
            return val + args[1:]
        else:
            return (val,) + args[1:]


class MethodHook(HookBase):
    @staticmethod
    def auto_dump(binding):
        """auto dump for two way binding"""
        from .constant import AUTO_DUMP

        binder = binding.__binder__
        if not AUTO_DUMP or not binder:
            return
        dumper = binder("dumper")
        for k, v in binder._var_dict_.items():
            if v is binding:
                dumper._filters_.add(k)
                break

    @staticmethod
    def remember_cursor_position(callback):
        """maintain the Qt edit cusorPosition after setting a new value"""

        def wrapper(self, *args, **kwargs):
            setter = None
            cursor_pos = 0
            pos = self.property("cursorPosition")
            # NOTE for editable combobox
            if pos and isinstance(self, QtWidgets.QComboBox):
                edit = self.lineEdit()
                pos = edit.property("cursorPosition")
            elif isinstance(self, QtWidgets.QTextEdit):
                cursor = self.textCursor()
                cursor_pos = cursor.position()

            callback(self, *args, **kwargs)

            # NOTE wait for two event call
            if cursor_pos:
                total = len(self.toPlainText())
                cursor.setPosition(total if cursor_pos > total else cursor_pos)
                setter = partial(self.setTextCursor, cursor)
            elif not pos is None:
                setter = partial(self.setProperty, "cursorPosition", pos)

            if callable(setter):
                QtCore.QTimer.singleShot(0, setter)

        return wrapper

    def __call__(cls, func):
        from .binding import Binding

        @six.wraps(func)
        def wrapper(self, *args, **kwargs):
            callback = args[0] if args else None
            if not isinstance(callback, types.LambdaType):
                return func(self, *args, **kwargs)

            # NOTE get the running bindings (with __get__ method) add to Binding._trace_list_
            with Binding.set_trace():
                val = callback()

            # NOTE *_args, **_kwargs for custom argument 
            def connect_callback(callback, args, *_args, **_kwargs):
                val = callback()
                args = cls.combine_args(val, args)
                # cls.remember_cursor_position(func)(self, *args, **kwargs)
                QtCore.QTimer.singleShot(
                    0,
                    lambda: cls.remember_cursor_position(func)(self, *args, **kwargs),
                )

            # NOTE register auto update
            _callback_ = partial(connect_callback, callback, args)
            for binding in Binding._trace_list_:
                binding.connect(_callback_)

            args = cls.combine_args(val, args)

            # NOTE Single binding connect to the updater
            updater = cls.options.get("updater")
            prop = cls.options.get("property")
            getter = cls.options.get("getter")
            _getter_1 = getattr(self, getter) if getter else None
            _getter_2 = lambda: self.property(prop) if prop else None
            getter = _getter_1 if _getter_1 else _getter_2
            code = callback.__code__

            if (
                updater
                and getter
                # NOTE only bind one response variable
                and len(Binding._trace_list_) == 1
                and len(code.co_consts) == 1  # NOTE only bind directly variable
            ):
                updater = getattr(self, updater)
                updater.connect(lambda *args: binding.set(getter()))
                binding = Binding._trace_list_.pop()
                QtCore.QTimer.singleShot(0, partial(cls.auto_dump, binding))

            return func(self, *args, **kwargs)

        return wrapper


class FuncHook(HookBase):
    def __call__(cls, func):
        from .binding import Binding

        @six.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != 1:
                return func(*args, **kwargs)

            callback = args[0]

            if isinstance(callback, types.LambdaType):

                # NOTE get the running bindings (with __get__ method) add to Binding._trace_list_
                with Binding.set_trace():
                    val = callback()

                def connect_callback(callback, args):
                    val = callback()
                    args = cls.combine_args(val, args)
                    func(*args, **kwargs)

                # NOTE register auto update
                _callback_ = partial(connect_callback, callback, args[1:])
                for binding in Binding._trace_list_:
                    binding.connect(_callback_)

                args = cls.combine_args(val, args[1:])
            return func(*args, **kwargs)

        return wrapper


def hook_initialize(hooks):
    """
    # NOTE Dynamic wrap the Qt Widget setter base on the HOOKS Definition
    """
    for widget, setters in hooks.items():
        lib, widget = widget.split(".")
        widget = getattr(getattr(Qt, lib), widget)
        for setter, options in setters.items():
            func = getattr(widget, setter)
            setattr(widget, setter, MethodHook(options)(func))
