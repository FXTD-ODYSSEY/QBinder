# -*- coding: utf-8 -*-
"""
https://vuejs.org/v2/examples/todomvc.html
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-08 16:05:07'

import os
import sys

repo = (lambda f: lambda p=__file__: f(f, p))(
    lambda f, p: p
    if [
        d
        for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p))
        if d == ".git"
    ]
    else None
    if os.path.dirname(p) == p
    else f(f, os.path.dirname(p))
)()
sys.path.insert(0, repo) if repo not in sys.path else None

from QBinder import Binder, GBinder,show_info_panel
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi

state = GBinder()
state.msg = "msg"
state.num = 1
state.input_ui = 1
# state.text = 'text'

# class VerticalLabel(QtWidgets.QLabel):
#     '''
#     https://stackoverflow.com/a/59904457
#     python qt not support css rotate
#     '''
#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         painter.translate(0, self.height())
#         painter.rotate(-90)
#         painter.drawText(self.height()/4, self.width(), self.text())
#         painter.end()
        
class TodoWidget(QtWidgets.QWidget):
    def __init__(self):
        super(TodoWidget, self).__init__()
        ui_file = os.path.join(__file__,'..','todo.ui')
        loadUi(ui_file,self)
        
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(3,3)
        self.TodoContainer.setGraphicsEffect(effect)
        

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    todo = TodoWidget()
    todo.show()
    sys.exit(app.exec_())