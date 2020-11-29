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


from QBinder import Binder,QEventHook
from QBinder.handler import Set

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

# NOTE event_hook 使用单例模式
event_hook = QEventHook()

class WidgetTest(QtWidgets.QWidget):
    state = Binder()
    state.text = "text"
    state.num = 1
    state.color = "black"
    state.spin_color = "black"

    def __init__(self):
        super(WidgetTest, self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.edit = QtWidgets.QLineEdit()
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.edit)
        layout.addWidget(self.label)

        self.edit.setText(lambda: self.state.text)
        self.label.setText(lambda: "message is %s" % self.state.text)
        
        event_hook.add_hook(self.edit,QtCore.QEvent.FocusIn,lambda:self.state.color >> Set("red"))
        event_hook.add_hook(self.edit,QtCore.QEvent.FocusOut,lambda:self.state.color >> Set("black"))
        self.label.setStyleSheet(lambda:"color:%s" % self.state.color)

        self.spin = QtWidgets.QSpinBox(self)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.spin)
        layout.addWidget(self.label)
        self.spin.setValue(lambda: self.state.num)
        self.label.setText(lambda: "num is %s" % self.state.num)
        
        self.spin >> event_hook("HoverEnter",lambda:self.state.spin_color >> Set("pink"))
        self.spin >> event_hook("HoverLeave",lambda:self.state.spin_color >> Set("blue"))
        self.label.setStyleSheet(lambda:"color:%s" % self.state.spin_color)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = WidgetTest()
    widget.show()
    app.exec_()
