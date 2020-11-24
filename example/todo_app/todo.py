# -*- coding: utf-8 -*-
"""
https://vuejs.org/v2/examples/todomvc.html
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-08 16:05:07"

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

os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"
# os.environ["QT_PREFERRED_BINDING"] = "PySide;PySide2"

from QBinder import Binder, GBinder, QEventHook, FnHook, BinderCollector
from QBinder.handler import Set, Call, ItemConstructor, GroupBoxBind
from QBinder.mixin import ItemMixin

import Qt

print(Qt.__binding__)
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi

event_hook = QEventHook()
gstate = GBinder()


# gstate.todo_data = [
#     {"text": "todo1", "completed": False},
#     {"text": "todo2", "completed": True},
# ] * 5
# gstate.todo_data = [{"text": "%s" % i, "completed": False} for i in range(10)]

with gstate("dumper"):
    gstate.todo_data = []
    gstate.selected = "All"
    gstate.input = ""

gstate.item_count = 0
gstate.input_font = "italic"
gstate.completed_color = "lightgray"
gstate.footer_visible = False
gstate.todolist_visible = False
gstate.header_border = 0


gstate.update_count = FnHook()


@gstate.update_count
def _(state):
    state.item_count = len([todo for todo in state.todo_data if not todo["completed"]])


class EditableLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(EditableLabel, self).__init__(*args, **kwargs)
        self.editable = True
        self.item = None
        self.edit = QtWidgets.QLineEdit()
        self.edit.setVisible(False)
        self.edit.editingFinished.connect(self.__complete__)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.edit)

    def __complete__(self):
        self.edit.setVisible(False)
        edit_text = self.edit.text()
        self.setText(edit_text)
        if self.item:
            self.item.completedChanged()
            gstate.todo_data[self.item.__index__]["text"] = edit_text

    def mouseDoubleClickEvent(self, event):
        if event.button() == 1 and self.editable:
            self.edit.setVisible(True)
            self.edit.setText(self.text())
            self.edit.selectAll()
            self.edit.setFocus()
            if self.item:
                state = self.item.state
                state.text_style = "none"
                state.text_color = "black"

    def setEditable(self, editable):
        self.editable = bool(editable)

    def bind(self, item):
        self.item = item


class TodoItem(QtWidgets.QWidget, ItemMixin):

    state = Binder()

    # @inject(state)
    def __init__(self):
        super(TodoItem, self).__init__()

        self.state.text = "a"
        self.state.completed = False
        self.state.visible = False
        self.state.text_style = "none"
        self.state.text_color = "black"

        ui_file = os.path.join(__file__, "..", "item.ui")
        loadUi(ui_file, self)

        self.ItemText.bind(self)
        self.ItemText.setText(lambda: self.state.text)
        self.ItemText.setStyleSheet(
            lambda: "color:%s;text-decoration:%s"
            % (self.state.text_color, self.state.text_style)
        )
        self.ItemDelete.setVisible(lambda: self.state.visible)
        self.ItemCheck.setChecked(lambda: self.state.completed)

        self.state["completed"].connect(self.completedChanged)
        self.state["completed"].connect(gstate.update_count)

        self.ItemDelete.clicked.connect(lambda: gstate.todo_data.pop(self.__index__))

    def completedChanged(self):
        completed = self.state.completed
        self.state.text_style = "line-through" if completed else "none"
        self.state.text_color = "gray" if completed else "black"
        if gstate.todo_data[self.__index__]["completed"] != completed:
            gstate.todo_data[self.__index__]["completed"] = completed

    def setCompleted(self, completed):
        self.state.completed = completed

    def setText(self, text):
        self.state.text = text

    def enterEvent(self, event):
        self.state.visible = True

    def leaveEvent(self, event):
        self.state.visible = False


class TodoWidget(QtWidgets.QWidget):
    item_list = []

    def __init__(self):
        super(TodoWidget, self).__init__()
        ui_file = os.path.join(__file__, "..", "todo.ui")
        loadUi(ui_file, self)
        self.state = Binder()
        self.state.clear_text_style = "none"

        self.TodoHeader.setStyleSheet(
            lambda: "#TodoHeader { border-bottom:%spx solid lightgray; }"
            % (gstate.header_border)
        )
        self.TodoInput.setText(lambda: gstate.input)
        self.TodoInput.setStyleSheet(lambda: "font-style:%s" % (gstate.input_font))
        self.TodoInput.textChanged.connect(self.input_change)
        self.TodoInput.returnPressed.connect(self.add_item)
        self.TodoFooter.setVisible(lambda: gstate.footer_visible)
        self.TodoList.setVisible(lambda: gstate.todolist_visible)

        # NOTE add hover effect
        self.effect = QtWidgets.QGraphicsDropShadowEffect()
        self.effect.setBlurRadius(40)
        self.effect.setColor(QtGui.QColor("lightgray"))
        self.TodoContainer.setGraphicsEffect(self.effect)

        self.ItemClear.linkActivated.connect(self.clear_items)
        self.ItemClear.setText(
            lambda: '<html><head/><body><p><a href="clear" style="text-decoration: %s;color:gray">Clear completed</a></p></body></html>'
            % self.state.clear_text_style
        )
        self.ItemClear >> event_hook(
            "Enter", lambda: self.state.clear_text_style >> Set("underline")
        )
        self.ItemClear >> event_hook(
            "Leave", lambda: self.state.clear_text_style >> Set("none")
        )

        self.ItemComplted.linkActivated.connect(self.complete_items)
        self.ItemComplted.setText(
            lambda: '<html><head/><body><a href="complted" style="text-decoration:none;color:%s">﹀</p></body></html>'
            % gstate.completed_color
        )
        gstate["item_count"].connect(self.change_completed_color)

        self.ItemCount.setText(lambda: "%s item left" % gstate.item_count)

        # NOTE filter radiobutton handler
        gstate.selected >> GroupBoxBind(self.StateGroup)
        
        gstate["selected"].connect(self.update_item)
        gstate["todo_data"].connect(self.update_item) >> Call()

    def change_completed_color(self):
        gstate.completed_color = "lightgray" if gstate.item_count else "black"

    def complete_items(self):
        for todo in gstate.todo_data:
            todo["completed"] = True

    def clear_items(self):
        gstate.todo_data = [todo for todo in gstate.todo_data if not todo["completed"]]

    def add_item(self):
        gstate.todo_data.append(
            {
                "text": self.TodoInput.text(),
                "completed": False,
            }
        )
        self.TodoInput.clear()

    def update_item(self):

        filters = {
            "All": lambda data: data,
            "Active": lambda data: [d for d in data if not d["completed"]],
            "Completed": lambda data: [d for d in data if d["completed"]],
        }

        TodoItem >> ItemConstructor(
            __layout__=self.TodoList.layout(),
            __binder__="state",
            __data__=lambda: filters[gstate.selected](gstate.todo_data),
        )
        if gstate.todo_data:
            gstate.header_border = 1
            gstate.footer_visible = True
            gstate.todolist_visible = True
            gstate.update_count()
        else:
            gstate.header_border = 0
            gstate.footer_visible = False
            gstate.todolist_visible = False

    def input_change(self, text):
        gstate.input_font = "bold" if text else "italic"


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    gstate.todo_app = TodoWidget()
    gstate.todo_app.show()
    sys.exit(app.exec_())