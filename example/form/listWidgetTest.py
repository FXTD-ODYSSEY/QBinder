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
os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"

from QBinder import Binder
from Qt import QtGui, QtWidgets, QtCore
from functools import partial


class ListWidgetTest(QtWidgets.QWidget):

    state = Binder()
    state.selected = []

    def __init__(self):
        super(ListWidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.listWidget.addItems(["A", "B", "C"])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.label)

        self.label.setText(lambda: "Selected: %s" % self.state.selected)

        self.listWidget.itemSelectionChanged.connect(self.update)

    def update(self):
        self.state.selected = [item.text() for item in self.listWidget.selectedItems()]


def main():
    app = QtWidgets.QApplication([])

    widget = ListWidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
