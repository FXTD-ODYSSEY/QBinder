# coding:utf-8

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import os
import sys

from functools import wraps,partial

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..","..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QMVVM

class WidgetTest(QtWidgets.QWidget):

    @QMVVM.store({
        "state": {
            "picked": "",
        },
        "methods": {
            "label.setText":{
                "args":["picked"],
            	"action": lambda a:"Picked %s" %  a,
            },
        },
        "signals":{
            "rb1.toggled":"$updateRB",
            "rb2.toggled":"$updateRB",
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        groupBox = QtWidgets.QGroupBox("Exclusive Radio Buttons")
        self.rb1 = QtWidgets.QRadioButton('One')
        self.rb2 = QtWidgets.QRadioButton('Two')

        h_layout = QtWidgets.QVBoxLayout()
        h_layout.addWidget(self.rb1)
        h_layout.addWidget(self.rb2)
        groupBox.setLayout(h_layout)

        self.label = QtWidgets.QLabel()
        layout.addWidget(groupBox)
        layout.addWidget(self.label)

        # self.label.setText("CheckedNames %s" %  self.state.checkedNames)

        # for rb in groupBox.findChildren(QtWidgets.QRadioButton):
        #     rb.toggled.connect(partial(self.updateRB,rb))

    def updateRB(self,rb,state):
        if state:
            self.state.picked = rb.text()

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
