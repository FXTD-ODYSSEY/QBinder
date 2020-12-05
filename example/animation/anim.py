# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-03 19:10:10"

import os
import sys
import random

repo = (lambda f: lambda p=__file__: f(f, p))(
    lambda f, p: p
    if [
        d
        for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p))
        if d == ".github"
    ]
    else None
    if os.path.dirname(p) == p
    else f(f, os.path.dirname(p))
)()
sys.path.insert(0, repo) if repo not in sys.path else None

# os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"

from QBinder import BinderTemplate, Binder
from QBinder.handler import Set, Anim
import Qt

print("__binding__", Qt.__binding__)
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi, translate


class AnimBinder(BinderTemplate):
    def __init__(self):
        self.color_list = []
        self.idx_list = [i for i in range(7)]
        self.rainbow_color = [
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255),
            (255, 0, 0),
        ]
        with self("dumper") as dumper:
            self.rainbow_index = 0
            self.c0 = [255, 0, 0]
            self.c1 = [255, 255, 0]
            self.c2 = [0, 255, 0]
            self.c3 = [0, 255, 255]
            self.c4 = [0, 0, 255]
            self.c5 = [255, 0, 255]
            self.c6 = [255, 0, 0]

        self["rainbow_index"].connect(self.rainbow_change)

    def rainbow_change(self):

        idx_list = (
            self.idx_list[self.rainbow_index :] + self.idx_list[: self.rainbow_index]
        )
        for i, idx in enumerate(idx_list):
            color = self.rainbow_color[idx]
            self["c%s" % i].get() >> Anim(color)
            # TODO
            # self["c%s" % i] >> Anim(self.rainbow_color[idx])

    def rainbow_increment(self):
        self.rainbow_index += 1
        if self.rainbow_index >= 7:
            self.rainbow_index = 0

    def rainbow_decrement(self):
        self.rainbow_index -= 1
        if self.rainbow_index <= 0:
            self.rainbow_index = 6


class AnimWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AnimWidget, self).__init__(parent)

        self.state = AnimBinder()
        # self.setupUi(self)

        ui_file = os.path.join(__file__, "..", "anim.ui")
        loadUi(ui_file, self)

        self.Rainbow_Label.setStyleSheet(
            lambda: """
            background: qlineargradient(spread: pad,
                x1: 0,
                y1: 0,
                x2: 1,
                y2: 0,
                stop: 0.000 rgb{c0},
                stop: 0.166 rgb{c1},
                stop: 0.333 rgb{c2},
                stop: 0.500 rgb{c3},
                stop: 0.666 rgb{c4},
                stop: 0.833 rgb{c5},
                stop: 1.000 rgb{c6}
            );
        """.format(
                c0=tuple(self.state.c0),
                c1=tuple(self.state.c1),
                c2=tuple(self.state.c2),
                c3=tuple(self.state.c3),
                c4=tuple(self.state.c4),
                c5=tuple(self.state.c5),
                c6=tuple(self.state.c6),
            )
        )
        

        self.ColorIncrement_BTN.clicked.connect(lambda: self.state.rainbow_increment())
        self.ColorDecrement_BTN.clicked.connect(lambda: self.state.rainbow_decrement())

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.state.rainbow_increment)
        self.AnimStart_BTN.clicked.connect(lambda: timer.start(1000))
        self.AnimStop_BTN.clicked.connect(lambda: timer.stop())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = AnimWidget()
    widget.show()
    app.exec_()
