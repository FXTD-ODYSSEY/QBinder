import sys
MODULE = r"D:\Users\82047\Desktop\repo\QtConfig\QMVVM\_vender"
if MODULE not in sys.path:
    sys.path.append(MODULE)
import astroid
module = astroid.extract_node('''
def func(first, second):
    return first + second

arg_1 = 2
arg_2 = 3
func(arg_1, arg_2)
''')


# print(module)


def format_to_fstring_transform(node):
    
    f_string_node = astroid.JoinedStr(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
    )
    formatted_value_node = astroid.FormattedValue(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
    )
    formatted_value_node.postinit(value=node.args[0])

    # Removes the {} since it will be represented as
    # formatted_value_node
    string = astroid.Const(node.func.expr.value.replace('{}', ''))

    print node
    f_string_node.postinit(values=[string, formatted_value_node])
    node.keywords = "a"
    return astroid.Const(node.func.expr.value.replace('{}', ''))

def format_to_fstring_transform(node):
    f_string_node = astroid.JoinedStr(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
    )
    formatted_value_node = astroid.FormattedValue(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
    )
    print node
    print node.func
    print node.func.expr
    print node.func.expr.value
    formatted_value_node.postinit(value=node.args[0])

    # Removes the {} since it will be represented as
    # formatted_value_node
    string = astroid.Const(node.func.expr.value.replace('{}', ''))

    # f_string_node.postinit(values=[string, formatted_value_node])
    return string

astroid.MANAGER.register_transform(
    astroid.Call,
    format_to_fstring_transform,
)

tree = astroid.parse('''
"my name is {}".format(name)
''')
print(tree.as_string())