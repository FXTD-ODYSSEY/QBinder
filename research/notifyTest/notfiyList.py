import sys

_pyversion = sys.version_info[0]

def callback_method(func):
    def notify(self,*args,**kwargs):
        for _,callback in self._callbacks:
            callback()
        return func(self,*args,**kwargs)
    return notify

class NotifyList(list):
    extend = callback_method(list.extend)
    append = callback_method(list.append)
    remove = callback_method(list.remove)
    pop = callback_method(list.pop)
    __delitem__ = callback_method(list.__delitem__)
    __setitem__ = callback_method(list.__setitem__)
    __iadd__ = callback_method(list.__iadd__)
    __imul__ = callback_method(list.__imul__)

    #Take care to return a new NotifyList if we slice it.
    if _pyversion < 3:
        __setslice__ = callback_method(list.__setslice__)
        __delslice__ = callback_method(list.__delslice__)
        def __getslice__(self,*args):
            return self.__class__(list.__getslice__(self,*args))

    def __getitem__(self,item):
        if isinstance(item,slice):
            return self.__class__(list.__getitem__(self,item))
        else:
            return list.__getitem__(self,item)

    def __init__(self,*args):
        list.__init__(self,*args)
        self._callbacks = []
        self._callback_cntr = 0

    def register_callback(self,cb):
        self._callbacks.append((self._callback_cntr,cb))
        self._callback_cntr += 1
        return self._callback_cntr - 1

    def unregister_callback(self,cbid):
        for idx,(i,cb) in enumerate(self._callbacks):
            if i == cbid:
                self._callbacks.pop(idx)
                return cb
        else:
            return None


if __name__ == '__main__':
    A = NotifyList(range(10))
    def cb():
        print ("Modify!")

    #register a callback
    cbid = A.register_callback(cb)

    A.append('Foo')
    A += [1,2,3]
    A *= 3
    A[1:2] = [5]
    del A[1:2]

    #Add another callback.  They'll be called in order (oldest first)
    def cb2():
        print ("Modify2")
    A.register_callback(cb2)
    print ("-"*80)
    A[5] = 'baz'
    print ("-"*80)

    #unregister the first callback
    A.unregister_callback(cbid)

    A[5] = 'qux'
    print ("-"*80)

    print (A)
    print (type(A[1:3]))
    print (type(A[1:3:2]))
    print (type(A[5]))