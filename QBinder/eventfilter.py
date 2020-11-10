# -*- coding: utf-8 -*-
"""

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


class QEventHook(QtCore.QObject):
    
    __init_flag = False
    __filter = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(QEventHook, cls).__new__(cls)
            cls.__init_flag = True
        return cls.__instance
    
    def __init__(self):
        if self.__init_flag:
            self.__init_flag = False
            super(QEventHook, self).__init__()
            app = QtWidgets.QApplication.instance()
            self.installEventFilter(app)

    def add_filter(self,option):
        self.__filter.update(option if isinstance(option,dict) else {})
        
    def get_filter(self):
        return self.__filter
    
    def eventFilter(self,receiver,event):
        data = self.__filter.get(receiver,{})
        if not data:
            return False
        for e,callbacks in data.items():
            if e is not event:
                continue
            callbacks = [callbacks] if callable(callbacks) else callbacks
            for callback in callbacks:
                callback()

        return False
    
        
