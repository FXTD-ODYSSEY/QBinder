# coding:utf-8
from __future__ import print_function,division
__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""
import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
sys.path.insert(0,repo) if repo not in sys.path else None

from QBinding import Binder, connect_binder 
from PySide2 import QtGui, QtWidgets, QtCore
from collections import OrderedDict

@connect_binder
class WidgetTest(QtWidgets.QWidget):
    
    state = Binder()
    state.selected = ""
    state.option_A = "A"
    state.option_B = "B"
    state.option_C = "C"
    state.item_list = [state.selected,state.option_A,state.option_B,state.option_C]
        
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        print(self.state.selected)

        self.combo = QtWidgets.QComboBox()
        # self.combo.addItems(self.state.item_list)
        self.combo.addItems(['A','B','C'])

        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton('click')
        layout.addWidget(self.combo)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.testComputed)
        self.combo.currentTextChanged.connect(self.update)
        self.state.selected = self.combo.currentText()
        print(self.state.item_list)

        self.label.setText(lambda:"selected {selected}".format(selected=self.state.selected))
    
    def testComputed(self):
        self.state.selected = 'AAA'

    def update(self,text):
        self.state.selected = text

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
