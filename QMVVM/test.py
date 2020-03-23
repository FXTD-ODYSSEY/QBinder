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

# import QRedux

from functools import wraps

def initDeco(func):

	def trace_func(frame,event,arg):
		# NOTE 获取局部变量 a 并修改变量
		if event == 'return':
			caller_code = frame.f_code
			lineno = frame.f_lineno
			# print lineno
			
			print dis.dis(caller_code.co_code)
			# try:
			# 	print "caller_code",caller_code.co_code.encode('utf-8')
			# except:
			# 	pass
		return trace_func

	@wraps(func)
	def wrapper(*args, **kwargs):

		# sys.settrace(trace_func)
		ret = func(*args, **kwargs)
		# sys.settrace(None)

		return ret
	return wrapper


class Counter(QtWidgets.QWidget):

	# @QRedux.store({
	# 	"count":{
	# 		"setter":0,
	# 		"getter":0,
	# 		"updater":0,
	# 	},
	# 	"mutations":[
	# 		"add",
	# 		"subtract",
	# 	],
	# 	"actions":{},
	# })

	_count = 0
	@property
	def count(self):
		print "get count"
		curr_frame = inspect.currentframe()
		caller_frame = curr_frame.f_back
		# print curr_frame.f_code.co_name
		# print inspect.getframeinfo(caller_frame)

		caller_code = caller_frame.f_code
		f_lineno = caller_frame.f_lineno
		print f_lineno
		# print inspect.getmodule(caller_code)

		# print inspect.getmembers(caller_frame)

		# NOTE get caller method name
		# curframe = inspect.currentframe()
		# calframe = inspect.getouterframes(curframe, 2)
		# print('caller name:', calframe[1][3])
		return self._count

	@count.setter
	def count(self,val):
		print "set count"
		self._count = val

	@initDeco
	def __init__(self):
		super(Counter,self).__init__()
	
		self.count = 0

		self.initialize()

	def initialize(self):
		
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)

		label = QtWidgets.QLabel()
		label.setText("<center>%s</center>" % self.count)

		plus_button = QtWidgets.QPushButton("+")
		minus_button = QtWidgets.QPushButton("-")

		label2 = QtWidgets.QLabel()
		label2.setText("<center>%s</center>" % self.count)

		layout.addWidget(label)
		layout.addWidget(plus_button)
		layout.addWidget(minus_button)
		layout.addWidget(label2)
		
		plus_button.clicked.connect(self.add)
		minus_button.clicked.connect(self.subtract)


	def add(self):
		self.count += 1

	def subtract(self):
		self.count -= 1

		
def main():
	app = QtWidgets.QApplication([])

	counter = Counter()
	counter.show()

	app.exec_()

if __name__ == "__main__":
	main()

# Vuex.Store({
# 	state: {
# 		count: 0
# 	},
# 	mutations: {
# 		add(state, payload) {
# 			payload ? (state.count += payload) : state.count++;
# 		},
# 		subtract(state, payload) {
# 			payload ? (state.count -= payload) : state.count--;
# 		}
# 	},
# 	actions: {
# 		addThreeAsync({ commit }) {
# 			setTimeout(() => commit('add', 3), 3000);
# 		}
# 	}
# }
