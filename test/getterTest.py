# coding:utf-8

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-03-22 22:55:38"

"""

"""



import os
import sys

DIR = os.path.dirname(__file__)
import sys

MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from QBinder import Binder , Binding
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class TestOP(object):
    def __rrshift__(self,val):
        print('__rrshift__',Binding._inst_)
        return val

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
        self.state.data >> TestOP()

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
