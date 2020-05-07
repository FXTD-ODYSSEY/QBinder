# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-29 17:07:57'

"""

"""

import os
import sys

from functools import wraps,partial
from collections import OrderedDict
DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QBinding
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class WidgetTest(QtWidgets.QWidget):

    @QBinding.store({
        "state": {
            "selected": "",
            "option_A": "A",
            "option_B": "B",
            "option_C": "C",
        },
        "computed":{
            "item_list": [
                "${selected}",
                "${option_A}",
                "${option_B}",
                "${option_C}"
            ],
            "*item_model": [
                ["${option_A}","${option_B}"],
                "${option_B}",
                "${option_C}",
                ["12"],
                ["asd","1234"]
            ],
        },
        "signals":{
            "line.textChanged":"option_B",
            # "combo.currentTextChanged":"selected",
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        layout.addWidget(self.line)
        
        #ALL OF OUR VIEWS
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()

        # print ("dynamicPropertyNames",comboBox.dynamicPropertyNames())
        layout.addWidget(comboBox)

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        red   = QtGui.QColor(255,0,0)
        green = QtGui.QColor(0,255,0)
        blue  = QtGui.QColor(0,0,255)

        item_list = [red, "green", "blue"]
        # TODO configurate the model
        # self.model = StateModel(self.state.item_list)

        # print (self.state.item_list)
        self.state.selected = "selected"
        # print (self.state.item_list)

        # print ("item_model",self.state.item_model)

        listView.setModel(self.state.item_model)
        comboBox.setModel(self.state.item_model)
        tableView.setModel(self.state.item_model)
        treeView.setModel(self.state.item_model)

        button = QtWidgets.QPushButton("change")
        button.clicked.connect(self.changeOrder)
        layout.addWidget(button)
        button = QtWidgets.QPushButton("change2")
        button.clicked.connect(self.addComboBox)
        layout.addWidget(button)
        
        self.text = '123'
        self.label = QtWidgets.QLabel("label")
        self.label.setText(lambda: "%s %s" % (self.state.option_B,self.text))
        layout.addWidget(self.label)

    def addComboBox(self):
        print (self.state.item_list)
        self.state.option_B = "BBB"
        print (self.state.item_list)

    def changeOrder(self):
        self.text = "asd"

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()

    widget.show()
    
    sys.exit(app.exec_())