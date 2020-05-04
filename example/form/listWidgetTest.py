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

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..","..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QBinding

class WidgetTest(QtWidgets.QWidget):

    @QBinding.store({
        "state": {
            "selected": [],
        },
        "methods": {
            "label.setText":{
                # "args":["selected"],
            	"action":"`Selected: ${selected}`",
            },
        },
        "signals":{
            "listWidget.itemSelectionChanged":"$update"
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.listWidget.addItems(['A','B','C'])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.label)

    def update(self,widget):
        self.state.selected = [item.text() for item in widget.selectedItems()]

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()



if __name__ == "__main__":
    main()
