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
        state.selected = []

    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()
        print(self.state('dump'))
        dispatcher = self.state('dispatcher')
        print(dispatcher)
        
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

        self.listWidget.itemSelectionChanged.connect(
            partial(self.update, self.listWidget)
        )

    def update(self, widget):
        self.state.selected = [item.text() for item in widget.selectedItems()]


def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
