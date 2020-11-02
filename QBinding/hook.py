# coding:utf-8

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-04-17 15:35:39"

"""
自动绑定配置表
"""
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
        # "setItemText": {
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
    updater = options.get("updater")
    getter = options.get("getter")

    def wrapper(self, value, *args, **kwargs):
        if callable(value):
            # # NOTE get the outter frame state attribute from the widget class
            # frame = inspect.currentframe().f_back
            # parent = frame.f_locals.get('self')

            with Binding.set_trace():
                val = value()

            # NOTE register auto update
            callback = lambda: func(
                self, typ(value()) if typ else value(), *args, **kwargs
            )
            for binding in Binding.TRACE_LIST:
                binding.signal.connect(callback)

            # # NOTE Single binding connect to the updater
            # # TODO only support one binding without other evaluation
            # if updater and getter and len(Binding.TRACE_SET) == 1:
            #     # binding = Binding.TRACE_SET.pop()
            #     updater = getattr(self, updater)
            #     getter = getattr(self, getter)
            #     updater.connect(lambda: binding.set(getter()))

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
