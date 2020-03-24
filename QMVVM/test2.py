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
		},
		"binding":{
			"count":{
				"label.setText":"str",
				"@label2.setText":{
					"set_callback_args":["count"],
					"set_callback":lambda count: "<center>%s</center>"%count,
				},
				"@label3.setText":lambda count: "<center>%s</center>" % count,
			},
		},
	})
	def __init__(self):
		super(Counter,self).__init__()
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
		# label2.setText("<center>%s</center>" % self.count)

		layout.addWidget(self.label)
		layout.addWidget(plus_button)
		layout.addWidget(minus_button)
		layout.addWidget(label2)
		layout.addWidget(label3)
		
		plus_button.clicked.connect(self.add)
		minus_button.clicked.connect(self.subtract)

		# print inspect.getmembers(OptionParser, predicate=inspect.ismethod)

	def add(self):
		print self.state.count
		self.state.count = 1

	def subtract(self):
		self.state.count = 4

		
def main():
	app = QtWidgets.QApplication([])

	counter = Counter()
	counter.show()

	app.exec_()

if __name__ == "__main__":
	main()
