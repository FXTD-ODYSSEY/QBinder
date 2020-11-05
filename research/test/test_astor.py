# coding:utf-8

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-03-29 23:23:16"

"""
https://zhuanlan.zhihu.com/p/21945624
"""

import sys

MODULE = r"D:\Users\82047\Desktop\repo\QtConfig\QBinding\_vender"
if MODULE not in sys.path:
    sys.path.append(MODULE)

import ast
import astor

expr = """
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import os
import sys
# import QBinding
from QBinder import store

class Counter(QtWidgets.QWidget):

    @store({
        "state":{
            "text":"",
        },
    })
    def __init__(self):
        super(Counter,self).__init__()
        print self.state.text
        self.initialize()

    def initialize(self):
        import traceback
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
    
        self.line = QtWidgets.QLineEdit()
        self.line.setText(self.state.text)
        label = QtWidgets.QLabel()
        label.setText(self.state.text)
        layout.addWidget(self.line)
        layout.addWidget(label)
"""
p = ast.parse(expr)


class QBindingImportParser(ast.NodeVisitor):
    import_dict = {}

    def visit_ImportFrom(self, node):
        module = node.module
        alias = node.names[0]
        var = alias.asname if alias.asname else alias.name
        self.import_dict[var] = "%s.%s" % (module, var)

    def visit_Import(self, node):
        alias = node.names[0]
        var = alias.asname if alias.asname else alias.name
        self.import_dict[var] = var


class QBindingDecoratorParser(ast.NodeVisitor):

    store_option = []

    def __init__(self, import_dict):
        self.import_dict = import_dict

    def visit_ClassDef(self, node):
        class_func_dict = []
        print node
        for n in ast.iter_child_nodes(node):
            if isinstance(n, ast.FunctionDef):
                if n.name == "__init__":
                    # NOTE 遍历查询 QBinding 装饰器
                    for decorator in n.decorator_list:
                        if isinstance(decorator.func, ast.Name):
                            name = decorator.func.id
                        elif isinstance(decorator.func, ast.Name):
                            name = decorator.func.value.id

                        if "QBinding" in self.import_dict[name]:
                            self.store_option.append(decorator.args)
                            break
                for n in ast.iter_child_nodes(n):
                    if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Call):
                        continue
                    for arg in n.value.args:
                        if not isinstance(arg, ast.Attribute):
                            continue
                        value = arg.value
                        if (
                            isinstance(value, ast.Attribute)
                            and value.attr == "state"
                            and value.value.id == "self"
                        ):
                            attr = arg.attr
                            func = n.value.func
                            print attr, func.lineno
                            break


class QBindingCallParser(ast.NodeVisitor):

    store_option = None

    def __init__(self, import_dict):
        self.import_dict = import_dict

    def visit_Call(self, node):
        print node
        if isinstance(node.value, ast.Name) and node.value.id == "self":
            print dir(node)


import_parser = QBindingImportParser()
import_parser.visit(p)
deco_parser = QBindingDecoratorParser(import_parser.import_dict)
deco_parser.visit(p)


deco_parser.store_option


# print astor.dump(p)
# p.body[0].body = [ ast.parse("return 42").body[0] ] # Replace function body with "return 42"

# print(astor.to_source(p))