# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-09 17:02:59'

"""

"""

import os
import sys
# sys.path.append(os.path.abspath(os.path.join(__file__,"..","..")))

import Qt
print Qt.__binding__
from config import ConfigManager
from config import setAutoConfig
from Qt.QtGui import *
from Qt.QtCore import *
from Qt.QtWidgets import *

class MainWindow(QMainWindow):
    CONFIG = ConfigManager()

    def show_config(self):
        self.current_config_output.setText(str(self.CONFIG.as_dict()))

    @setAutoConfig(CONFIG)
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('PyQtConfig Demo')

        CHOICE_A = 1
        CHOICE_B = 2
        CHOICE_C = 3
        CHOICE_D = 4

        map_dict = {
            'Choice A': CHOICE_A,
            'Choice B': CHOICE_B,
            'Choice C': CHOICE_C,
            'Choice D': CHOICE_D,
        }

        # self.CONFIG.set_defaults({
        #     'number': 13,
        #     'text': 'hello',
        #     'active': True,
        #     'combo': CHOICE_C,
        # })

        gd = QGridLayout()

        sb = QSpinBox()
        gd.addWidget(sb, 0, 1)
        sb.setObjectName("number")
        # self.CONFIG.add_handler('number', sb)

        te = QLineEdit()
        gd.addWidget(te, 1, 1)
        te.setObjectName("text")
        te.setText("yes")
        # self.CONFIG.add_handler('text', te)

        cb = QCheckBox()
        gd.addWidget(cb, 2, 1)
        cb.setObjectName("active")
        # self.CONFIG.add_handler('active', cb)

        cmb = QComboBox()
        cmb.addItems(map_dict.keys())
        gd.addWidget(cmb, 3, 1)
        cmb.setObjectName("combo")

        cmb = QComboBox()
        cmb.addItems(map_dict.keys())
        gd.addWidget(cmb, 4, 1)
        # cmb.setObjectName("combo")
        self.CONFIG.add_handler('combo', cmb, mapper=map_dict)

        self.current_config_output = QTextEdit()
        gd.addWidget(self.current_config_output, 0, 3, 3, 1)

        self.CONFIG.updated.connect(self.show_config)

        self.show_config()

        self.window = QWidget()
        self.window.setLayout(gd)
        self.setCentralWidget(self.window)

    
def test():
        
    # Create a Qt application
    app = QApplication(sys.argv)
    app.setOrganizationName("PyQtConfig")
    app.setOrganizationDomain("martinfitzpatrick.name")
    app.setApplicationName("PyQtConfig")

    w = MainWindow()
    w.show()
    app.exec_()  # Enter Qt application main loop

if __name__ == "__main__":
    test()
