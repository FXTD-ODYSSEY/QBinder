# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-29 17:07:57'

"""

"""

import os
import sys

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR,"..","QBinding","_vendor")
if MODULE not in sys.path:
    sys.path.append(MODULE)

# import QBinding
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class WidgetTest(QtWidgets.QWidget):

    # ComputedSignal = QtCore.Signal()
    # StateSignal = QtCore.Signal()

    _var_dict = {}
    _var_dict["ComputedSignal"] = QtCore.Signal()
    _var_dict["StateSignal"] = QtCore.Signal()
    locals().update(_var_dict)

    def __init__(self):
        super(WidgetTest, self).__init__()

        # ! RuntimeError: maximum recursion depth exceeded while calling a Python object
        getattr(self,"StateSignal").connect(getattr(self,"ComputedSignal").emit)
        self.ComputedSignal.connect(lambda:print("computed signal"))
        getattr(self,"StateSignal").emit()

        # ! Empty Property 
        self.setProperty("test","hello,world")
        print(self.dynamicPropertyNames())

        # ! remove unicode_literals will fix all the problems or Add b to the _var_dict key
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()

    widget.show()
    
    sys.exit(app.exec_())