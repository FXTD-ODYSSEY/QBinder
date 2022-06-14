# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 23:47:53"

import re
import sys
import six
import types
import inspect
from functools import partial

import Qt
from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui
from Qt.QtCompat import isValid

from .util import nestdict
from .hookconfig import CONFIG

HOOKS = nestdict()
_HOOKS_REL = nestdict()
qt_dict = {"QtWidgets.%s" % n: m for n, m in inspect.getmembers(QtWidgets)}
qt_dict.update({"QtCore.%s" % n: m for n, m in inspect.getmembers(QtCore)})
qt_dict.update({"QtGui.%s" % n: m for n, m in inspect.getmembers(QtGui)})


def _cell_factory():
    a = 1
    f = lambda: a + 1
    return f.__closure__[0]


CellType = type(_cell_factory())


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


def get_property_count(meta_obj):
    if not isinstance(meta_obj, QtCore.QMetaObject):
        return
    try:
        count = meta_obj.propertyCount()
        return count
    except RuntimeError:
        pass


def _initialize():
    for name, member in qt_dict.items():
        # NOTE filter qt related func
        if name == "QtGui.QMatrix" or not hasattr(member, "staticMetaObject"):
            continue
        data = CONFIG.get(name, {})
        for method_name, _ in inspect.getmembers(member, inspect.isroutine):
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
        meta_obj = getattr(member, "staticMetaObject", None)
        count = get_property_count(meta_obj)
        if count is None and issubclass(member, QtCore.QObject):
            meta_obj = member().metaObject()
            count = get_property_count(meta_obj)

        for i in range(count or 0):
            prop = meta_obj.property(i)
            if not prop.hasNotifySignal():
                continue
            property_name = prop.name()
            method_name = _HOOKS_REL.get("set%s" % property_name.lower())
            data = HOOKS[name].get(method_name)
            if isinstance(data, dict):
                updater, _ = get_method_name(prop.notifySignal())
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

    @classmethod
    def trace_callback(cls, callback, self=None):
        """trigger all possible binder binding __get__ call"""
        pattern = "QBinder.binder.*BinderInstance"
        closure = getattr(callback, "__closure__", None)
        closure = closure if closure else [self] if self else []
        code = callback.__code__
        names = code.co_names

        for cell in closure:
            self = cell.cell_contents if isinstance(cell, CellType) else cell
            for name in names:
                binder = getattr(self, name, None)
                if not binder:
                    continue
                if re.search(pattern, str(binder.__class__)):
                    for _name in names:
                        getattr(binder, _name, None)
                # NOTE `lambda: self.callback()` hook class callback
                elif callable(binder):
                    cls.trace_callback(binder, self)


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
            if self and not isValid(self):
                del self
                return
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

    def __call__(self, func):
        from .binding import Binding

        @six.wraps(func)
        def wrapper(_self, *args, **kwargs):
            callback = args[0] if args else None
            if isinstance(callback, types.LambdaType):

                # NOTE get the running bindings (with __get__ method) add to Binding._trace_dict_
                with Binding.set_trace():
                    val = callback()
                    self.trace_callback(callback)

                # NOTE *_args, **_kwargs for custom argument
                def connect_callback(callback, args, *_args, **_kwargs):
                    args = self.combine_args(callback(), args)
                    self.remember_cursor_position(func)(_self, *args, **kwargs)
                    # TODO some case need to delay for cursor position but it would broke the slider sync effect
                    # QtCore.QTimer.singleShot(
                    #     0,
                    #     lambda: cls.remember_cursor_position(func)(self, *args, **kwargs),
                    # )

                # NOTE register auto update
                _callback_ = partial(connect_callback, callback, args)
                for binding in Binding._trace_dict_.values():
                    binding.connect(_callback_)
                args = self.combine_args(val, args)

                # NOTE Single binding connect to the updater
                updater = self.options.get("updater")
                prop = self.options.get("property")
                getter = self.options.get("getter")
                _getter_1 = getattr(_self, getter) if getter else None
                _getter_2 = lambda: _self.property(prop) if prop else None
                getter = _getter_1 if _getter_1 else _getter_2
                code = callback.__code__

                if (
                    updater
                    and getter
                    # NOTE only bind one response variable
                    and len(Binding._trace_dict_) == 1
                    and len(code.co_consts) == 1  # NOTE only bind directly variable
                ):
                    updater = getattr(_self, updater)
                    updater.connect(lambda *args: binding.set(getter()))
                    binding = list(Binding._trace_dict_.values())[0]
                    QtCore.QTimer.singleShot(0, partial(self.auto_dump, binding))

            return func(_self, *args, **kwargs)

        return wrapper


class FuncHook(HookBase):
    def __call__(self, func):
        from .binding import Binding

        @six.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != 1:
                return func(*args, **kwargs)

            callback = args[0]

            if isinstance(callback, types.LambdaType):

                # NOTE get the running bindings (with __get__ method) add to Binding._trace_dict_
                with Binding.set_trace():
                    val = callback()
                    self.trace_callback(callback)

                def connect_callback(callback, args):
                    val = callback()
                    args = self.combine_args(val, args)
                    func(*args, **kwargs)

                # NOTE register auto update
                _callback_ = partial(connect_callback, callback, args[1:])
                for binding in Binding._trace_dict_.values():
                    binding.connect(_callback_)

                args = self.combine_args(val, args[1:])
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


_initialize()
