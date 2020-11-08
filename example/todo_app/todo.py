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

from QBinder import Binder, GBinder
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi



class TodoItem(QtWidgets.QWidget):
    
    def __init__(self):
        super(TodoItem, self).__init__()
        self.state = Binder()
        self.state.text = ''
        self.state.completed = False
        self.state.visible = False
        self.state.text_style = "none"

        ui_file = os.path.join(__file__,'..','item.ui')
        loadUi(ui_file,self)
        self.ItemDelete.setVisible(lambda:self.state.visible)
        self.ItemCheck.setChecked(lambda:self.state.completed)
        self.ItemText.setText(lambda:self.state.text)
        self.ItemText.setStyleSheet(lambda:"text-decoration:%s" % self.state.text_style)
        self.state["completed"].connect(self.completedChanged)
    
    def completedChanged(self):
        self.state.text_style = "line-through" if self.state.completed else "none"
    
    def setCompleted(self,completed):
        self.state.completed = completed
    
    def setIndex(self,index):
        self.index = index
    
    def setText(self,text):
        self.state.text = text
    
    def enterEvent(self, event):
        self.state.visible = True

    def leaveEvent(self, event):
        self.state.visible = False
        
state = GBinder()
state.todo_data = [{"text":'todo','completed':False}]
state.input_font = "italic"
state.footer_visible = True
state.header_border = 0


class HoverLabel(QtWidgets.QLabel):
    """
    https://stackoverflow.com/a/57088301
    """
    state = Binder()
    state.clear_text_style = "none"

    def enterEvent(self, event):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)
        self.state.clear_text_style = "underline"

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        self.state.clear_text_style = "none"
        
class TodoWidget(QtWidgets.QWidget):
    item_list = []
    def __init__(self):
        super(TodoWidget, self).__init__()
        ui_file = os.path.join(__file__,'..','todo.ui')
        loadUi(ui_file,self)
        
        self.TodoHeader.setStyleSheet(lambda : """
            #TodoHeader
            {
                border-bottom:%spx solid lightgray;
            }                              
        """ % (state.header_border))
        self.TodoInput.setStyleSheet(lambda : "font-style:%s" % (state.input_font))
        self.TodoInput.textChanged.connect(self.input_change)
        self.TodoInput.returnPressed.connect(self.add_item)
        self.TodoFooter.setVisible(lambda:state.footer_visible)

        # NOTE add hover effect 
        self.ItemClear.setStyleSheet(lambda:"text-decoration:%s" % self.ItemClear.state.clear_text_style)
        
        self.effect = QtWidgets.QGraphicsDropShadowEffect()
        self.effect.setBlurRadius(40)
        self.effect.setColor(QtGui.QColor("lightgray"))
        self.TodoContainer.setGraphicsEffect(self.effect)
        
        state["todo_data"].connect(self.load_item)
        self.load_item()
   
    def add_item(self):
        state.todo_data.append({
            "text": self.TodoInput.text(),
            "completed": False,    
        })
        self.TodoInput.clear()

    def load_item(self):
        layout = self.TodoList.layout()
        # NOTE clear item 
        [item.deleteLater() for item in self.item_list]
        del self.item_list[:]
        for i,todo in enumerate(state.todo_data):
            item = TodoItem()
            item.setIndex(i)
            item.setText(todo['text'])
            item.setCompleted(todo['completed'])
            self.item_list.append(item)
            layout.addWidget(item)
        
    def input_change(self,text):
        state.input_font = "bold" if text else "italic"
        # state.header_border = 1 if text else 0
        # state.footer_visible = text
    

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    todo = TodoWidget()
    todo.show()
    sys.exit(app.exec_())