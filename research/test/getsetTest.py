# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 22:39:01'

"""

"""


class Int_validation(object):
    def __get__(self, instance, owner):
        print ("get")
        return  self.value
    def __set__(self, instance, value):
        print( "set")
        if  isinstance(value,int) and 0<value<100:
            self.value=value        #这个要注意 要用value，不能用instance 否则会陷入死循环
        else:
            print("请输入合法的数字")

class Student(object):
    age=Int_validation()

stu=Student()   
stu.age=50
print(stu.age)
