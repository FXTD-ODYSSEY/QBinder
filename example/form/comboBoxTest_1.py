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

    @QBinding.init({
        "state": {
            "selected": "",
        },
        "signals":{
            "combo.currentTextChanged":"update",
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(['A','B','C'])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.combo)
        layout.addWidget(self.label)

        self.label.setText(lambda:"Selected: %s" % self.state.selected)
        self.state.selected = self.combo.currentText()

    def update(self,widget,text):
        self.state.selected = text

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()



if __name__ == "__main__":
    main()
