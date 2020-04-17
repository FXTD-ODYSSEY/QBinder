
def addId(cls):

    class AddId(cls):

        def __init__(self, id, *args, **kargs):
            super(AddId, self).__init__(*args, **kargs)
            self.__id = id

        def getId(self):
            return self.__id

    return AddId

@addId
class Test(object):
    def __init__(self):
        print "test"

a = Test(1)
print a.getId()
