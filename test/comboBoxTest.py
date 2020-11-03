# coding:utf-8

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-03-22 22:55:38"

"""

"""

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


@connect_binder
class ComboTest(QtWidgets.QWidget):

    state = Binder()
    state.text = "asd"
    state.text2 = "asd"
    state.num = 123
    state.enable = True
    state.data_list = Model([state.text2, state.enable])

    def __init__(self):
        super(ComboTest, self).__init__()
        self.initialize()

        print(~self.state)

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton("change enable")
        self.label = QtWidgets.QLabel()
        self.cb = QtWidgets.QCheckBox("disable")
        self.label2 = QtWidgets.QLabel()

        self.combo = QtWidgets.QComboBox()
        self.combo.setModel(self.state.data_list)
        # self.combo.addItem(self.state.text)

        layout.addWidget(self.btn)
        layout.addWidget(self.line)
        layout.addWidget(self.label)
        layout.addWidget(self.cb)
        layout.addWidget(self.combo)
        layout.addWidget(self.label2)

        self.line.setText(lambda: self.state.text2)
        self.label.setText(
            lambda: "{text2} {enable}".format(
                text2=self.state.text2, enable=self.state.enable
            )
        )
        self.label2.setText(lambda: self.state.data_list)
        self.cb.setChecked(lambda: self.state.enable)

        # self.line.textChanged.connect(self.modify)
        self.btn.clicked.connect(self.clickEvent)

    def clickEvent(self):
        self.state.enable = not self.state.enable
        print(self.state.enable)
        self.state.data_list.append(1)
        # self.state.num += 1
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
