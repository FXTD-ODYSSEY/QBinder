# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-07 22:40:46'

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

from functools import partial

class CollapsibleWidget( QtWidgets.QWidget ):
    def __init__(self):
        super( CollapsibleWidget, self ).__init__()
        
    @staticmethod
    def install(btn,container,duration=300,expand_callback=None,collapse_callback=None):
        anim = QtCore.QPropertyAnimation(container, b"maximumHeight")
        
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(container.sizeHint().height())
        anim.finished.connect(lambda:container.setMaximumHeight(16777215) if not btn.toggle else None)

        btn.toggle = False
        btn.setText(u"▼ %s"%btn.text())
        def toggleFn(btn,anim):
            if btn.toggle:
                btn.toggle = False
                anim.setDirection(QtCore.QAbstractAnimation.Forward)

                anim.setEndValue(CollapsibleWidget.getHeightEndValue(container))
                anim.start()
                btn.setText(u"▼%s"%btn.text()[1:])
                btn.setStyleSheet('font:normal')
                if expand_callback:
                    expand_callback()
            else:
                btn.toggle = True
                anim.setDirection(QtCore.QAbstractAnimation.Backward)
                anim.setEndValue(container.sizeHint().height())
                anim.start()
                btn.setText(u"■%s"%btn.text()[1:])
                btn.setStyleSheet('font:bold')
                if collapse_callback:
                    collapse_callback()

        func = partial(toggleFn,btn,anim)
        btn.clicked.connect(func)
        return func

    @staticmethod
    def getHeightEndValue(widget):

        parent = widget.parent()
        total_height = parent.height()

        height = 0
        for child in parent.children():
            if child == widget or not hasattr(child,"height"):
                continue
            
            height += child.height()

        widget.updateGeometry()
        prefer = widget.sizeHint().height()
        height = total_height - height
        return height if height > prefer else prefer