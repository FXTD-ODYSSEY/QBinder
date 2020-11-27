# -*- coding: utf-8 -*-
"""
To Create PySide2 white list for PyQt
"""

# from __future__ import division
# from __future__ import print_function
# from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-24 19:35:01"

import os
import json
import inspect
from collections import defaultdict

nestdict = lambda: defaultdict(nestdict)

import PyQt5
import PySide2

from PyQt5 import QtWidgets, QtCore, QtGui
from PySide2 import QtWidgets, QtCore, QtGui

# for name,method in inspect.getmembers(QtWidgets.QWidget):
#     if "event" in name.lower():
#         print(name)
# raise

# func = QtWidgets.QAbstractButton.changeEvent
# sig = inspect.signature(func)
# print(func.__name__)
# print(type(func))
# print(sig.parameters)
# print(sig.parameters.get('event'))
# print(len(sig.parameters))
# sig = inspect.signature(QtWidgets.QApplication.aboutQt)
# print(type(QtWidgets.QApplication.aboutQt))
# print(len(sig.parameters))
# print(str(sig).startswith('()') or str(sig).startswith('self'))
# raise

pyqt_dict = {}
pyside_dict = {}
PYQT_DICT = nestdict()
result_dict = nestdict()

module_list = ["QtWidgets", "QtCore", "QtGui"]
for module in module_list:
    pyqt_dict.update(
        {
            "%s.%s" % (module, n): m
            for n, m in inspect.getmembers(getattr(PyQt5, module))
        }
    )
    pyside_dict.update(
        {
            "%s.%s" % (module, n): m
            for n, m in inspect.getmembers(getattr(PySide2, module))
        }
    )

# print("pyqt_dict",len(pyqt_dict))
# print("pyside_dict",len(pyside_dict))

app = QtWidgets.QApplication([])
for name, member in pyqt_dict.items():
    for method_name, method in inspect.getmembers(member, inspect.isroutine):
        PYQT_DICT[name][method_name] = type(method).__name__

for name, member in pyside_dict.items():
    for method_name, method in inspect.getmembers(member, inspect.isroutine):
        try:
            sig = inspect.signature(method)
        except:
            continue
        param = sig.parameters
        # count =  1 if type(method).__name__ == "method_descriptor" else 0
        if (
            type(method).__name__ == "method_descriptor"
            and len(param) > 1
            and PYQT_DICT[name].get(method_name)
            and not method_name.startswith("__")
            and not param.get('event')
            and not param.get('e')
        ):
            # if type(method).__name__ == "method_descriptor":
            result_dict[name][method_name] = True

path = "%s.json" % os.path.splitext(__file__)[0]
with open(path, "w") as f:
    json.dump(result_dict, f, indent=4, ensure_ascii=False)
