# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-10-22 15:44:39"

from QBinder import BinderTemplate
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)
class WidgetBinder(BinderTemplate):
    def __init__(self):
        self.text1 = ""
        self.text2 = ""


class WidgetTest(QtWidgets.QWidget):

    state = WidgetBinder()

    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def callback(self):
        print("callback\ntext1: %s\ntext2: %s" % (self.state.text1, self.state.text2))
        return bool(self.state.text1 and self.state.text2)
        return bool(self.state.text1) and bool(self.state.text2)

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.edit1 = QtWidgets.QLineEdit()
        self.edit2 = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("test")

        self.edit1.setText(lambda: self.state.text1)
        self.edit2.setText(lambda: self.state.text2)
        self.button.setEnabled(lambda: bool(self.state.text1 or self.state.text2))

        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.button)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()

