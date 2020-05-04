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
import inspect
import traceback
import dis
import pdb
from optparse import OptionParser

from functools import wraps

DIR = os.path.dirname(__file__)
import sys
MODULE = os.path.join(DIR,"..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QBinding
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import os
import sys
import QBinding

class Counter(QtWidgets.QWidget):
    '''
        # 1234
        self.test
    '''
    @QBinding.store({
        "state":{
            "count":0,
            "count2":6,
        },
        "bindings":{
            "count":{
                "label.setText":"str",
                "@label3.setText":lambda count: "<center>%s</center>" % count,
            },
        },
        "methods":{
            "@label2.setText":{
                "args":["$count","count"],
                "action":lambda a,b: "<center>%s %s</center>"%(a,b),
            },
            "@label4.setText":{
                "args":["$count","count2"],
                "action":"$calculate",
            },
            "@label5.setText":{
                "args":["count2"],
                "action":lambda a :str(a),
            },
        },
    })
    def __init__(self):
        super(Counter,self).__init__()
        self.count = 4
        self.count3 = 15
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
    
        self.label = QtWidgets.QLabel()

        plus_button = QtWidgets.QPushButton("count ++")
        minus_button = QtWidgets.QPushButton("count --")

        label2 = QtWidgets.QLabel()
        label3 = QtWidgets.QLabel()
        label4 = QtWidgets.QLabel()

        plus_button2 = QtWidgets.QPushButton("count2 ++")
        minus_button2 = QtWidgets.QPushButton("count2 --")
        label5 = QtWidgets.QLabel()

        self.label.setText(str(self.state.count))
        label2.setText("<center>%s %s</center>"%(self.count,self.state.count))
        label3.setText("<center>%s</center>" % self.count)
        label4.setText(self.calculate(self.count,self.count3))
        label5.setText(str(self.state.count2))

        layout.addWidget(self.label)
        layout.addWidget(plus_button)
        layout.addWidget(minus_button)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(plus_button2)
        layout.addWidget(minus_button2)
        layout.addWidget(label5)
        
        plus_button.clicked.connect(self.add)
        minus_button.clicked.connect(self.subtract)
        plus_button2.clicked.connect(self.add2)
        minus_button2.clicked.connect(self.subtract2)

        # print inspect.getmembers(OptionParser, predicate=inspect.ismethod)
        # print inspect.getmembers(OptionParser, predicate=inspect.ismethod)
        # print inspect.getmembers(OptionParser, predicate=inspect.ismethod)
        # print inspect.getmembers(OptionParser, predicate=inspect.ismethod)

    def add(self):
        self.state.count += 1

    def subtract(self):
        self.state.count -= 1

    def add2(self):
        self.state.count2 += 1

    def subtract2(self):
        self.state.count2 -= 1

    def calculate(self,a,b):
        return str(a * b + self.state.count)
    
    def mul(self):
        return str(self.state.count2 + self.state.count)

def main():
    app = QtWidgets.QApplication([])

    counter = Counter()
    counter.show()

    app.exec_()

if __name__ == "__main__":
    main()
