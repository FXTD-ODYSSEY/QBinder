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

# os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"
os.environ['QT_PREFERRED_BINDING'] = 'PySide;PySide2'

import inspect

import QBinder
# from QBinder import Binder, GBinder, QEventHook
import six
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
qt_dict = {"QtWidgets.%s" % n:m for n,m in inspect.getmembers(QtWidgets)}
qt_dict.update({"QtCore.%s" % n:m for n,m in inspect.getmembers(QtCore)})
qt_dict.update({"QtGui.%s" % n:m for n,m in inspect.getmembers(QtGui)})

def byte2str(text):
    # NOTE compat python 2 and 3
    return str(text,encoding = "utf-8") if sys.hexversion >= 0x3000000 else str(text)

def get_method_name(method):
    # NOTE compat Qt 4 and 5
    version = QtCore.qVersion()
    name = ''
    count = False
    if version.startswith('5'):
        name = method.name()
        count = method.parameterCount()
    elif version.startswith('4'):
        name = method.signature()
        name = name.split('(')[0]
        count = method.parameterNames()
    return byte2str(name),count

for name,member in qt_dict.items():
    if not hasattr(member,'staticMetaObject'):
        continue
    meta_obj = getattr(member,'staticMetaObject')
    
    for i in range(meta_obj.methodCount()):
        method = meta_obj.method(i)
        method_name,count = get_method_name(method)
        if count and method.methodType() != QtCore.QMetaMethod.Signal and hasattr(member,method_name):
            HOOKS[name][method_name] = {}
            _HOOKS[name][method_name.lower()] = method_name

    for i in range(meta_obj.propertyCount()):
        property = meta_obj.property(i)
        if not property.hasNotifySignal():
            continue
        property_name = property.name()
        method_name = _HOOKS[name].get("set%s" % property_name.lower())
        data = HOOKS[name].get(method_name)
        if isinstance(data,dict):
            updater,_ = get_method_name(property.notifySignal())
            if updater:
                data.update({
                    "updater" : updater,
                    "property" : property_name
                })
                

path = "%s.json" % os.path.splitext(__file__)[0]
with open(path,'w') as f:
    json.dump(HOOKS,f,indent=4,ensure_ascii=False)
# print(json.dumps(method_dict))
# print(method_dict)

