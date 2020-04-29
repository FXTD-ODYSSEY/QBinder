# coding:utf-8
from __future__ import print_function

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

import QMVVM
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class WidgetTest(QtWidgets.QWidget):

    @QMVVM.store({
        "state": {
            "selected": "",
            "option_A": "A",
            "option_B": "B",
            "option_C": "C",
        },
        "computed":{
            "*item_list": ["${selected}","${option_B}","${option_C}"],
        },
        # "methods": {
        #     "label.setText":{
        #         # "bindings":["item_list"],
        #         # "args":["selected"],
        #     	# "action": lambda a:"Selected: %s" %  a,
        #     	"action":"`selected ${item_list}`",
        #     },
        # },
        # "signals":{
        #     "combo.currentTextChanged":"$update",
        #     # "combo.currentTextChanged":"selected",
        # }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        #ALL OF OUR VIEWS
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()
        layout.addWidget(comboBox)

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        red   = QtGui.QColor(255,0,0)
        green = QtGui.QColor(0,255,0)
        blue  = QtGui.QColor(0,0,255)

        rowCount = 4
        columnCount = 6

        item_list = [red, "green", "blue"]
        self.model = item_list
        
        # listView.setModel(self.model)
        # comboBox.setModel(self.model)
        # tableView.setModel(self.model)
        # treeView.setModel(self.model)

        button = QtWidgets.QPushButton("change")
        button.clicked.connect(self.changeOrder)
        layout.addWidget(button)
        button = QtWidgets.QPushButton("change2")
        button.clicked.connect(partial(self.addComboBox,comboBox))
        layout.addWidget(button)

        # self.model.dataChanged.connect(self.modifyData)

    def modifyData(self,topLeft,bottomRight,roles):
        pass
        # self.model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        # print ("modifyData",topLeft,bottomRight,roles)
        # print ("topLeft",topLeft.row())
        # print ("bottomRight",bottomRight.row())
        # model = topLeft.model()
        # print (model.stringList())
        
    def addComboBox(self,comboBox):
        comboBox.addItem("asdasd")
        
    def changeOrder(self):
        self.model.setData([])
        self.model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()


    widget.show()
    
    sys.exit(app.exec_())