# coding:utf-8

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import os
import sys

from functools import wraps,partial

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QMVVM

class WidgetTest(QtWidgets.QWidget):

    @QMVVM.store({
        "state": {
            "message": "",
        },
        "methods": {
            "label.setText":{
                # "args":["message"],
                "action": "message",
            },
            "edit.setText":"message",
        },
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.edit = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton('change Text')
        layout.addWidget(self.edit)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.button.clicked.connect(self.changeText)
        # self.edit.setText.setText(self.state.message)
        # self.label.setText.setText("message is %s" % self.state.message)
        
    def changeText(self):
        self.label.setText("asd")
        # self.state.message = "asd"
        print self.state.message


def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()



if __name__ == "__main__":
    main()
