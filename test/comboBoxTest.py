# coding:utf-8

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""

import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
sys.path.insert(0,repo) if repo not in sys.path else None

import QBinding
from Qt import QtGui, QtWidgets, QtCore

class ComboTest(QtWidgets.QWidget):

    @QBinding.init({
        "ui":"#/../",
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
    })
    def __init__(self):
        super(ComboTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItem(self.state.text)
        self.combo._QBinding_Bindings = {}

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

        self.line.setText(lambda:self.state.text2)
        self.label.setText(lambda:"{text2} {enable}".format(text2=self.state.text2,enable=self.state.enable))
        self.label2.setText(lambda:self.state.data_list)
        self.cb.setChecked(lambda:self.state.enable)

        # self.line.textChanged.connect(self.modify)
        self.btn.clicked.connect(self.clickEvent)

    def clickEvent(self):
        self.state.enable = not self.state.enable
        # self.state.num += 1
        # self.state.data_list = [1234,1]
        # self.state.data_list.append(1)
        # self.state.data_list.append(2)
        # print self.state.data_list
        # print self.state.text2
        # self.state.text2 = "abxcs"

        # print("data_list",self.state.data_list)
        # self.state.data_list[1][4] = {123:"4444" }

def main():
    app = QtWidgets.QApplication([])

    counter = ComboTest()
    counter.show()

    app.exec_()


if __name__ == "__main__":
    main()
