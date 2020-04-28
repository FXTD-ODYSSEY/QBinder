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
from collections import OrderedDict
DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..","..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QMVVM

class WidgetTest(QtWidgets.QWidget):

    @QMVVM.store({
        "state": {
            "selected": "",
            "options": OrderedDict([
                ('One', 'A'),
                ('Two', 'B'),
                ('Three', 'C'),
            ]),
        },
        "methods": {
            "label.setText":{
                "args":["selected"],
            	"action": lambda a:"Selected: %s" %  a,
            },
        },
        "signals":{
            "combo.currentTextChanged":"$update"
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems([text for text in self.state.options])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.combo)
        layout.addWidget(self.label)

        # self.combo.currentTextChanged.connect(lambda *args:self.update(self.combo,*args))
        self.state.selected =  self.state.options.get(self.combo.currentText())
        
    def update(self,widget,text):
        self.state.selected = self.state.options.get(text)

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()



if __name__ == "__main__":
    main()
