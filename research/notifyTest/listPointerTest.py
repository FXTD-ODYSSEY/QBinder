# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-28 16:30:33'

"""
https://stackoverflow.com/questions/36911164/
"""

class ListPointer(object):
    def __init__(self, myList,i=0):
         self.myList = myList
         self.i = i % len(self.myList)

    def __repr__(self):
         return 'ListPointer(' + repr(self.myList) + ',' + str(self.i) + ')'

    def __str__(self):
        return str(self.myList[self.i])

    def __call__(self,*value):
        if len(value) == 0:
            return self.myList[self.i]
        else:
            self.myList[self.i] = value[0]

def ListPointerTest1():
        
    foo = [2,3,4,5]
    this = ListPointer(foo,2)
    print this
    print foo
    this('ABC')
    print foo
    # TODO 存在瑕疵_(:з」∠)_
    foo.insert(0,1)
    print foo
    this('123')
    print foo


class Pointer(object):
    def __init__(self, value):
         self.value = value

    def __get__(self,instance,owner):
        print "get"
        return self.value

    def __set__(self,instance, value):
        print "set"
        self.value = value
    
    def __repr__(self):
         return 'FooWrapper(' + repr(self.value) + ')'
    def __str__(self):
        return str(self.value)
    def __call__(self,value):
        self.value = value

class Wrapper(object):
    pointer = Pointer(10)

def ListPointerTest2():
    vals = [1,2,3]
    vals[1] = Wrapper.pointer
    print vals
    # for x in vals: 
    #     print(x)
    Wrapper.pointer = 13
    print Wrapper.pointer
    # for x in vals: 
    #     print(x)
    vals.insert(0,1)
    vals = [x+1 for x in vals]



if __name__ == "__main__":
    ListPointerTest2()