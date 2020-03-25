# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import os
import sys

from functools import wraps

DIR = os.path.dirname(__file__)
import sys
MODULE = os.path.join(DIR,"..")
if MODULE not in sys.path:
	sys.path.append(MODULE)

import QMVVM

class Counter(QtWidgets.QWidget):

	@QMVVM.store({
		"state":{
			"text":"",
		},
		"bindings":{
			"text":{
				"line.setText":"str",
				"@label.setText":"str",
				"@line.setText":"str",
			},
		},
	})
	def __init__(self):
		super(Counter,self).__init__()
		self.initialize()

	def initialize(self):
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)
	
		self.line = QtWidgets.QLineEdit()
		line = QtWidgets.QLineEdit()

		label = QtWidgets.QLabel()

		layout.addWidget(self.line)
		layout.addWidget(label)
		layout.addWidget(line)
		
		self.line.textChanged.connect(self.modify)
		line.textChanged.connect(self.modify)

	def modify(self,text):
		self.state.text = text
		
def main():
	app = QtWidgets.QApplication([])

	counter = Counter()
	counter.show()

	app.exec_()

if __name__ == "__main__":
	main()
