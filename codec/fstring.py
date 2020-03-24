# -*- coding: future_fstrings -*-
# import pdb;pdb.set_trace()

test = 'asdas'
test0 = 'asdas'
test1 = 'asdas'
test2 = 'asdas'
thing = 'world'


# fstring = 'f"hello {text}"'.decode('future-fstrings')

print "=========================="
# print(fstring)
print_string =  f"yes {test2}"
print print_string

import ast
func_def = \
"""
def add(x, y):
    return x + y
print add(3, 5)
"""
r_node = ast.parse(func_def)

print ast.dump(r_node)