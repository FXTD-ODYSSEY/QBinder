# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 22:39:01'

"""

"""


class Celsius(object):

    def __get__(self, instance, owner):
        print "get"
        return 5 * (instance.fahrenheit - 32) / 9

    def __set__(self, instance, value):
        print "set"
        instance.fahrenheit = 32 + 9 * value / 5


class Temperature(object):

    

    def __init__(self, initial_f):
        self.fahrenheit = initial_f
        self.celsius = Celsius()


t = Temperature(212)
print(t.celsius)
t.celsius = 0
t.celsius += 1
print(t.fahrenheit)