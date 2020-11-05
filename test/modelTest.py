# coding:utf-8
from __future__ import division, print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-04-29 17:07:57"

"""

"""

import os
import sys

from functools import wraps, partial
from collections import OrderedDict

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from QBinder import Binder, Model
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui


class InputTest(QtWidgets.QWidget):
    state = Binder()
    state.text = "abc"

    def __init__(self):
        super(InputTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.line)
        layout.addWidget(self.label)

        self.line.setText(lambda: self.state.text)
        self.label.setText(lambda: self.state.text)


class WidgetTest(QtWidgets.QWidget):
    # state = Binder()
    # state.selected = ""
    # state.option_A = 123.0
    # state.option_B = "B"
    # state.option_C = "C"
    # state.item_list = [
    #     state["selected"],
    #     state["option_A"],
    #     state["option_B"],
    #     state["option_C"],
    # ]
    # state.item_model = Model(
    #     [
    #         [[state["option_A"], state["option_B"]], "1"],
    #         [state["option_A"], state["option_B"]],
    #         state["option_B"],
    #         state["option_C"],
    #         [None, "asd", None, 123],
    #         ["asd", "1234"],
    #     ]
    # )
    with Binder() as state:
        state.selected = ""
        state.option_A = 123.0
        state.option_B = "B"
        state.option_C = "C"
        state.item_list = [
            state.selected,
            state.option_A,
            state.option_B,
            state.option_C,
        ]
        state.item_model = Model(
            [
                [[state.option_A, state.option_B], "1"],
                [state.option_A, state.option_B],
                state.option_B,
                state.option_C,
                [None, "asd", None, 123],
                ["asd", "1234"],
            ]
        )

    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.input = InputTest()
        layout.addWidget(self.input)
        self.input.label.setText(lambda: "%s test" % self.state.option_B)

        # print (self.state.toJson())

        self.line = QtWidgets.QLineEdit()
        # print(self.line.STATE)
        layout.addWidget(self.line)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)

        self.line.setText(lambda: self.state.option_B)
        self.label.setText(lambda: self.state.option_B)

        # ALL OF OUR VIEWS
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()

        # print ("dynamicPropertyNames",comboBox.dynamicPropertyNames())
        layout.addWidget(comboBox)

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        # red = QtGui.QColor(255, 0, 0)
        # green = QtGui.QColor(0, 255, 0)
        # blue = QtGui.QColor(0, 0, 255)
        # item_list = [red, "green", "blue"]

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

        self.text = "123"
        self.label = QtWidgets.QLabel("label")
        self.label.setText(lambda: "%s %s" % (self.state.option_B, self.text))
        layout.addWidget(self.label)

    def addComboBox(self):
        print(self.state.item_list)
        self.state.option_B = 123
        val = self.state.item_list[2]
        print(val + "1")

    def changeOrder(self):
        self.text = "asd"


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()

    widget.show()

    sys.exit(app.exec_())