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
from functools import partial

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

os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"

from QBinder import BinderTemplate, Binder
from QBinder.handler import Set, Anim
import Qt

print("__binding__", Qt.__binding__)
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi, translate


class RainbowBinder(BinderTemplate):
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
            self.start_flag = True
            self.height = 0
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
            # TODO Binding Handler getter
            # self["c%s" % i] >> Anim(self.rainbow_color[idx])

    def rainbow_increment(self):
        self.rainbow_index += 1
        if self.rainbow_index >= 7:
            self.rainbow_index = 0

    def rainbow_decrement(self):
        self.rainbow_index -= 1
        if self.rainbow_index <= 0:
            self.rainbow_index = 6


class ProgressBinder(BinderTemplate):
    def __init__(self):
        with self("dumper") as dumper:
            self.start_flag = True
            self.progress = 0
            self.timeout = 200
            self.step = 1

    def progress_increment(self):
        self.progress += self.step
        if self.progress >= 100:
            self.progress -= 100


class AnimWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AnimWidget, self).__init__(parent)

        # self.setupUi(self)

        ui_file = os.path.join(__file__, "..", "anim.ui")
        loadUi(ui_file, self)

        self.rainbow_initialize()
        self.progress_initialize()

    def rainbow_initialize(self):
        rainbow_binder = RainbowBinder()
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
                c0=tuple(rainbow_binder.c0),
                c1=tuple(rainbow_binder.c1),
                c2=tuple(rainbow_binder.c2),
                c3=tuple(rainbow_binder.c3),
                c4=tuple(rainbow_binder.c4),
                c5=tuple(rainbow_binder.c5),
                c6=tuple(rainbow_binder.c6),
            )
        )

        def anim_color_channel(i):
            R_SB = getattr(self, "C%sR_SB" % i)
            R_SB.setValue(lambda: getattr(rainbow_binder, "c%s" % i)[0] * 1)
            R_SB.editingFinished.connect(
                lambda: getattr(rainbow_binder, "c%s" % i)
                >> Anim(
                    [
                        R_SB.value(),
                        getattr(rainbow_binder, "c%s" % i)[1],
                        getattr(rainbow_binder, "c%s" % i)[2],
                    ]
                )
            )
            G_SB = getattr(self, "C%sG_SB" % i)
            G_SB.setValue(lambda: getattr(rainbow_binder, "c%s" % i)[1] * 1)
            G_SB.editingFinished.connect(
                lambda: getattr(rainbow_binder, "c%s" % i)
                >> Anim(
                    [
                        getattr(rainbow_binder, "c%s" % i)[0],
                        G_SB.value(),
                        getattr(rainbow_binder, "c%s" % i)[2],
                    ]
                )
            )
            B_SB = getattr(self, "C%sB_SB" % i)
            B_SB.setValue(lambda: getattr(rainbow_binder, "c%s" % i)[2] * 1)
            B_SB.editingFinished.connect(
                lambda: getattr(rainbow_binder, "c%s" % i)
                >> Anim(
                    [
                        getattr(rainbow_binder, "c%s" % i)[0],
                        getattr(rainbow_binder, "c%s" % i)[1],
                        B_SB.value(),
                    ]
                )
            )

        for i in range(7):
            anim_color_channel(i)

        self.Color_Frame.setFixedHeight(lambda: rainbow_binder.height)
        self.ColorInfo_BTN.clicked.connect(
            lambda: rainbow_binder.height
            >> Anim(
                0 if rainbow_binder.height else self.Color_Frame.sizeHint().height()
            )
        )

        self.ColorIncrement_BTN.clicked.connect(rainbow_binder.rainbow_increment)
        self.ColorDecrement_BTN.clicked.connect(rainbow_binder.rainbow_decrement)

        timer = QtCore.QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(rainbow_binder.rainbow_increment)
        self.AnimStart_BTN.clicked.connect(rainbow_binder.rainbow_increment)
        self.AnimStart_BTN.clicked.connect(
            lambda: rainbow_binder.start_flag >> Set(True)
        )
        self.AnimStop_BTN.clicked.connect(
            lambda: rainbow_binder.start_flag >> Set(False)
        )
        rainbow_binder["start_flag"].connect(
            lambda: timer.start() if rainbow_binder.start_flag else timer.stop()
        )

    def progress_initialize(self):
        progress_binder = ProgressBinder()

        self.Progress_SB.setValue(lambda: progress_binder.progress * 1)
        self.Progress_SB.editingFinished.connect(
            lambda: progress_binder.progress >> Set(self.Progress_SB.value())
        )
        self.Progress_Slider.setValue(lambda: progress_binder.progress)
        self.ProgressBar.setValue(lambda: progress_binder.progress)

        self.Time_SB.setValue(lambda: progress_binder.timeout * 1)
        self.Time_SB.editingFinished.connect(
            lambda: progress_binder.timeout >> Set(self.Time_SB.value())
        )
        self.Step_SB.setValue(lambda: progress_binder.step * 1)
        self.Step_SB.editingFinished.connect(
            lambda: progress_binder.step >> Set(self.Step_SB.value())
        )

        timer = QtCore.QTimer(self)
        timer.setInterval(lambda: progress_binder.timeout)
        timer.timeout.connect(progress_binder.progress_increment)
        self.ProgressStart_BTN.clicked.connect(progress_binder.progress_increment)

        self.ProgressStart_BTN.clicked.connect(
            lambda: progress_binder.start_flag >> Set(True)
        )
        self.ProgressStop_BTN.clicked.connect(
            lambda: progress_binder.start_flag >> Set(False)
        )
        progress_binder["start_flag"].connect(
            lambda: timer.start() if progress_binder.start_flag else timer.stop()
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = AnimWidget()
    widget.show()
    app.exec_()
