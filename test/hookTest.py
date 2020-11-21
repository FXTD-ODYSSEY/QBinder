# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-11 13:49:53'


import os
import sys

from functools import wraps, partial

os.environ['QT_PREFERRED_BINDING'] = 'PyQt4;PySide2'
# os.environ['QT_PREFERRED_BINDING'] = 'PyQt4;PyQt5'

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)


from QBinder import Binder,QEventHook


from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

event_hook = QEventHook()

class WidgetTest(QtWidgets.QWidget):
    with Binder("test") as state:
        state.text = "aasdsd"
        state.num = 1
        state.val = 2.0
        state.color = "black"
        state.spin_color = "black"
    
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()
        

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.edit = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton("change Text")
        layout.addWidget(self.edit)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.change_text)
        self.edit.setText(lambda: self.state.text)
        self.label.setText(lambda: "message is %s" % self.state.text)
        
        # NOTE hook
        event_hook.add_hook(self.edit,QtCore.QEvent.FocusIn,self.color_focus_in)
        event_hook.add_hook(self.edit,QtCore.QEvent.FocusOut,self.color_focus_out)
        self.label.setStyleSheet(lambda:"color:%s" % self.state.color)

        self.spin = QtWidgets.QSpinBox(self)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.spin)
        layout.addWidget(self.label)
        self.spin.setValue(lambda: self.state.num)
        self.label.setText(lambda: "num is %s" % self.state.num)
        
        self.spin >> event_hook("HoverEnter",self.hover_in_event)
        self.spin >> event_hook("HoverLeave",self.hover_out_event)
        self.label.setStyleSheet(lambda:"color:%s" % self.state.spin_color)
        
        self.spin = QtWidgets.QDoubleSpinBox(self)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.spin)
        layout.addWidget(self.label)
        self.spin.setValue(lambda: self.state.val)
        self.label.setText(lambda: "val is %s" % self.state.val)
        
    def change_text(self):
        self.state.text = "asd"
    
    def color_focus_in(self):
        self.state.color = "red"
    
    def color_focus_out(self):
        self.state.color = "black"

    def hover_in_event(self):
        self.state.spin_color = "pink"

    def hover_out_event(self):
        self.state.spin_color = "blue"



if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    widget = WidgetTest()
    widget.show()

    app.exec_()
