# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

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
MODULE = os.path.join(DIR,"..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QMVVM

class Counter(QtWidgets.QWidget):

    @QMVVM.store({
        "state":{
            "text":"123",
        },
        "methods":{
        	# "combo.addItem":{
        	# 	"action": "text"
        	# },
            "line.setText":{
                "bindings": "text",
                "action": "text",
            },
            "label.setText":{
                "bindings": "text",
                "action": "text",
            }
        },
    })
    def __init__(self):
        super(Counter,self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
    
        self.combo = QtWidgets.QComboBox()
        self.combo.addItem(self.state.text)
        self.combo._QMVVM_Bindings = {}

        self.line = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton('123')
        self.label = QtWidgets.QLabel()

        layout.addWidget(self.btn)
        layout.addWidget(self.line)
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        
        self.line.setText(self.state.text)
        self.label.setText(self.state.text)
        # self.line.textChanged.connect(self.modify)
        self.btn.clicked.connect(self.clickEvent)

    def clickEvent(self):
        self.state.text = "566778"
        
    def modify(self,text):
        self.state.text = text
        
def main():
    app = QtWidgets.QApplication([])

    counter = Counter()
    counter.show()

    app.exec_()

if __name__ == "__main__":
    main()
