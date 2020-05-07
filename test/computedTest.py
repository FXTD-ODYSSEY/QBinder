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

import QBinding
from Qt import QtGui, QtWidgets, QtCore
from collections import OrderedDict

class WidgetTest(QtWidgets.QWidget):

    @QBinding.store({
        "state": {
            "selected": "",
            "option_A": "A",
            "option_B": "B",
            "option_C": "C",
        },
        "computed":{
            # "item_list": ["${selected}","${option_B}","${option_C}",True],
            "item_list":OrderedDict([
                ('One', "${option_A}"),
                ('${selected}', "${option_B}"),
                ('A','AAA'),
                ('Three', "${option_C}"),
            ]),
        },
        "signals":{
            "combo.currentTextChanged":"$update",
            # "combo.currentTextChanged":"selected",
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.combo = QtWidgets.QComboBox()
        # self.combo.addItems(self.state.item_list)
        self.combo.addItems(['A','B','C'])

        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton('click')
        layout.addWidget(self.combo)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.testComputed)
        # self.combo.currentTextChanged.connect(lambda *args:self.update(self.combo,*args))
        self.state.selected = self.combo.currentText()
        print(self.state.item_list)

        self.label.setText(lambda:"selected {selected}".format(selected=self.state.selected))
    
    # def getData(self):
    #     print 1,self.item_list
    #     self.item_list.append('asd')
    #     self.item_list.insert(1,'d')
    #     print 2,self.item_list
    #     self.state.option_B = "BBC"
    #     print 3,self.item_list
    #     self.item_list[0] += 'aA'
    #     # print self.item_list[0].replace('A','sds')
    #     # print self.item_list[0].append('A')
    #     print self.item_list
    #     print self.item_list[0]
    #     print str(self.item_list[0])
    #     # print self.item_list[0].replace
    #     # print self.item_list

    def testComputed(self):
        self.state.option_A = 'AAA'
        print(self.state.item_list)
        # print self.state.item_list
        # # self.state.item_list[0].append(1)
        # self.state.selected += '2'
        # print self.state.item_list

    def update(self,widget,text):
        self.state.selected = text

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()
