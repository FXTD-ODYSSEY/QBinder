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

from functools import wraps

DIR = os.path.dirname(__file__)
import sys

MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from QBinder import Binder


class Counter(QtWidgets.QWidget):

    state = Binder()
    state.data = [1, 2, 3]

    def __init__(self):
        super(Counter, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        label = QtWidgets.QLabel()
        plus_button = QtWidgets.QPushButton("+")

        layout.addWidget(label)
        layout.addWidget(plus_button)

        label.setText(lambda: "Label %s" % self.state.data)
        plus_button.clicked.connect(self.changeData)

    def changeData(self):
        self.state.data.append(3)
        print(self.state.data)


def main():
    app = QtWidgets.QApplication([])

    counter = Counter()
    counter.show()

    app.exec_()


if __name__ == "__main__":
    main()
