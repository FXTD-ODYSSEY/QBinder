# -*- coding: utf-8 -*-
"""
metamethod get all the paramter method
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-08 16:05:07"

import os
import sys

repo = (lambda f: lambda p=__file__: f(f, p))(
    lambda f, p: p
    if [
        d
        for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p))
        if d == ".git"
    ]
    else None
    if os.path.dirname(p) == p
    else f(f, os.path.dirname(p))
)()
sys.path.insert(0, repo) if repo not in sys.path else None

os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"
# os.environ['QT_PREFERRED_BINDING'] = 'PySide;PySide2'

import inspect

from QBinder import Binder, GBinder, QEventHook
from QBinder.handler import ItemMixin, Set

from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi

# meta_obj = QtWidgets.QWidget.staticMetaObject
from collections import defaultdict
import json
nested_dict = lambda: defaultdict(nested_dict)

HOOKS = nested_dict()
_HOOKS = nested_dict()
method_dict = nested_dict()
method_comp = defaultdict(list)
qt_dict = inspect.getmembers(QtWidgets)
qt_dict.extend(inspect.getmembers(QtCore))
qt_dict.extend(inspect.getmembers(QtGui))

for name,member in qt_dict:
    if not hasattr(member,'staticMetaObject'):
        continue
    meta_obj = getattr(member,'staticMetaObject')
        
    for i in range(meta_obj.methodCount()):
        method = meta_obj.method(i)
        method_name = str(method.name())
        if method.parameterCount() and method.methodType() != QtCore.QMetaMethod.Signal and not method_name.startswith('_') :
            if hasattr(member,method_name):
                HOOKS[name][method_name] = {}
                _HOOKS[name][method_name.lower()] = method_name
            # for m in method_comp[method_name]:
            #     if m == method:
            #         break
            # else:
            #     method_comp[method_name].append(method)
            #     if not method_dict[name][str(method_name)] :
            #         method_dict[name][str(method_name)] = []
            #     method_dict[name][str(method_name)].append(str(method.methodSignature()))

    for i in range(meta_obj.propertyCount()):
        property = meta_obj.property(i)
        if not property.hasNotifySignal():
            continue
        property_name = property.name()
        setter = "set%s" % property_name
        method_name = _HOOKS[name].get(setter)
        data = HOOKS[name].get(method_name)
        if data is not None:
            updater = str(property.notifySignal().name())
            if updater:
                data.update({
                    "updater" : updater,
                    "getter" : property_name
                })
                

path = "%s.json" % os.path.splitext(__file__)[0]
with open(path,'w') as f:
    json.dump(HOOKS,f,indent=4,ensure_ascii=False)
# print(json.dumps(method_dict))
# print(method_dict)

