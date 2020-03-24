# https://gist.github.com/anonymous/4086770

import traceback

class Watcher(object):
    def __init__(self, obj=None, attr=None, log_file='log.txt', enabled=False):
        """
            Debugger that watches for changes in object attributes
            obj - object to be watched
            attr - string, name of attribute
            log_file - string, where to write output
        """

        self.log_file=log_file
        with open(self.log_file, 'wb'): pass
        if obj:
            self.value = getattr(obj, attr)
        self.obj = obj
        self.attr = attr
        self.enabled = enabled # Important, must be last line on __init__.

    def __call__(self, *args, **kwargs):
        kwargs['enabled'] = True
        self.__init__(*args, **kwargs)

    def check_condition(self):
        tmp = getattr(self.obj, self.attr)
        result = tmp != self.value
        self.value = tmp
        return result

    def trace_command(self, frame, event, arg):
        if not self.enabled:
            return self.trace_command
        if not self.check_condition():
            return self.trace_command
        if frame:
            with open(self.log_file, 'ab') as f:
                print >>f, "Value of",self.obj,".",self.attr,"changed!",self.value
                print >>f,"###### Before this line:"
                # print >>f,''.join(traceback.format_stack(frame))
        return self.trace_command


import os
import sys
watcher = Watcher()
sys.settrace(watcher.trace_command)

DIR = os.path.dirname(__file__)

class X(object):
    def __init__(self, foo):
        self.foo = foo

x = X(50)
watcher(x, 'foo', log_file=os.path.join(DIR,'log.txt'))
x.foo = 500
for val in range(100):
    x.foo = val