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

from QBinding import Binder, connect_binder

@connect_binder
class Counter(QtWidgets.QWidget):

    state = Binder()
    state.text = "asd"
    
    def __init__(self):
        super(Counter,self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        
        self.line = QtWidgets.QLineEdit()
        self.line2 = QtWidgets.QLineEdit()

        label = QtWidgets.QLabel()
        plus_button = QtWidgets.QPushButton("+")

        layout.addWidget(self.line)
        layout.addWidget(label)
        layout.addWidget(self.line2)
        layout.addWidget(plus_button)
        
        self.line.setText(lambda: "asd %s" % self.state.text)
        self.line2.setText(lambda:self.state.text)
        label.setText(lambda:self.state.text)
        # self.line.textChanged.connect(self.modify)
        # self.line2.textChanged.connect(self.modify)
        plus_button.clicked.connect(self.changeText)
    
    def changeText(self):
        self.line.setText('bbcc')
        
def main():
    app = QtWidgets.QApplication([])

    counter = Counter()
    counter.show()

    app.exec_()

if __name__ == "__main__":
    main()
