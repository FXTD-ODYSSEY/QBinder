# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 14:34:10"


import os
import sys
import inspect
import traceback

from functools import wraps

DIR = os.path.dirname(__file__)
import sys

MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import os
import sys
from QBinding import Binder, connect_binder

@connect_binder
class Counter(QtWidgets.QWidget):

    state = Binder()
    state.count = 0
    state.count2 = 6

    def __init__(self):
        super(Counter, self).__init__()
        self.count = 4
        self.count3 = 15
        self.initialize()
        
        print(self.state.count)

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.label = QtWidgets.QLabel()

        plus_button = QtWidgets.QPushButton("count ++")
        minus_button = QtWidgets.QPushButton("count --")

        label2 = QtWidgets.QLabel()
        label3 = QtWidgets.QLabel()
        label4 = QtWidgets.QLabel()

        plus_button2 = QtWidgets.QPushButton("count2 ++")
        minus_button2 = QtWidgets.QPushButton("count2 --")
        label5 = QtWidgets.QLabel()

        self.label.setText(lambda:str(self.state.count))
        label2.setText("<center>%s %s</center>" % (self.count, self.state.count))
        label3.setText("<center>%s</center>" % self.count)
        label4.setText(self.calculate(self.count, self.count3))
        label5.setText(str(self.state.count2))

        layout.addWidget(self.label)
        layout.addWidget(plus_button)
        layout.addWidget(minus_button)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(plus_button2)
        layout.addWidget(minus_button2)
        layout.addWidget(label5)

        plus_button.clicked.connect(self.add)
        minus_button.clicked.connect(self.subtract)
        plus_button2.clicked.connect(self.add2)
        minus_button2.clicked.connect(self.subtract2)

    def add(self):
        self.state.count += 1
        print(self.state.count)

    def subtract(self):
        print(self.state.count)
        self.state.count -= 1

    def add2(self):
        self.state.count2 += 1

    def subtract2(self):
        self.state.count2 -= 1

    def calculate(self, a, b):
        return str(a * b + self.state.count)

    def mul(self):
        return str(self.state.count2 + self.state.count)


def main():
    app = QtWidgets.QApplication([])

    counter = Counter()
    counter.show()
    app.exec_()


if __name__ == "__main__":
    main()
