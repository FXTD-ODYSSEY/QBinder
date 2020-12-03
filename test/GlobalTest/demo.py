# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-03 15:55:15"

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

from QBinder import Binder, GBinder
from Qt import QtGui, QtWidgets, QtCore

import data

state = GBinder()
state.msg = "msg"
# state.text = 'text'


class InputTest(QtWidgets.QWidget):
    def __init__(self):
        super(InputTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.line)
        layout.addWidget(self.label)

        self.line.setText(lambda: state.text)
        self.label.setText(lambda: state.msg)


class InputTest2(QtWidgets.QWidget):
    def __init__(self):
        super(InputTest2, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.line)
        layout.addWidget(self.label)

        self.line.setText(lambda: state.msg)
        self.label.setText(lambda: state.text)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    state.input_ui = InputTest2()
    state.input_ui.show()

    widget = InputTest()
    widget.show()
    sys.exit(app.exec_())