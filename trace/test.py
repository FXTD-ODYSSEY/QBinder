import inspect
from abc import ABCMeta
print dir(ABCMeta)
def func():
        
    frame_stack = inspect.getouterframes(inspect.currentframe())
    # code_context = frame_stack[1].code_context[0]
    # print code_context
    print frame_stack
    # is_return_value_assigned = re.match(r"[\w+ ,]*=", code_context) is not None
    # if return_value_assigned():
    #      print("yes")
    # else:
    #      print("no")
    return 0

# this should print "no"
func()

# this should print "yes"
a = func()
