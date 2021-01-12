# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 14:34:10"


import os
import sys
import inspect
import traceback

from functools import wraps

# os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"

DIR = os.path.dirname(__file__)

MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.insert(0, MODULE)

from QBinder import Binder, QEventHook
import Qt

print(Qt.__binding__)
from Qt import QtWidgets, QtCore, QtGui

event_hook = QEventHook.instance()


class DragDropListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(DragDropListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        app = QtWidgets.QApplication.instance()
        app.installEventFilter(self)

    def eventFilter(self, receiver, event):
        if event.type() == QtCore.QEvent.DragMove:
            print("filter", receiver, receiver.parent(), type(receiver))
        return False

    def dragEnterEvent(self, event):
        event.accept() if event.mimeData().hasUrls() else event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            url_list = [url.toLocalFile() for url in event.mimeData().urls()]
            self.addItems(url_list)
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # print(event,type(event))
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


class DragDropWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DragDropWidget, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("DragDropWidget")

        # self.list_widget = DragDropListWidget()
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setAcceptDrops(True)

        # TODO eventhook limitations
        self.list_widget.dragEnterEvent = self.dragEnterEvent
        self.list_widget.dragMoveEvent = self.dragMoveEvent
        # self.list_widget.dropEvent = self.dropEvent

        # self.list_widget >> event_hook("DragEnter",self.dragEnterEvent)
        # self.list_widget >> event_hook("DragMove",self.dragMoveEvent)
        self.list_widget >> event_hook("Drop", self.dropEvent)

        layout.addWidget(self.list_widget)

    def dragEnterEvent(self, event):
        print(event, event.mimeData().hasUrls(), type(event))
        event.accept() if event.mimeData().hasUrls() else event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            url_list = [url.toLocalFile() for url in event.mimeData().urls()]
            self.list_widget.addItems(url_list)
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


def main():
    app = QtWidgets.QApplication([])

    widget = DragDropWidget()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
