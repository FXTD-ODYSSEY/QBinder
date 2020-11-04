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

from QBinding import init_binder
from Qt import QtGui, QtWidgets, QtCore
from functools import partial


class WidgetTest(QtWidgets.QWidget):

    with init_binder() as state:
        state.checkedNames = []

    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        groupBox = QtWidgets.QGroupBox("Exclusive Check Buttons")
        groupBox.setChecked(True)
        self.cb1 = QtWidgets.QCheckBox("Jack")
        self.cb2 = QtWidgets.QCheckBox("John")
        self.cb3 = QtWidgets.QCheckBox("Mike")

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.cb1)
        h_layout.addWidget(self.cb2)
        h_layout.addWidget(self.cb3)
        groupBox.setLayout(h_layout)

        self.label = QtWidgets.QLabel()
        layout.addWidget(groupBox)
        layout.addWidget(self.label)

        self.label.setText(lambda: "CheckedNames: %s" % self.state.checkedNames)
        for cb in groupBox.findChildren(QtWidgets.QCheckBox):
            cb.stateChanged.connect(partial(self.updateCB, cb))

    def updateCB(self, widget, state):
        method = (
            self.state.checkedNames.append if state else self.state.checkedNames.remove
        )
        method(widget.text())


def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
