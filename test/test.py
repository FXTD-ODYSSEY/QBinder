# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-30 22:20:47"


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

import inspect
from QBinder import Binder, QEventHook

import Qt

print("__binding__", Qt.__binding__)
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

event_hook = QEventHook()

app = QtWidgets.QApplication([])

label = QtWidgets.QLabel("display")
label.show()

# NOTE 扩展 label 为可点击组件

# NOTE 可不接受参数或者接受 event 参数
label >> event_hook("MouseButtonPress", lambda: sys.exit())

app.exec_()