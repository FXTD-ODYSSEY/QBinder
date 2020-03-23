# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-23 21:26:03'

"""

"""

import sys

def trace_dispatch(frame,event,arg):
    # NOTE 获取局部变量 a 并修改变量
    # value = frame.f_locals["a"]
    # print value
    # print "value",value
    print "event",event
    print "arg",arg
    return trace_dispatch


def f(a):
    print a

if __name__ == "__main__":
    sys.settrace(trace_dispatch)
    # for i in range(0,5):
    #     f(i)
    a = 3
    b = []
    f(3)
    sys.settrace(None)
    

# NOTE 输出 ↓↓↓
# NOTE 1
# NOTE 1
# NOTE 3
# NOTE 3
# NOTE 5