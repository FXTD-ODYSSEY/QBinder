# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 21:12:08'

"""

"""

import re
import codecs
import string
import encodings
from functools import wraps

import source_parser

import sys
MODULE = r"D:\Users\82047\Desktop\repo\QtConfig\QMVVM"
if MODULE not in sys.path:
    sys.path.append(MODULE)

# import QMVVM


def sourceCodeHandler(func,*args):

    @wraps(func)
    def wrapper(source,*args,**kwargs):
        source , length = func(source,*args,**kwargs)
        # source = source_parser.parse(source)
        exec source in globals(),locals()
        print 'complete'
        # code = ast.parse(source)
        # print ast.dump(code)
        return source , length 

    return wrapper

def QMVVM_search_function(encoding_name):
    QMVVM = ''
    try:
        QMVVM,encoding_name = encoding_name.split(";;")
    except ValueError:
        encoding_name = "utf-8"

    CODING = encodings.search_function(encoding_name)
    CODING.decode = sourceCodeHandler(CODING.decode) if "QMVVM" in QMVVM else CODING.decode

    CODING = codecs.CodecInfo(
        encode=CODING.encode,
        decode=sourceCodeHandler(CODING.decode),
        incrementalencoder=CODING.incrementalencoder,
        streamreader=CODING.streamreader,
        streamwriter=CODING.streamwriter,
    )

    return CODING



def test():
    
    codecs.register(QMVVM_search_function)
    
    from textwrap import dedent
    code = dedent("""
        from PySide2 import QtWidgets
        from PySide2 import QtCore
        from PySide2 import QtGui
        import os
        import sys
        import QMVVM

        class Counter(QtWidgets.QWidget):

            @QMVVM.store({
                "state":{
                    "text":"",
                },
                "actions":{
                    "@label2.setText":{
                        "args":["$count","count2"],
                        "mutation":lambda count,count2: "<center>%s %s</center>"%(count,count2),
                    },
                    "@label4.setText":{
                        "args":["$count","count3"],
                        "mutation":"calculate",
                    },
                },
            })
            def __init__(self):
                super(Counter,self).__init__()
                self.initialize()
    
                self.test()

            def initialize(self):
                layout = QtWidgets.QVBoxLayout()
                self.setLayout(layout)
            
                self.line = QtWidgets.QLineEdit()
                self.line.setText(self.state.text)
                line = QtWidgets.QLineEdit()
                line.setText(self.state.text)
                label = QtWidgets.QLabel()
                layout.addWidget(self.line)
                layout.addWidget(line)
                layout.addWidget(label)
                self.line = ''

            def test(self):
                print "123"

        class test(object):
            def __init__(self):
                print "test"
                
    """)
    
    text = code.decode('QMVVM;;utf-8')

if __name__ == '__main__':
    test()