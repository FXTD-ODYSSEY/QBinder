# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-28 16:23:56'

"""

"""

import sys
from collections import OrderedDict

def notify(func):
    def wrapper(self,*args,**kwargs):
        # NOTE 更新数据
        res = func(self,*args,**kwargs)
        # NOTE 更新组件数据
        if hasattr(self,"STATE"):
            getattr(self.STATE.widget.state,"_%s_signal" % self.STATE.var).emit()
        return res
    return wrapper

class NotifyList(list):
    """
    https://stackoverflow.com/questions/13259179/list-callbacks
    监听数组的内置函数更新组件数据
    """
    def __init__(self,val,STATE):
        super(NotifyList, self).__init__(val)
        self.STATE = STATE

    extend = notify(list.extend)
    append = notify(list.append)
    remove = notify(list.remove)
    pop = notify(list.pop)
    __iadd__ = notify(list.__iadd__)
    __imul__ = notify(list.__imul__)

    #Take care to return a new NotifyList if we slice it.
    if sys.version_info[0] < 3:
        __setslice__ = notify(list.__setslice__)
        __delslice__ = notify(list.__delslice__)
        def __getslice__(self,*args):
            return self.__class__(list.__getslice__(self,*args))

    __delitem__ = notify(list.__delitem__)
    
    def __getitem__(self,item):
        if isinstance(item,slice):
            return self.__class__(list.__getitem__(self,item))
        else:
            return list.__getitem__(self,item)

    @notify
    def __setitem__(self,key,value):
        if isinstance(value, dict):
            value = NotifyDict(value,self.STATE)
        elif isinstance(value, list):
            value = NotifyList(value,self.STATE)
        list.__setitem__(self,key,value)
        
class NotifyDict(OrderedDict):
    """
    https://stackoverflow.com/questions/5186520/python-property-change-listener-pattern
    """
    def __init__(self,val,STATE):
        super(NotifyDict, self).__init__(val)
        self.STATE = STATE

    clear = notify(OrderedDict.clear)
    pop = notify(OrderedDict.pop)
    popitem = notify(OrderedDict.popitem)
    setdefault = notify(OrderedDict.setdefault)
    update =  notify(OrderedDict.update)
    __delitem__ = notify(OrderedDict.__delitem__)

    @notify
    def __setitem__(self,key,value):
        if hasattr(self,"STATE"):
            if isinstance(value, dict):
                value = NotifyDict(value,self.STATE)
            elif isinstance(value, list):
                value = NotifyList(value,self.STATE)
        return OrderedDict.__setitem__(self,key,value)
    

class BaseState(object):

    def sync(self):
        getattr(self.widget.state,"_%s_signal" % self.var).emit()

    def setVal(self,value):
        self.val = self.retrieve2Notify(value)
        self.sync()

    def retrieve2Notify(self,val,initialize=True):
        """
        遍历所有字典和数组对象，转换为 Notify 对象
        """
        itr = val.items() if type(val) is dict else enumerate(val) if type(val) is list else []
        for k,v in itr:        
            if isinstance(v, dict):
                self.retrieve2Notify(v,initialize=False)
                val[k] = NotifyDict(v,self)
            elif isinstance(v, list):            
                self.retrieve2Notify(v,initialize=False)
                val[k] = NotifyList(v,self)
        
        if initialize:
            if isinstance(val, dict):
                return NotifyDict(val,self)
            elif isinstance(val, list):
                return NotifyList(val,self)
            else:
                return val
