# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-10 22:32:24'

"""

"""
import types
from functools import wraps
from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel
def QtWrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print("run wrapper")
        return res
    return wrapper


class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        print("meta class")
        return obj

class A(object):
    # __metaclass__ = NewInitCaller
    pass


A.__metaclass__ = NewInitCaller

# print(A())

print(hasattr(None,"asd"))
print(dir(None))

def init(self,*args,**kwargs):
    # super(QtWidgets.QLabel, self).__init__(*args,**kwargs)
    print("init")
    print("init12")

# types.MethodType(QtWidgets.QLabel.__init__, init)
# types.MethodType(QtWidgets.QLabel.__new__, init)
# # types.MethodType(QtWidgets.QLabel.__call__, init)
# QtWidgets.QLabel.__call__ = init

setattr(QtWidgets,"QLabel",QtWrap(QtWidgets.QLabel))

app = QtWidgets.QApplication([])

label = QtWidgets.QLabel()
label.show()
# print ("state",label.STATE)

QtWidgets.QLabel.STATE = "123"

# print ("state",label.STATE)
# print ("state",QtWidgets.QLabel.__dict__)


app.exec_()