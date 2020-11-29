# coding:utf-8
from __future__ import division, print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-05-06 23:02:37"

"""

"""


import six
import sys
import time
import inspect
from functools import partial, wraps
from collections import OrderedDict
from contextlib import contextmanager
from Qt import QtCore, QtGui, QtWidgets
from .eventhook import QEventHook


event_hook = QEventHook()


class BindingBase(object):
    pass


class BindingProxy(BindingBase):
    def __init__(self, binder, attr):
        self.binder = binder
        self.attr = attr

    def __rrshift__(self, d):
        self.binder.__setattr__(self.attr, d)
        del self
        return d

    def __iter__(self):
        for attr in dir(self):
            yield attr


class FnBinding(BindingBase):
    
    def __init__(self, binder=None, func=None):
        from .binder import Binder
        self.cls = None
        self.binder = binder
        self.binded = isinstance(binder,Binder)
        if self.binded:
            self.func = func if six.callable(func) else func.__func__
            self.static = isinstance(self.func, staticmethod)
    
    def connect_binder(self, name, binder):
        """
        connect_binder automatically run by the BinderBase __setattr__
        """
        self.name = name
        self.binder = binder

    def __call__(self, *args, **kwargs):
        
        # NOTE if not initialize binded should bind func
        if not self.binded:
            self.binded = True
            func = args[0]
            self.func = func if six.callable(func) else func.__func__
            self.static = isinstance(func, staticmethod)
            
            stack = inspect.stack()[-2]
            cls_name = stack[3]
            frame = stack[0]
            module = inspect.getmodule(frame)
            dispatcher = self.binder('dispatcher')
            dispatcher._trace_dict_[module][cls_name][self.func.__name__] = self

            return self.func
        
        arg = self.binder
        if self.cls:
            # TODO not very good solution | may be try __subclasshook__
            # NOTE Try to Get A Default Instance from binder
            for _, member in inspect.getmembers(self.binder, lambda f: not callable(f)):
                if type(member) is self.cls:
                    arg = member
                    return self.func(arg, *args, **kwargs)
        
        return self.func(*args, **kwargs)

    def __getitem__(self, attr):
        # NOTE special bind 
        attr = getattr(self.binder, attr) if type(attr) is str else attr

        @six.wraps(self.func)
        def wrapper(*args, **kw):
            if self.static:
                return self.func(*args, **kw)
            else:
                length = len(inspect.getargspec(self.func).args)
                return self.func(attr, *args[: length - 1], **kw)

        return wrapper


