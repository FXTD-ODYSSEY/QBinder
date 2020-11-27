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
from QBinder.handler import Set
from Qt import QtGui, QtWidgets, QtCore


class ComboBoxWidget_1(QtWidgets.QWidget):

    state = Binder()
    with state('dumper','combo_test1'):
        state.selected = ""

    def __init__(self):
        super(ComboBoxWidget_1, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["A", "B", "C"])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.combo)
        layout.addWidget(self.label)

        self.label.setText(lambda: "Selected: %s" % self.state.selected)
        self.combo.setCurrentText(lambda: self.state.selected)
        # self.combo.currentTextChanged.connect(lambda text:self.state.selected >> Set(text))


def main():
    app = QtWidgets.QApplication([])

    widget = ComboBoxWidget_1()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
