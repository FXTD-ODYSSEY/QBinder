# -*- coding: utf-8 -*-
"""
App Event Hook
hook the widget event rather than override class event method
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 23:47:53"

import sys
import six
import inspect
from functools import partial

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

class CustomThread(QtCore.QThread):
    def __init__(self, target):
        super(CustomThread, self).__init__()
        self.target = target
    def run(self, *args, **kwargs):
        self.target(*args, **kwargs)
        
class QEventHook(QtCore.QObject):

    __instance = None
    __init_flag = False
    __app_flag = False
    __hook = {}
    __event = None
    __callbacks = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(QEventHook, cls).__new__(cls)
            cls.__init_flag = True
        return cls.__instance

    def __init__(self):
        if self.__init_flag:
            self.__init_flag = False
            self.__app_flag = True
            super(QEventHook, self).__init__()
            self.installEventFilter(self)
            # self.timer = QtCore.QTimer()
            
            # self.thread = QtCore.QThread()
            # self.moveToThread(self.thread)
            # self.thread.started.connect(self.start)
            # self.thread.start()
            # QtCore.QMetaObject.invokeMethod(self,"start",QtCore.Qt.QueuedConnection)
        
        # TODO May be Hook QApplication
        instance = QtWidgets.QApplication.instance()
        if self.__app_flag and instance:
            self.__app_flag = True
            QtCore.QTimer.singleShot(
                0, lambda: QtWidgets.QApplication.instance().installEventFilter(self)
            )
                
    def __rrshift__(self, receiver):
        self.add_hook(receiver)
        return receiver

    def __call__(self, event, callbacks):
        self.__event = event
        self.__callbacks = callbacks
        return self

    def add_hook(self, receiver, event=None, callbacks=None):
        event = event if event else self.__event
        event = getattr(QtCore.QEvent, event) if isinstance(event, str) else event
        callbacks = callbacks if callbacks else self.__callbacks
        if not event or not callbacks:
            return
        self.__hook.setdefault(receiver, {})
        self.__hook[receiver].setdefault(event, [])
        self.__hook[receiver][event].extend(
            callbacks if isinstance(callbacks, list) else [callbacks]
        )

    def get_hook(self):
        return self.__hook

    def set_hook(self, hook):
        self.__hook = hook

    def eventFilter(self, receiver, event):
        data = self.__hook.get(receiver)
        if data:
            callbacks = data.get(event.type(), [])
            for callback in callbacks:
                callback()

        return super(QEventHook, self).eventFilter(receiver, event)
