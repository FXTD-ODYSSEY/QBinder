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

from QBinder import Binder

from Qt import QtGui, QtWidgets, QtCore
from collections import OrderedDict


class ComboBoxWidget_2(QtWidgets.QWidget):

    state = Binder()
    state.selected = ""
    state.options = [
        {"text": "One", "value": "A"},
        {"text": "Two", "value": "B"},
        {"text": "Three", "value": "C"},
    ]

    def __init__(self):
        super(ComboBoxWidget_2, self).__init__()
        self.initialize()
        # print(self.state.options[0].text)

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems([data.get("text") for data in self.state.options])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.combo)
        layout.addWidget(self.label)
        self.label.setText(lambda: "Selected: %s" % self.state.selected)

        self.combo.currentTextChanged.connect(self.update)
        self.update(self.combo.currentText())

    def update(self, text):
        for data in self.state.options:
            if data.get("text") == text:
                self.state.selected = data.get("value")


def main():
    app = QtWidgets.QApplication([])

    widget = ComboBoxWidget_2()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
