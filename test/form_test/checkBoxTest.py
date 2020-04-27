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
            "checkedNames": [],
        },
        "methods": {
            "label.setText":{
                "args":["checkedNames"],
            	"action": lambda a:"CheckedNames %s" %  a,
            },
        },
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        groupBox = QtWidgets.QGroupBox("Exclusive Check Buttons")
        groupBox.setChecked(True)
        self.cb1 = QtWidgets.QCheckBox('Jack')
        self.cb2 = QtWidgets.QCheckBox('John')
        self.cb3 = QtWidgets.QCheckBox('Mike')

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.cb1)
        h_layout.addWidget(self.cb2)
        h_layout.addWidget(self.cb3)
        groupBox.setLayout(h_layout)

        self.label = QtWidgets.QLabel()
        layout.addWidget(groupBox)
        layout.addWidget(self.label)

        self.cb1.stateChanged.connect(partial(self.updateCB,self.cb1))
        self.cb2.stateChanged.connect(partial(self.updateCB,self.cb2))
        self.cb3.stateChanged.connect(partial(self.updateCB,self.cb3))

    def updateCB(self,widget,state):
        method = self.state.checkedNames.append if state else self.state.checkedNames.remove
        method(widget.text())
            

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()



if __name__ == "__main__":
    main()
