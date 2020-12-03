import os
import sys

repo = (lambda f: lambda p=__file__: f(f, p))(
    lambda f, p: p
    if [
        d
        for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p))
        if d == ".github"
    ]
    else None
    if os.path.dirname(p) == p
    else f(f, os.path.dirname(p))
)()
sys.path.insert(0, repo) if repo not in sys.path else None

os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"
# os.environ["QT_PREFERRED_BINDING"] = "PySide;PySide2"

import json
import inspect
from collections import defaultdict
import QBinder

import Qt

print(Qt.__binding__)
from Qt import QtWidgets

meta = QtWidgets.QApplication.staticMetaObject
method_list = defaultdict(list)

# while meta:
#     for i in range(meta.methodCount()):
#         method = meta.method(i)
#         method_list[meta.className()].append(method.signature())
#     meta = meta.superClass()

# app = QtWidgets.QApplication([])
app = QtWidgets.QApplication
func = app.postEvent
func = app.setStyleSheet
func = app.wheelScrollLines
print(func.__name__)
# print (dir(func))
print(type(func))

data = {}
for name, member in inspect.getmembers(app):
    # text += "%s %s \n" % ( name , type(member).__name__ )
    # print(name,type(member))
    # data[name] = type(member).__name__
    data[name] = inspect.isbuiltin(member)

path = "%s.json" % os.path.splitext(__file__)[0]

with open(path, "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


# setStyleSheet
# PySide  <type 'method_descriptor'>
# PyQt4   <type 'builtin_function_or_method'>
# PySide2 <class 'method_descriptor'>
# PyQt5   <class 'builtin_function_or_method'>

# postEvent
# PySide  <type 'builtin_function_or_method'>
# PyQt4   <type 'builtin_function_or_method'>
# PySide2 <class 'builtin_function_or_method'>
# PyQt5   <class 'builtin_function_or_method'>