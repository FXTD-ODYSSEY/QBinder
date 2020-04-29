# coding:utf-8
from __future__ import print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-29 14:51:13'

"""
https://stackoverflow.com/questions/45337189/can-you-assign-variables-in-a-lambda
"""

class Test():
    val = 1
    val2 = 10
    
test = Test()
print (test.val,test.val2)

a = lambda cls: [None for test.val2 in [test.val]]
a(test)


b = lambda cls: exec('cls.val2 = 3')
b(test)
print (test.val,test.val2)