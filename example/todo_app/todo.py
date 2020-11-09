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

from QBinder import Binder, GBinder
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi


state = GBinder()
state.todo_data = [
    {"text": "todo", "completed": False},
    {"text": "todo", "completed": True},
]
# state.todo_data = []
state.item_count = 0
state.input_font = "italic"
state.completed_color = "lightgray"
state.footer_visible = False
state.todolist_visible = False
state.header_border = 0
state.selected = "All"

# TODO computed attr
def update_count():
    count = 0
    for todo in state.todo_data:
        count += 0 if todo["completed"] else 1
    state.item_count = count


class TodoItem(QtWidgets.QWidget):
    def __init__(self, index):
        super(TodoItem, self).__init__()
        self.index = index
        self.state = Binder()
        self.state.text = ""
        self.state.completed = False
        self.state.visible = False
        self.state.text_style = "none"
        self.state.text_color = "black"

        ui_file = os.path.join(__file__, "..", "item.ui")
        loadUi(ui_file, self)

        self.ItemDelete.setVisible(lambda: self.state.visible)
        self.ItemCheck.setChecked(lambda: self.state.completed)
        self.ItemText.setText(lambda: self.state.text)
        self.ItemText.setStyleSheet(
            lambda: "color:%s;text-decoration:%s"
            % (self.state.text_color, self.state.text_style)
        )

        self.state["completed"].connect(self.completedChanged)
        self.state["completed"].connect(update_count)

        self.ItemDelete.clicked.connect(lambda: state.todo_data.pop(self.index))

    def completedChanged(self):
        completed = self.state.completed
        self.state.text_style = "line-through" if completed else "none"
        self.state.text_color = "gray" if completed else "black"
        check = state.todo_data[self.index]["completed"]
        if check != completed:
            state.todo_data[self.index]["completed"] = completed

    def setCompleted(self, completed):
        self.state.completed = completed

    def setText(self, text):
        self.state.text = text

    def enterEvent(self, event):
        self.state.visible = True

    def leaveEvent(self, event):
        self.state.visible = False


class HoverLabel(QtWidgets.QLabel):
    """
    https://stackoverflow.com/a/57088301
    """

    def __init__(self, *args, **kwargs):
        super(HoverLabel, self).__init__(*args, **kwargs)
        self.state = Binder()
        self.state.clear_text_style = "none"

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
        ui_file = os.path.join(__file__, "..", "todo.ui")
        loadUi(ui_file, self)

        self.TodoHeader.setStyleSheet(
            lambda: "#TodoHeader { border-bottom:%spx solid lightgray; }"
            % (state.header_border)
        )
        self.TodoInput.setStyleSheet(lambda: "font-style:%s" % (state.input_font))
        self.TodoInput.textChanged.connect(self.input_change)
        self.TodoInput.returnPressed.connect(self.add_item)
        self.TodoFooter.setVisible(lambda: state.footer_visible)
        self.TodoList.setVisible(lambda: state.todolist_visible)

        # NOTE add hover effect
        self.effect = QtWidgets.QGraphicsDropShadowEffect()
        self.effect.setBlurRadius(40)
        self.effect.setColor(QtGui.QColor("lightgray"))
        self.TodoContainer.setGraphicsEffect(self.effect)

        self.ItemClear.linkActivated.connect(self.clear_items)
        self.ItemClear.setText(
            lambda: '<html><head/><body><p><a href="clear" style="text-decoration: %s;color:gray">Clear completed</a></p></body></html>'
            % self.ItemClear.state.clear_text_style
        )

        self.ItemComplted.linkActivated.connect(self.complete_items)
        self.ItemComplted.setText(
            lambda: '<html><head/><body><a href="complted" style="text-decoration:none;color:%s">﹀</p></body></html>'
            % state.completed_color
        )
        state["item_count"].connect(self.change_completed_color)

        self.ItemCount.setText(lambda: "%s item left" % state.item_count)

        # NOTE get state
        for rb in self.StateGroup.findChildren(QtWidgets.QRadioButton):
            rb.toggled.connect(self.filter_state)

        state["todo_data"].connect(self.load_item)
        self.load_item()

    def filter_state(self, filter):
        for rb in self.StateGroup.findChildren(QtWidgets.QRadioButton):
            if rb.isChecked():
                state.selected = rb.text().strip()
        self.load_item()

    def change_completed_color(self):
        state.completed_color = "lightgray" if state.item_count else "black"

    def complete_items(self):
        for todo in state.todo_data:
            todo["completed"] = True
        self.load_item()

    def clear_items(self):
        del state.todo_data[:]

    def add_item(self):
        state.todo_data.append(
            {
                "text": self.TodoInput.text(),
                "completed": False,
            }
        )
        self.TodoInput.clear()

    def load_item(self):
        layout = self.TodoList.layout()
        # NOTE clear item
        [item.deleteLater() for item in self.item_list]
        del self.item_list[:]

        # TODO reconstruct item not optimized
        if state.todo_data:
            state.header_border = 1
            state.footer_visible = True
            state.todolist_visible = True
            for i, todo in enumerate(state.todo_data):
                completed = todo["completed"]

                if state.selected == "Active" and completed:
                    continue
                elif state.selected == "Completed" and not completed:
                    continue

                item = TodoItem(i)
                item.setText(todo["text"])
                item.setCompleted(completed)
                self.item_list.append(item)
                layout.addWidget(item)
            update_count()
        else:
            state.header_border = 0
            state.footer_visible = False
            state.todolist_visible = False

    def input_change(self, text):
        state.input_font = "bold" if text else "italic"


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    state.todo_app = TodoWidget()
    state.todo_app.show()
    sys.exit(app.exec_())