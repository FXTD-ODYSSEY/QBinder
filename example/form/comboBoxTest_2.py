# coding:utf-8

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
            "options": OrderedDict([
                ('One', 'A'),
                ('Two', 'B'),
                ('Three', 'C'),
            ]),
        },
        "signals":{
            "combo.currentTextChanged": lambda self,widget,text: self.state["selected"].setVal(self.state.options.get(text))
        }
    })
    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        print(type(self.state.selected),type(self.state["selected"]))
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems([text for text in self.state.options])

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.combo)
        layout.addWidget(self.label)
        self.label.setText(lambda:"Selected: %s" % self.state.selected)

        self.state.selected =  self.state.options.get(self.combo.currentText())

        # self.combo.currentTextChanged.connect(lambda text: self.state._var_dict["selected"].setVal(self.state.options.get(text)))
        
    # def update(self,widget,text):
    #     self.state._var_dict["selected"].setVal(self.state.options.get(text))
        # self.state.selected = self.state.options.get(text)

def main():
    app = QtWidgets.QApplication([])

    widget = WidgetTest()
    widget.show()

    app.exec_()



if __name__ == "__main__":
    main()
