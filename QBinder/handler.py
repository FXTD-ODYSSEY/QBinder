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
from .eventhook import Iterable
from Qt import QtWidgets, QtCore


class HandlerBase(object):
    def __rrshift__(self, _):
        binding = Binding._inst_.pop()
        self.handle(binding)

    def handle(self, binding):
        raise NotImplementedError


class ItemMeta(type):
    def __getitem__(cls, item):
        # NOTE support cls[item]
        cls.item = item
        return cls


class ItemConstructor(HandlerBase, six.with_metaclass(ItemMeta)):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __rrshift__(self, item_data):
        # NOTE trace lambda function
        filters = self.kwargs.pop("__filters__", [i for i in range(len(item_data))])
        if callable(filters):
            # NOTE make sure handle list data
            filters = [item_data.index(d) for d in filters(item_data)]

        layout = self.kwargs.pop("__layout__")
        binder_name = self.kwargs.pop("__binder__")
        index = self.kwargs.pop("__index__", 0)

        if not hasattr(layout, "__items__"):
            layout.__items__ = []

        for i, data in enumerate(item_data):
            widget = layout.__items__ >> ListGet(i)
            if not widget:
                widget = self.item(*self.args, **self.kwargs)
                layout.insertWidget(i + index, widget)
                layout.__items__.append(widget)
                if hasattr(widget, "__item__"):
                    widget.__item__(i, item_data, layout)

            widget.setVisible(i in filters)

            if hasattr(widget, binder_name):
                # NOTE delay update
                QtCore.QTimer.singleShot(
                    0, partial(self._update_value_, data, widget, binder_name)
                )

        for i in reversed(range(len(item_data), len(layout.__items__))):
            widget = layout.__items__[i]
            widget.hide()
        # layout.__items__ = layout.__items__[: len(item_data)]

    def _update_value_(self, data, widget, binder_name):
        binder = getattr(widget, binder_name)
        for k, v in data.items():
            val = getattr(binder, k)
            # NOTE avoid infinite loop
            if val != v:
                setattr(binder, k, v)


class GroupBoxBind(HandlerBase):
    def __init__(self, group):
        self.group = group

    def handle(self, binding):
        self.binding = binding
        for rb in self.group.findChildren(QtWidgets.QRadioButton):
            rb.toggled.connect(partial(self.filter_state, rb))
        self.binding.connect(self.check_state) >> Call()

        return self.binding

    def filter_state(self, rb, state):
        state and self.binding.set(rb.text().strip())

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

    def handle(self, binding):
        binding.set(self.val)
        return binding


class QAnim(QtCore.QVariantAnimation):
    def __init__(self, parent=None):
        # NOTE avoid gc
        parent = parent if parent else QtWidgets.QApplication.activeWindow()
        super(QAnim, self).__init__(parent)

    def updateCurrentValue(self, v):
        pass
        # return super(QAnim, self).updateCurrentValue(v)


class Anim(HandlerBase):
    # NOTE support anim value change
    def __init__(
        self,
        value,
        duration=1000,
        easing=QtCore.QEasingCurve.Linear,
        valueChanged=None,
        finished=None,
    ):
        self.value_list = value if isinstance(value, Iterable) else [value]
        self.duration = duration
        self.valueChanged = valueChanged
        self.finished = finished
        self.easing = easing

    def handle(self, binding):
        data = binding.get()
        data_list = data if isinstance(data, Iterable) else [data]

        anim_list = []
        for i, (start, value) in enumerate(zip(data_list, self.value_list)):
            anim = QAnim()
            anim_list.append(anim)
            anim.setDuration(self.duration)

            def value_change(i, v):
                value = binding.get()
                if not isinstance(value, Iterable):
                    binding.set(v)
                else:
                    value[i] = v
                    binding.set(value)

            anim.valueChanged.connect(partial(value_change, i))
            anim.finished.connect(anim.deleteLater)
            anim.setEasingCurve(self.easing)

            anim.setStartValue(start)
            anim.setEndValue(value)
            anim.start()

            if callable(self.finished):
                anim.finished.connect(self.finished)
            if callable(self.valueChanged):
                anim.valueChanged.connect(self.valueChanged)

        return anim_list