def notify(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        if hasattr(self, "STATE"):
            self.STATE.emitDataChanged()
            self.STATE.emit()
        return res

    return wrapper


class NotifyList(list):
    """
    https://stackoverflow.com/questions/13259179/list-callbacks
    """

    __repr__ = list.__repr__

    def __init__(self, val, STATE):
        super(NotifyList, self).__init__(val)
        self.STATE = STATE

    extend = notify(list.extend)
    append = notify(list.append)
    remove = notify(list.remove)
    pop = notify(list.pop)
    __iadd__ = notify(list.__iadd__)
    __imul__ = notify(list.__imul__)

    # Take care to return a new NotifyList if we slice it.
    if sys.version_info[0] < 3:
        __setslice__ = notify(list.__setslice__)
        __delslice__ = notify(list.__delslice__)

        def __getslice__(self, *args):
            return self.__class__(list.__getslice__(self, *args))

    __delitem__ = notify(list.__delitem__)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(list.__getitem__(self, item))
        else:
            return list.__getitem__(self, item)

    @notify
    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = NotifyDict(value, self.STATE)
        elif isinstance(value, list):
            value = NotifyList(value, self.STATE)
        list.__setitem__(self, key, value)


class NotifyDict(OrderedDict):
    """
    https://stackoverflow.com/questions/5186520/python-property-change-listener-pattern
    """

    __repr__ = dict.__repr__

    def __init__(self, val, STATE):
        super(NotifyDict, self).__init__(val)
        self.STATE = STATE

    clear = notify(OrderedDict.clear)
    pop = notify(OrderedDict.pop)
    popitem = notify(OrderedDict.popitem)
    setdefault = notify(OrderedDict.setdefault)
    update = notify(OrderedDict.update)
    __delitem__ = notify(OrderedDict.__delitem__)

    @notify
    def __setitem__(self, key, value):
        if hasattr(self, "STATE"):
            if isinstance(value, dict):
                value = NotifyDict(value, self.STATE)
            elif isinstance(value, list):
                value = NotifyList(value, self.STATE)
        return OrderedDict.__setitem__(self, key, value)


class Binding(QtGui.QStandardItem, BindingBase):

    __trace = False
    __emit_flag = False
    _trace_list_ = []
    _inst_ = []

    __repr__ = lambda self: repr(self.val)
    __str__ = lambda self: str(self.val)

    operator_list = {
        "__add__": lambda self, x: self.val.__add__(x),
        "__sub__": lambda self, x: self.val.__sub__(x),
        "__mul__": lambda self, x: self.val.__mul__(x),
        "__floordiv__": lambda self, x: self.val.__floordiv__(x),
        "__truediv__": lambda self, x: self.val.__truediv__(x),
        "__mod__": lambda self, x: self.val.__mod__(x),
        "__pow__": lambda self, x: self.val.__pow__(x),
        "__lshift__": lambda self, x: self.val.__lshift__(x),
        "__rshift__": lambda self, x: self.val.__rshift__(x),
        "__and__": lambda self, x: self.val.__and__(x),
        "__xor__": lambda self, x: self.val.__xor__(x),
        "__or__": lambda self, x: self.val.__or__(x),
        "__iadd__": lambda self, x: self.val.__iadd__(x),
        "__isub__": lambda self, x: self.val.__isub__(x),
        "__imul__": lambda self, x: self.val.__imul__(x),
        "__idiv__": lambda self, x: self.val.__idiv__(x),
        "__ifloordiv__": lambda self, x: self.val.__ifloordiv__(x),
        "__imod__": lambda self, x: self.val.__imod__(x),
        "__ipow__": lambda self, x: self.val.__ipow__(x),
        "__ilshift__": lambda self, x: self.val.__ilshift__(x),
        "__irshift__": lambda self, x: self.val.__irshift__(x),
        "__iand__": lambda self, x: self.val.__iand__(x),
        "__ixor__": lambda self, x: self.val.__ixor__(x),
        "__ior__": lambda self, x: self.val.__ior__(x),
        "__neg__": lambda self, x: self.val.__neg__(x),
        "__pos__": lambda self, x: self.val.__pos__(x),
        "__abs__": lambda self, x: self.val.__abs__(x),
        "__invert__": lambda self, x: self.val.__invert__(x),
        "__complex__": lambda self, x: self.val.__complex__(x),
        "__int__": lambda self, x: self.val.__int__(x),
        "__long__": lambda self, x: self.val.__long__(x),
        "__float__": lambda self, x: self.val.__float__(x),
        "__oct__": lambda self, x: self.val.__oct__(x),
        "__hex__": lambda self, x: self.val.__hex__(x),
        "__lt__": lambda self, x: self.val.__lt__(x),
        "__le__": lambda self, x: self.val.__le__(x),
        "__eq__": lambda self, x: self.val.__eq__(x),
        "__ne__": lambda self, x: self.val.__ne__(x),
        "__ge__": lambda self, x: self.val.__ge__(x),
        "__gt__": lambda self, x: self.val.__gt__(x),
    }

    def __init__(self, val=None):
        super(Binding, self).__init__()
        self.val = self.retrieve2Notify(val)
        self.overrideOperator(self.val)
        self.event_loop = []
        self.__binder__ = None

    @classmethod
    @contextmanager
    def set_trace(cls):
        del cls._trace_list_[:]
        cls.__trace = True
        yield
        cls.__trace = False

    def __get__(self, instance, owner):
        self.__class__._inst_ = [self]
        self._trace_list_.append(self) if self.__trace else None
        return self.get()

    def __rrshift__(self, d):
        self.set(d)
        return d

    def set(self, value):
        # if value == self.get():
        #     return
        self.val = self.retrieve2Notify(value)
        self.overrideOperator(value)
        self.emitDataChanged()
        self.emit()

    def get(self):
        return self.val

    @classmethod
    def overrideOperator(cls, val):
        for attr, func in cls.operator_list.items():
            if attr in dir(val):
                setattr(cls, attr, func)

    def retrieve2Notify(self, val, initialize=True):
        """ convert to Notify type """
        itr = (
            six.iteritems(val)
            if isinstance(val, dict)
            else enumerate(val)
            if isinstance(val, list)
            else []
        )
        for k, v in itr:
            if isinstance(v, dict):
                self.retrieve2Notify(v, initialize=False)
                val[k] = NotifyDict(v, self)
            elif isinstance(v, list):
                self.retrieve2Notify(v, initialize=False)
                val[k] = NotifyList(v, self)

        if initialize:
            if isinstance(val, dict):
                return NotifyDict(val, self)
            elif isinstance(val, list):
                return NotifyList(val, self)
            else:
                return val

    def data(self, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return str(self.val)

    def setData(self, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.set(value)
            return True
        return False

    def connect(self, callback):
        self.event_loop.append(callback)
        return callback

    def disconnect(self, callback):
        self.event_loop.remove(callback)

    def emit(self, *args, **kwargs):
        QtCore.QTimer.singleShot(0, lambda: self.run_event(*args, **kwargs))
        self.__emit_flag = True

    def run_event(self, *args, **kwargs):
        if self.__emit_flag:
            self.__emit_flag = False
            for callback in self.event_loop[:]:
                if six.callable(callback):
                    try:
                        callback(*args, **kwargs)
                    except:
                        self.event_loop.remove(callback)


class Model(QtGui.QStandardItemModel):
    def __init__(self, source=None):
        super(Model, self).__init__()
        self.setSource(source)

    def dataChangedEmit(self):
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def setSource(self, source):
        # NOTE update source data remove old callback
        [
            item.disconnect(self.dataChangedEmit)
            for row in self._source
            for item in row
            if isinstance(item, Binding)
        ] if hasattr(self, "_source") else None

        self._source = (
            [
                item
                if isinstance(item, list)
                else [item if isinstance(item, Binding) else item]
                for item in source
            ]
            if source
            else []
        )

        self.setRowCount(len(self._source))
        self.setColumnCount(max([len(row) for row in self._source]))
        
        # NOTE add data update callback
        for row in self._source:
            for item in row:
                if isinstance(item, Binding):
                    item.connect(self.dataChangedEmit)

        # NOTE fill None to the empty cell
        columnCount = max([len(row) for row in self._source])
        for row in self._source:
            rowCount = len(row)
            if rowCount < columnCount:
                row.extend([None for i in range(columnCount - rowCount)])

    # def index(self, row, column, parent=QtCore.QModelIndex()):
    #     return self.createIndex(row, column)

    # def parent(self, index):
    #     return QtCore.QModelIndex()

    # def rowCount(self, parent):
    #     return len(self._source) if parent.row() == -1 else 0

    # def columnCount(self, parent):
    #     return 10
    #     return max([len(row) for row in self._source])

    def item(self, row, column):
        row_list = next(iter(self._source[row:]), None)
        if row_list is None:
            return
        return next(iter(row_list[column:]), None)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.isValid():
                item = self.item(index.row(), index.column())
                return (
                    item.val
                    if isinstance(item, Binding)
                    else item.text()
                    if isinstance(item, QtGui.QStandardItem)
                    else str(item)
                )

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if index.isValid():
                row = index.row()
                column = index.column()
                item = self.item(row, column)
                if isinstance(item, Binding):
                    item.set(value)
                elif isinstance(item, QtGui.QStandardItem):
                    item.setText(value)
                else:
                    self._source[row][column] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
        )

    def get(self):
        return self._source
