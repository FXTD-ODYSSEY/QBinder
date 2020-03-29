# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-29 23:23:16'

"""
https://zhuanlan.zhihu.com/p/21945624
"""

import sys
MODULE = r"D:\Users\82047\Desktop\repo\QtConfig\QMVVM\_vender"
if MODULE not in sys.path:
    sys.path.append(MODULE)

import ast
import astor

expr="""
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import os
import sys
# import QMVVM
from QMVVM import store

class Counter(QtWidgets.QWidget):

    @store({
        "state":{
            "text":"",
        },
    })
    def __init__(self):
        super(Counter,self).__init__()
        self.initialize()

    def initialize(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
    
        self.line = QtWidgets.QLineEdit()
        self.line.setText(self.state.text)
        label = QtWidgets.QLabel()
        label.setText(self.state.text)
        layout.addWidget(self.line)
        layout.addWidget(label)
"""
p=ast.parse(expr)

class QMVVMParser(ast.NodeVisitor):

    import_dict = {}
    store_option = None

    def visit_ImportFrom(self,node):
        module = node.module
        alias = node.names[0]
        var = alias.asname if alias.asname else alias.name
        self.import_dict[var] = "%s.%s" % (module,var)

    def visit_Import(self,node):
        alias = node.names[0]
        var = alias.asname if alias.asname else alias.name
        self.import_dict[var] = var
        
    def visit_ClassDef(self, node):
        class_func_dict = []
        for n in ast.iter_child_nodes(node):
            if not isinstance(n, ast.FunctionDef):
                continue

            # TODO 查询 组件 赋值关系
            
            if n.name != "__init__":
                continue
            # NOTE 遍历查询 QMVVM 装饰器
            for decorator in n.decorator_list:
                if isinstance(decorator.func, ast.Name):
                    name = decorator.func.id
                elif isinstance(decorator.func, ast.Name):
                    name = decorator.func.value.id

                if "QMVVM" in self.import_dict[name]:
                    store_option = decorator.args
                    break
            


parser = QMVVMParser()
parser.visit(p)


# print astor.dump(p)
# p.body[0].body = [ ast.parse("return 42").body[0] ] # Replace function body with "return 42"

print(astor.to_source(p))