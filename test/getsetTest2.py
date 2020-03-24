# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 22:39:01'

"""

"""
from functools import wraps

# def store(options):
#     def handler(func):
        
#         @wraps(func)
#         def wrapper(self,*args, **kwargs):
#             for var in options:
#                 setattr(self,var,Celsius())
#             res = func(self,*args, **kwargs)
#             return res
#         return wrapper
#     return handler

class Celsius(object):

    def __get__(self, instance, owner):
        print "get"
        return 5 * (instance.fahrenheit - 32) / 9

    def __set__(self, instance, value):
        print "set"
        instance.fahrenheit = 32 + 9 * value / 5


class Temperature(object):

    # celsius = Celsius()
    def __init__(self, initial_f):
        self.fahrenheit = initial_f
        class Test(object):
            celsius = Celsius()
            data = {}
            for i in range(5):
                data['celsius_%s' % i] = Celsius() 
            locals().update(data)

        t = Test()
        print dir(t)
        t.celsius_0 += 0


t = Temperature(212)
# print(t.celsius)
# t.celsius = 0
# t.celsius += 1
# print(t.fahrenheit)