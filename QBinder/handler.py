# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-15 20:11:41"

from functools import partial

import six
from .binding import Binding
from .util import ListGet
from Qt import QtWidgets


class HandlerBase(object):
    pass

class ItemMeta(type):
    
    def __getitem__(cls,item):
        cls.item = item
        return cls
    
class ItemConstructor(HandlerBase,six.with_metaclass(ItemMeta)):
    
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def __rrshift__(self, item_data):
        # binding = Binding._inst_.pop()
        
        # NOTE trace lamda function
        filters = self.kwargs.pop("__filters__", [i for i in range(len(item_data))])
        if callable(filters):
            # NOTE make sure handle list data
            filters = [item_data.index(d) for d in filters(item_data)]

        layout = self.kwargs.pop("__layout__")
        binder_name = self.kwargs.pop("__binder__")

        if not hasattr(layout,'__items__'):
            layout.__items__ = []
            
        for i, data in enumerate(item_data):
            widget = layout.__items__ >> ListGet(i)
            if not widget:
                widget = self.item(*self.args, **self.kwargs)
                layout.addWidget(widget)
                layout.__items__.append(widget)
                widget.__index__ = i

            widget.setVisible(i in filters)

            if hasattr(widget, binder_name):
                binder = getattr(widget, binder_name)
                for k, v in data.items():
                    val = getattr(binder, k)
                    setattr(binder, k, v)

        for i in range(len(item_data), len(layout.__items__)):
            widget = layout.__items__[i]
            widget.deleteLater()
        layout.__items__ = layout.__items__[: len(item_data)]


class GroupBoxBind(HandlerBase):
    def __init__(self, group):
        self.group = group

    def __rrshift__(self, binding):
        self.binding = Binding._inst_.pop()
        for rb in self.group.findChildren(QtWidgets.QRadioButton):
            rb.toggled.connect(partial(self.filter_state, rb))
        self.binding.connect(self.check_state) >> Call()

        return self.binding

    def filter_state(self, rb, state):
        if state:
            self.binding.set(rb.text().strip())

    def check_state(self):
        for rb in self.group.findChildren(QtWidgets.QRadioButton):
            if rb.text().strip() == self.binding.val:
                rb.setChecked(True)


class Call(HandlerBase):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __rrshift__(self, func):
        return func(*self.args, **self.kwargs)


class Set(HandlerBase):
    def __init__(self, val):
        self.val = val

    def __rrshift__(self, binding):
        binding = Binding._inst_.pop()
        binding.set(self.val)
        return binding


class Anim(HandlerBase):
    # TODO support anim value change
    def __init__(self, val):
        self.val = val

    def __rrshift__(self, binding):
        Binding._inst_
        return binding