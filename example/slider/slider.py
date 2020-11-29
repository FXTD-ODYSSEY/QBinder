# -*- coding: utf-8 -*-
"""
两个 slider 相互控制效果
"""

from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-27 16:18:54"

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

# os.environ["QT_PREFERRED_BINDING"] = "PyQt4;PyQt5;PySide;PySide2"

from QBinder import BinderTemplate
from QBinder.handler import Set
import Qt
print("__binding__",Qt.__binding__)
from Qt import QtGui, QtWidgets, QtCore


class SliderBinder(BinderTemplate):
    def __init__(self):
        with self("dumper"):
            self.min_value = 0
            self.max_value = 0
            self.visible = True

    def toggle_visible(self):
        self.visible = not self.visible

    def min_slider_change(self, v):
        v = v / 1000
        self.min_value = v
        if v > self.max_value:
            self.max_value = v

    def max_slider_change(self, v):
        v = v / 1000
        self.max_value = v
        if v < self.min_value:
            self.min_value = v

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(333, 136)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.Min_SP = QtWidgets.QDoubleSpinBox(Form)
        self.Min_SP.setDecimals(3)
        self.Min_SP.setMaximum(1.0)
        self.Min_SP.setSingleStep(0.001)
        self.Min_SP.setObjectName("Min_SP")
        self.horizontalLayout_2.addWidget(self.Min_SP)
        self.Min_Slider = QtWidgets.QSlider(Form)
        self.Min_Slider.setMaximum(1000)
        self.Min_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Min_Slider.setObjectName("Min_Slider")
        self.horizontalLayout_2.addWidget(self.Min_Slider)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.Max_SP = QtWidgets.QDoubleSpinBox(Form)
        self.Max_SP.setDecimals(3)
        self.Max_SP.setMaximum(1.0)
        self.Max_SP.setSingleStep(0.001)
        self.Max_SP.setProperty("value", 0.015)
        self.Max_SP.setObjectName("Max_SP")
        self.horizontalLayout.addWidget(self.Max_SP)
        self.Max_Slider = QtWidgets.QSlider(Form)
        self.Max_Slider.setMaximum(1000)
        self.Max_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Max_Slider.setObjectName("Max_Slider")
        self.horizontalLayout.addWidget(self.Max_Slider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Vis_BTN = QtWidgets.QPushButton(Form)
        self.Vis_BTN.setObjectName("Vis_BTN")
        self.verticalLayout.addWidget(self.Vis_BTN)
        self.Min_Label = QtWidgets.QLabel(Form)
        self.Min_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Min_Label.setObjectName("Min_Label")
        self.verticalLayout.addWidget(self.Min_Label)
        self.Max_Label = QtWidgets.QLabel(Form)
        self.Max_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Max_Label.setObjectName("Max_Label")
        self.verticalLayout.addWidget(self.Max_Label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "SliderExample", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "最小值", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "最大值", None, -1))
        self.Vis_BTN.setText(QtWidgets.QApplication.translate("Form", "显示最大值最小值", None, -1))
        self.Min_Label.setText(QtWidgets.QApplication.translate("Form", "Min_Label", None, -1))
        self.Max_Label.setText(QtWidgets.QApplication.translate("Form", "Max_Label", None, -1))



class SliderWidget(QtWidgets.QWidget, Ui_Form):

    state = SliderBinder()

    def __init__(self, parent=None):
        super(SliderWidget, self).__init__(parent)
        self.setupUi(self)

        # NOTE 使用运算符 禁用双向绑定
        self.Min_SP.setValue(lambda: self.state.min_value * 1)
        self.Min_SP.editingFinished.connect(
            lambda: self.state.min_value >> Set(self.Min_SP.value())
        )
        self.Min_Slider.setValue(lambda: self.state.min_value * 1000)
        self.Min_Slider.valueChanged.connect(self.state.min_slider_change)

        self.Max_SP.setValue(lambda: self.state.max_value * 1)
        self.Max_SP.editingFinished.connect(
            lambda: self.state.max_value >> Set(self.Max_SP.value())
        )
        self.Max_Slider.setValue(lambda: self.state.max_value * 1000)
        self.Max_Slider.valueChanged.connect(self.state.max_slider_change)

        self.Vis_BTN.clicked.connect(self.state.toggle_visible)
        self.Min_Label.setVisible(lambda: self.state.visible)
        self.Max_Label.setVisible(lambda: self.state.visible)
        self.Min_Label.setText(lambda: "最小值: %s" % self.state.min_value)
        self.Max_Label.setText(lambda: "最大值: %s" % self.state.max_value)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = SliderWidget()
    widget.show()
    app.exec_()
