# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-03 15:55:15"

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

from QBinder import Binder, GBinder , InfoPanel
from Qt import QtGui, QtWidgets, QtCore

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # state.input_ui = ButtonTest()
    # state.input_ui.show()
    widget = InfoPanel()
    widget.show()
    sys.exit(app.exec_())