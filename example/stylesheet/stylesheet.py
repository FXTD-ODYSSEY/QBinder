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
from QBinder.handler import Set,Anim
import Qt

print("__binding__", Qt.__binding__)
from Qt import QtGui, QtWidgets, QtCore
from Qt.QtCompat import loadUi, translate

class StyleSheetBinder(BinderTemplate):
    def __init__(self):
        with self("dumper") as dumper:
            self.r = 0
            self.g = 0
            self.b = 0

            self.h = 0
            self.s = 0
            self.v = 0

            self.text = "text"
            self.family = u"宋体"
            self.font_size = 9
            self.font_style = 0

            self.bold = False
            self.italic = False

            self.underline = False
            self.through = False

            self.decoration = "none"
            
        self["underline"].connect(self.decoration_change)
        self["through"].connect(self.decoration_change)

    def decoration_change(self):
        decoration = ""
        if self.underline:
            decoration += " underline"
        if self.through:
            decoration += " line-through"
        if not decoration:
            decoration = "none"
        self.decoration = decoration
        
    def to_red(self):
        self.r >> Anim(255)
        self.g >> Anim(0)
        self.b >> Anim(0)
        
    def to_green(self):
        self.r >> Anim(0)
        self.g >> Anim(255)
        self.b >> Anim(0)
        
    def to_blue(self):
        self.r >> Anim(0)
        self.g >> Anim(0)
        self.b >> Anim(255)

class StyleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StyleWidget, self).__init__(parent)
        try:
            self.state = StyleSheetBinder()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
        # self.setupUi(self)

        ui_file = os.path.join(__file__, "..", "stylesheet.ui")
        loadUi(ui_file, self)

        self.RGB_Label.setStyleSheet(
            lambda: "background:rgb(%s,%s,%s)"
            % (self.state.r, self.state.g, self.state.b)
        )
        self.R_SP.setValue(lambda: self.state.r)
        self.G_SP.setValue(lambda: self.state.g)
        self.B_SP.setValue(lambda: self.state.b)
        self.R_Slider.setValue(lambda: self.state.r)
        self.G_Slider.setValue(lambda: self.state.g)
        self.B_Slider.setValue(lambda: self.state.b)
        
        # NOTE Animation Color
        self.Red_BTN.clicked.connect(self.state.to_red)
        self.Green_BTN.clicked.connect(self.state.to_green)
        self.Blue_BTN.clicked.connect(self.state.to_blue)

        self.HSV_Label.setStyleSheet(
            lambda: "background:hsl(%s,%s,%s)"
            % (self.state.h, self.state.s, self.state.v)
        )
        self.H_SP.setValue(lambda: self.state.h)
        self.S_SP.setValue(lambda: self.state.s)
        self.V_SP.setValue(lambda: self.state.v)
        self.H_Slider.setValue(lambda: self.state.h)
        self.S_Slider.setValue(lambda: self.state.s)
        self.V_Slider.setValue(lambda: self.state.v)

        self.Font_Label.setStyleSheet(
            lambda: u"""
            font-family: {family};
            font-size: {size}pt;
            font-style: {style};
            font-weight: {weight};
            text-decoration: {decoration};
            """.format(
                family=self.state.family,
                size=self.state.font_size,
                decoration=self.state.decoration,
                style=u"italic" if self.state.italic else u"none",
                weight=u"bold" if self.state.bold else u"none",
            )
        )
        self.Font_Label.setText(lambda: self.state.text)
        self.Fone_LE.setText(lambda: self.state.text)

        self.Font_Combo.currentFontChanged.connect(
            lambda f: self.state.family >> Set(f.family())
        )
        self.Font_Size_SP.setValue(lambda: self.state.font_size)

        self.Font_Bold_CB.setChecked(lambda: self.state.bold)
        self.Font_Italic_CB.setChecked(lambda: self.state.italic)
        self.Font_Underline_CB.setChecked(lambda: self.state.underline)
        self.Font_LineThrough_CB.setChecked(lambda: self.state.through)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = StyleWidget()
    widget.show()
    app.exec_()
