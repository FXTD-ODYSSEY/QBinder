# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-22 22:55:38'

"""

"""

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import sys
import inspect
import traceback
import dis
import pdb
from optparse import OptionParser

from functools import wraps

import QMVVM

class Counter(QtWidgets.QWidget):

	@QMVVM.store({
		"state":{
			"count":0,
			"count2":6,
		},
		"bindings":{
			"variable":{
				"count":{
					"label.setText":"str",
					"@label3.setText":lambda count: "<center>%s</center>" % count,
				},
			},
			"callback":{
				"@label2.setText":{
					"set_callback_args":["count","count2"],
					"set_callback":lambda count,count2: "<center>%s %s</center>"%(count,count2),
				},
				"@label4.setText":{
					"set_callback_args":["@count","count3"],
					"set_callback":"calculate",
				},
			}
		},
	})
	def __init__(self):
		super(Counter,self).__init__()
		self.count = 4
		self.count3 = 15
		self.initialize()

	def initialize(self):
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)
	
		self.label = QtWidgets.QLabel()
		# label.setText("<center>%s</center>" % self.count)

		plus_button = QtWidgets.QPushButton("+")
		minus_button = QtWidgets.QPushButton("-")

		label2 = QtWidgets.QLabel()
		label3 = QtWidgets.QLabel()
		label4 = QtWidgets.QLabel()
		# label2.setText("<center>%s</center>" % self.count)

		layout.addWidget(self.label)
		layout.addWidget(plus_button)
		layout.addWidget(minus_button)
		layout.addWidget(label2)
		layout.addWidget(label3)
		layout.addWidget(label4)
		
		plus_button.clicked.connect(self.add)
		minus_button.clicked.connect(self.subtract)

		# print inspect.getmembers(OptionParser, predicate=inspect.ismethod)

	def add(self):
		print self.state.count
		self.state.count += 1

	def subtract(self):
		self.state.count -= 1

	def calculate(self,a,b):
		return str(a * b)
		
def main():
	app = QtWidgets.QApplication([])

	counter = Counter()
	counter.show()

	app.exec_()

if __name__ == "__main__":
	main()
