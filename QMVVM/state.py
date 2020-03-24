# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 22:19:44'

"""

"""

from PySide2 import QtCore




class IntState(int,object):
    def __init__(self):
        pass

class StateFactory(object):
    
    def getState(self,state_type):
        if state_type == int:
            return IntState()