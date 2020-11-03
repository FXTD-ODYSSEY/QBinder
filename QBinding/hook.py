# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 23:47:53"

import sys
import six
import inspect
from functools import partial

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

from .type import Binding

HOOKS = {
    QtWidgets.QComboBox: {
        "setCurrentIndex": {
            "type": int,
            "getter": "currentIndex",
            "updater": "currentIndexChanged",
        },
        "setCurrentText": {
            "type": str,
            "getter": "currentText",
            "updater": "currentTextChanged",
        },
        # "addItem": {
        #     "type":str,
        # },
    },
    QtWidgets.QLineEdit: {
        "setText": {
            "type": str,
            "getter": "text",
            "updater": "textChanged",
        },
    },
    QtWidgets.QLabel: {
        "setText": {"type": str, "getter": "text"},
    },
    QtWidgets.QCheckBox: {
        "setChecked": {
            "type": bool,
            "getter": "isChecked",
            "updater": "stateChanged",
        },
        "setText": {"type": str, "getter": "text"},
    },
    QtWidgets.QRadioButton: {
        "setChecked": {
            "type": bool,
            "getter": "isChecked",
            "updater": "stateChanged",
        },
        "setText": {"type": str, "getter": "text"},
    },
    QtWidgets.QSpinBox: {
        "setValue": {
            "type": int,
            "getter": "getValue",
            "updater": "valueChanged",
        },
    },
    QtWidgets.QDoubleSpinBox: {
        "setValue": {
            "type": float,
            "getter": "getValue",
            "updater": "valueChanged",
        },
    },
}


def state_handler(func, options=None):
    """
    # NOTE initialize the Qt Widget setter
    """
    options = options if options is not None else {}
    typ = options.get("type")

    def fix_cursor_position(func, widget):
        """fix the lineedit cusorPosition after setting the value"""

        def wrapper(*args, **kwargs):
            pos = widget.property("cursorPosition")
            res = func(*args, **kwargs)
            widget.setProperty("cursorPosition", pos) if pos else None
            return res

        return wrapper

    def wrapper(self, value, *args, **kwargs):
        if callable(value):
            # # NOTE get the outter frame state attribute from the widget class
            # frame = inspect.currentframe().f_back
            # parent = frame.f_locals.get('self')

            with Binding.set_trace():
                val = value()

            # NOTE register auto update
            callback = partial(
                lambda c: func(self, typ(c()) if typ else c(), *args, **kwargs), value
            )
            for binding in Binding.TRACE_LIST:
                binding.connect(callback)

            updater = options.get("updater")
            getter = options.get("getter")

            code = value.__code__
            # NOTE Single binding connect to the updater
            if (
                updater
                and getter
                and len(Binding.TRACE_LIST) == 1
                and len(code.co_consts) == 1
            ):
                updater = getattr(self, updater)
                getter = getattr(self, getter)
                updater.connect(
                    fix_cursor_position(lambda *args: binding.set(getter()), self)
                )

            value = typ(val) if typ else val

        res = func(self, value, *args, **kwargs)
        return res

    return wrapper


def hook_initialize():
    """
    # NOTE Dynamic wrap the Qt Widget setter base on the HOOKS Definition
    """
    for widget, setters in HOOKS.items():
        for setter, options in setters.items():
            wrapper = state_handler(getattr(widget, setter), options)
            setattr(widget, setter, wrapper)
