# -*- coding: utf-8 -*-
"""
整合
"""

from __future__ import division
from __future__ import print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-27 16:18:54'

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

from QBinder import Binder
from Qt import QtGui, QtWidgets, QtCore

from lineEditTest import LineEditWidget
from checkBoxTest import CheckBoxWidget
from radioButtonTest import RadioButtonWidget
from comboBoxTest_1 import ComboBoxWidget_1
from listWidgetTest import ListWidgetTest
from comboBoxTest_2 import ComboBoxWidget_2



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    container = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    container.setLayout(layout)

    widget = LineEditWidget()
    layout.addWidget(widget)

    widget = CheckBoxWidget()
    layout.addWidget(widget)

    widget = RadioButtonWidget()
    layout.addWidget(widget)

    widget = ComboBoxWidget_1()
    layout.addWidget(widget)

    widget = ListWidgetTest()
    layout.addWidget(widget)

    widget = ComboBoxWidget_2()
    layout.addWidget(widget)
    
    container.show()

    app.exec_()