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

from QBinding import BinderBase,init_binder

# with init_binder(True) as state:
#     state.message = "asd"
state = BinderBase()
state.text = "aasdsd"
        
class WidgetTest(QtWidgets.QWidget):


    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()
        print(state.text)
        print(type(state.text))
        print(type(state["text"]))
        
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
        self.edit.setText(lambda: state.text)
        self.label.setText(lambda: "message is %s" % state.text)

    def changeText(self):
        state.message = "asd"

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
