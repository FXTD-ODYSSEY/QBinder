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
        with self("dumper"):
            self.rainbow_index = 0
            self.c0_r = 255
            self.c0_g = 0
            self.c0_b = 0

            self.c1_r = 255
            self.c1_g = 255
            self.c1_b = 0

            self.c2_r = 0
            self.c2_g = 255
            self.c2_b = 0

            self.c3_r = 0
            self.c3_g = 255
            self.c3_b = 255

            self.c4_r = 0
            self.c4_g = 0
            self.c4_b = 255

            self.c5_r = 255
            self.c5_g = 0
            self.c5_b = 255

            self.c6_r = 255
            self.c6_g = 0
            self.c6_b = 0

    def rainbow_change(self):
        idx_list = (
            self.idx_list[self.rainbow_index :] + self.idx_list[: self.rainbow_index]
        )
        for i,idx in enumerate(idx_list):
            color = self.rainbow_color[idx]
            self["c%s_r" % i].get() >> Anim(color[0])
            self["c%s_g" % i].get() >> Anim(color[1])
            self["c%s_b" % i].get() >> Anim(color[2])

    def rainbow_increment(self):
        self.rainbow_index += 1
        if self.rainbow_index >= 7:
            self.rainbow_index = 0
        self.rainbow_change()
        
    def rainbow_decrement(self):
        self.rainbow_index -= 1
        if self.rainbow_index <= 0:
            self.rainbow_index = 6
        self.rainbow_change()


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
                stop: 0.000 rgb({c0_r}, {c0_g}, {c0_b}),
                stop: 0.166 rgb({c1_r}, {c1_g}, {c1_b}),
                stop: 0.333 rgb({c2_r}, {c2_g}, {c2_b}),
                stop: 0.500 rgb({c3_r}, {c3_g}, {c3_b}),
                stop: 0.666 rgb({c4_r}, {c4_g}, {c4_b}),
                stop: 0.833 rgb({c5_r}, {c5_g}, {c5_b}),
                stop: 1.000 rgb({c6_r}, {c6_g}, {c6_b})
            );
        """.format(
                c0_r=self.state.c0_r,
                c1_r=self.state.c1_r,
                c2_r=self.state.c2_r,
                c3_r=self.state.c3_r,
                c4_r=self.state.c4_r,
                c5_r=self.state.c5_r,
                c6_r=self.state.c6_r,
                c0_g=self.state.c0_g,
                c1_g=self.state.c1_g,
                c2_g=self.state.c2_g,
                c3_g=self.state.c3_g,
                c4_g=self.state.c4_g,
                c5_g=self.state.c5_g,
                c6_g=self.state.c6_g,
                c0_b=self.state.c0_b,
                c1_b=self.state.c1_b,
                c2_b=self.state.c2_b,
                c3_b=self.state.c3_b,
                c4_b=self.state.c4_b,
                c5_b=self.state.c5_b,
                c6_b=self.state.c6_b,
            )
        )

        self.ColorIncrement_BTN.clicked.connect(lambda: self.state.rainbow_increment())
        self.ColorDecrement_BTN.clicked.connect(lambda: self.state.rainbow_decrement())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = AnimWidget()
    widget.show()
    app.exec_()
