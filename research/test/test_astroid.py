import sys
MODULE = r"D:\Users\82047\Desktop\test"
if MODULE not in sys.path:
    sys.path.append(MODULE)

from astroid import parse
module = parse('''
def func(first, second):
    return first + second

arg_1 = 2
arg_2 = 3
func(arg_1, arg_2)
''')

print module.body[-1]