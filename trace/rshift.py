class TestProperty(object):
    def __init__(self,val=None):
        self.val = val

    def __set__(self,instance, value):
        self.val = value

    def __get__(self, instance, owner):
        return self.val

    def __rshift__(self,other):
        print "rshift Test",other

class Temperature(object):
    a = TestProperty(10)
    a >> 12 
    b = TestProperty(20)

temp=Temperature() 
print temp.a >> temp.b
print temp.a << temp.b

        