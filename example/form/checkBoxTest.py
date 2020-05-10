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

class WidgetTest(QtWidgets.QWidget):

    @QBinding.store({
        "state": {
            "checkedNames": [],
        },
        # "signals": {
        #     "cb1.stateChanged":"updateCB",
        #     "cb2.stateChanged":"updateCB",
        #     "cb3.stateChanged":"updateCB",
        # }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()
        self.state.OPTIONS["signals"] = {
            "cb1.stateChanged":"updateCB",
            "cb2.stateChanged":"updateCB",
            "cb3.stateChanged":"updateCB",
        }
        
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

        self.label.setText(lambda:"CheckedNames: %s" % self.state.checkedNames)
        # self.cb1.stateChanged.connect(partial(self.updateCB,self.cb1))
        # self.cb2.stateChanged.connect(partial(self.updateCB,self.cb2))
        # self.cb3.stateChanged.connect(partial(self.updateCB,self.cb3))

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
