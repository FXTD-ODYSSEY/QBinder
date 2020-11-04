# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-03 15:55:15'

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

from QBinding import BinderBase,  init_binder
from Qt import QtGui, QtWidgets, QtCore

import data

with init_binder(True) as gstate:
    gstate.text = '12'

class InputTest(QtWidgets.QWidget):

    def __init__(self):
        super(InputTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.line)
        layout.addWidget(self.label)

        self.line.setText(lambda: gstate.msg)
        self.label.setText(lambda: gstate.text)
        
        
class InputTest2(QtWidgets.QWidget):

    def __init__(self):
        super(InputTest2, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.line)
        layout.addWidget(self.label)

        self.line.setText(lambda: gstate.text)
        self.label.setText(lambda: gstate.msg)


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    widget = InputTest()
    widget.show()
    widget2 = InputTest2()
    widget2.show()
    sys.exit(app.exec_())