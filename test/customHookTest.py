# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-01-30 22:16:52"


import os
import sys
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

DIR = os.path.dirname(__file__)
import sys

MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.insert(0, MODULE)
    
from QBinder import Binder
from QBinder.hook import MethodHook,FuncHook
from Qt import QtWidgets
import os
import sys


state = Binder()
state.msg = "test"

@FuncHook
def print_test(msg):
    print("print_test: %s" % msg)

class Test(object):
    @MethodHook
    def cls_print_test(cls, msg):
        print("cls_print_test: %s" % msg)


def main():
    app = QtWidgets.QApplication([])
    test = Test()
    test.cls_print_test(lambda: state.msg)
    print_test(lambda: state.msg)
    state.msg = "change"

    app.exec_()


if __name__ == "__main__":
    main()
