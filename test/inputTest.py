# coding:utf-8

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-03-22 22:55:38"

"""

"""

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import os
import sys

from functools import wraps, partial

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from QBinder import Binder


class WidgetTest(QtWidgets.QWidget):
    with Binder() as state:
        state.text = "aasdsd"
    
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.edit = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton("change Text")
        layout.addWidget(self.edit)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.changeText)
        self.edit.setText(lambda: self.state.text)
        self.label.setText(lambda: "message is %s" % self.state.text)

    def changeText(self):
        self.state["text"] = "asd"


def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
