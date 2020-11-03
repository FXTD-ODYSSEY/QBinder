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

from QBinding import Binder, connect_binder, Model
from Qt import QtGui, QtWidgets, QtCore

from data import GlobalData

class InputTest(QtWidgets.QWidget,GlobalData):
    # gstate = GlobalData()

    def __init__(self):
        super(InputTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.line)
        layout.addWidget(self.label)

        print(self.gstate.text)
        print(type(self.gstate["text"]))
        self.line.setText(lambda: self.gstate.text)
        self.label.setText(lambda: self.gstate.text)


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    widget = InputTest()
    widget.show()
    sys.exit(app.exec_())