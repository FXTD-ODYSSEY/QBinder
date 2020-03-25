# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-24 13:44:48'

"""

"""

import sys
import inspect

# NOTE https://stackoverflow.com/questions/4214936/

# intercept a function and retrieve the modifed values
def get_modified_values(target):
    def wrapper(*args, **kwargs):

        # get the applied args
        kargs = getcallargs(target, *args, **kwargs)
        print kargs
        # # get the source code
        # src = inspect.getsource(target)
        # lines = src.split('\n')


        # # oh noes string patching of the function
        # unindent = len(lines[0]) - len(lines[0].lstrip())
        # indent = lines[0][:len(lines[0]) - len(lines[0].lstrip())]

        # lines[0] = ''
        # lines[1] = indent + 'def _temp(_args, ' + lines[1].split('(')[1]
        # setter = []
        # for k in kargs.keys():
        #     setter.append('_args["%s"] = %s' % (k, k))

        # i = 0
        # while i < len(lines):
        #     indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        #     if lines[i].find('return ') != -1 or lines[i].find('return\n') != -1:
        #         for e in setter:
        #             lines.insert(i, indent + e)

        #         i += len(setter)

        #     elif i == len(lines) - 2:
        #         for e in setter:
        #             lines.insert(i + 1, indent + e)

        #         break

        #     i += 1

        # for i in range(0, len(lines)):
        #     lines[i] = lines[i][unindent:]

        # data = '\n'.join(lines) + "\n"

        # # setup variables
        # frame = inspect.currentframe()
        # loc = inspect.getouterframes(frame)[1][0].f_locals
        # glob = inspect.getouterframes(frame)[1][0].f_globals
        # loc['_temp'] = None


        # # compile patched function and call it
        # func = compile(data, '<witchstuff>', 'exec')
        # eval(func, glob, loc)
        # loc['_temp'](kargs, *args, **kwargs)

        # # there you go....
        # print kargs
        # # >> {'a': 10, 'b': 1223, 'f': 'Hello World'}

    return wrapper



# from python 2.7 inspect module
def getcallargs(func, *positional, **named):
    """Get the mapping of arguments to values.

    A dict is returned, with keys the function argument names (including the
    names of the * and ** arguments, if any), and values the respective bound
    values from 'positional' and 'named'."""
    args, varargs, varkw, defaults = inspect.getargspec(func)
    f_name = func.__name__
    arg2value = {}

    # The following closures are basically because of tuple parameter unpacking.
    assigned_tuple_params = []
    def assign(arg, value):
        if isinstance(arg, str):
            arg2value[arg] = value
        else:
            assigned_tuple_params.append(arg)
            value = iter(value)
            for i, subarg in enumerate(arg):
                try:
                    subvalue = next(value)
                except StopIteration:
                    raise ValueError('need more than %d %s to unpack' %
                                     (i, 'values' if i > 1 else 'value'))
                assign(subarg,subvalue)
            try:
                next(value)
            except StopIteration:
                pass
            else:
                raise ValueError('too many values to unpack')
    def is_assigned(arg):
        if isinstance(arg,str):
            return arg in arg2value
        return arg in assigned_tuple_params
    if inspect.ismethod(func) and func.im_self is not None:
        # implicit 'self' (or 'cls' for classmethods) argument
        positional = (func.im_self,) + positional
    num_pos = len(positional)
    num_total = num_pos + len(named)
    num_args = len(args)
    num_defaults = len(defaults) if defaults else 0
    for arg, value in zip(args, positional):
        assign(arg, value)
    if varargs:
        if num_pos > num_args:
            assign(varargs, positional[-(num_pos-num_args):])
        else:
            assign(varargs, ())
    elif 0 < num_args < num_pos:
        raise TypeError('%s() takes %s %d %s (%d given)' % (
            f_name, 'at most' if defaults else 'exactly', num_args,
            'arguments' if num_args > 1 else 'argument', num_total))
    elif num_args == 0 and num_total:
        raise TypeError('%s() takes no arguments (%d given)' %
                        (f_name, num_total))
    for arg in args:
        if isinstance(arg, str) and arg in named:
            if is_assigned(arg):
                raise TypeError("%s() got multiple values for keyword "
                                "argument '%s'" % (f_name, arg))
            else:
                assign(arg, named.pop(arg))
    if defaults:    # fill in any missing values with the defaults
        for arg, value in zip(args[-num_defaults:], defaults):
            if not is_assigned(arg):
                assign(arg, value)
    if varkw:
        assign(varkw, named)
    elif named:
        unexpected = next(iter(named))
        if isinstance(unexpected, unicode):
            unexpected = unexpected.encode(sys.getdefaultencoding(), 'replace')
        raise TypeError("%s() got an unexpected keyword argument '%s'" %
                        (f_name, unexpected))
    unassigned = num_args - len([arg for arg in args if is_assigned(arg)])
    if unassigned:
        num_required = num_args - num_defaults
        raise TypeError('%s() takes %s %d %s (%d given)' % (
            f_name, 'at least' if defaults else 'exactly', num_required,
            'arguments' if num_required > 1 else 'argument', num_total))
    return arg2value

def main():

    @get_modified_values
    def foo(a, f, b):
        print a, f, b

        a = 10
        if a == 2:
            return a

        f = 'Hello World'
        b = 1223

    e = 1
    c = 2
    foo(e, 1000, b = c)
    
main()