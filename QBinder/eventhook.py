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

import inspect

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

class QEventHook(QtCore.QObject):

    __invert_flag = False
    __instance = None
    __init_flag = False
    __app_flag = False
    __hook = {}
    __invert_hook = {}
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
            # TODO Test PyQt
            event = QtCore.QEvent(QtCore.QEvent.User)
            QtWidgets.QApplication.postEvent(self,event)
    
    def event(self,event):
        # NOTE https://doc.qt.io/qtforpython/overviews/eventsandfilters.html
        if event.type() is QtCore.QEvent.User:
            app = QtWidgets.QApplication.instance()
            app.installEventFilter(self)
        return super(QEventHook,self).event(event)

    def eventFilter(self, receiver, event):
        data = self.__hook.get(receiver)
        if data:
            callbacks = data.get(event.type(), [])
            for callback in callbacks:
                length = len(inspect.getargspec(callback).args) 
                count = length - 1 if inspect.ismethod(callback) else length
                args = (event,)
                callback(*args[:count])
        data = self.__invert_hook.get(receiver)
        if data is None:
            callbacks = self.__invert_hook.get(event.type(),[])
            for callback in callbacks:
                length = len(inspect.getargspec(callback).args) 
                count = length - 1 if inspect.ismethod(callback) else length
                args = (receiver,event,)
                callback(*args[:count])

        return super(QEventHook, self).eventFilter(receiver, event)

    def __rrshift__(self, receiver):
        event = self.__event
        event = getattr(QtCore.QEvent, event) if isinstance(event, str) else event
        if self.__invert_flag:
            self.__invert_flag = False
            self.add_invert_hook(receiver,event,self.__callbacks)   
        else:
            self.add_hook(receiver,event,self.__callbacks)
        return receiver
    
    def __invert__(self):
        self.__invert_flag = True
        return self
            
    def __call__(self, event, callbacks):
        """__call__ drive add_hook
        
        https://doc.qt.io/qtforpython/PySide2/QtCore/QEvent.html
        
        :param event: QEvent Type 
        :type event: str | QEvent.Type
        :param callbacks: callable list or callable object
        :type callbacks: callable
        """        
        self.__event = event
        self.__callbacks = callbacks
        return self

    def add_hook(self, receiver, event, callbacks):   
        """add_hook global hook
        
        https://doc.qt.io/qtforpython/PySide2/QtCore/QEvent.html
        
        :param receiver: object or widget
        :type receiver: QtCore.QObject
        :param event: QEvent Type , defaults to None
        :type event: str | QEvent.Type
        :param callbacks: callable list or callable object , defaults to None
        :type callbacks: callable
        """    
        
        if not event or not callbacks:
            return
        self.__hook.setdefault(receiver, {})
        self.__hook[receiver].setdefault(event, [])
        self.__hook[receiver][event].extend(
            [c for c in callbacks if callable(c)] if isinstance(callbacks, list) else [callbacks]
        )
        
    def add_invert_hook(self, receiver, event, callbacks):   
        if not event or not callbacks:
            return
        self.__invert_hook.setdefault(receiver,True)
        self.__invert_hook.setdefault(event,[])
        self.__invert_hook[event].extend(
            [c for c in callbacks if callable(c)] if isinstance(callbacks, list) else [callbacks]
        )

    def get_hook(self):
        return self.__hook

    def set_hook(self, hook):
        self.__hook = hook

    