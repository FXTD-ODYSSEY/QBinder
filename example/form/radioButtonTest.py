# coding:utf-8

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""
import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
sys.path.insert(0,repo) if repo not in sys.path else None

import QBinding
from Qt import QtGui, QtWidgets, QtCore

from functools import partial

class WidgetTest(QtWidgets.QWidget):

    @QBinding.init({
        "state": {
            "picked": "",
        },
        "signals":{
            "rb1.toggled":"updateRB",
            "rb2.toggled":"updateRB",
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

        self.label.setText(lambda:"CheckedNames %s" %  self.state.picked)

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
