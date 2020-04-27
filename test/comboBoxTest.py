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

from functools import wraps

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QMVVM

class ComboTest(QtWidgets.QWidget):

    @QMVVM.store({
        "ui":r"",
        "state": {
            "text": "123",
            "text2": "1234",
            "num": 123,
            "enable": True,
            "data_list": {
                1:{2:'a'},
                2:["b"],
                3:"c",
            },
            # "data_list": ["${enable}",""],
        },
        "methods": {
            # "combo.addItem":{
            # 	"action": "text"
            # },
            "line.setText": "text",
            "label.setText": {
                "args": ["text2", "enable"],
                "action": lambda a, b: "%s %s" % (a, b),
            },
            "label2.setText": {
                # "action": "$modifyTest",
                "action": "data_list",
            },
            "cb.setChecked": {
                # "bindings": "text2",
                "action": "enable",
            }
        },
    })
    def __init__(self):
        super(ComboTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItem(self.state.text)
        self.combo._QMVVM_Bindings = {}

        self.line = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton('change enable')
        self.label = QtWidgets.QLabel()
        self.cb = QtWidgets.QCheckBox('disable')
        self.label2 = QtWidgets.QLabel()

        layout.addWidget(self.btn)
        layout.addWidget(self.line)
        layout.addWidget(self.label)
        layout.addWidget(self.cb)
        layout.addWidget(self.combo)
        layout.addWidget(self.label2)

        # self.line.setText(self.state.text)
        # self.label.setText(self.state.enable)
        # self.cb.setChecked(self.state.enable)

        # self.line.textChanged.connect(self.modify)
        self.btn.clicked.connect(self.clickEvent)

    def clickEvent(self):
        # self.state.enable = not self.state.enable
        # self.state.num += 1
        # self.state.data_list = [1234,1]
        # self.state.data_list.append(1)
        # self.state.data_list.append(2)
        # print self.state.data_list
        self.state.data_list[1][4] = {123:"4444" }
        # print self.state.text2
        # self.state.text2 = "abxcs"

    def modifyTest(self):
        return "%s %s %s" % (self.state.text2, self.state.text, self.state.num+1)

    def modify(self, text):
        self.state.text = text


def main():
    app = QtWidgets.QApplication([])

    counter = ComboTest()
    counter.show()

    app.exec_()


if __name__ == "__main__":
    main()
