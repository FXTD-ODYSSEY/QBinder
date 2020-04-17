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
MODULE = r"C:\Users\timmyliang\Desktop\repo\QtConfig\QMVVM"
if MODULE not in sys.path:
    sys.path.append(MODULE)

import QMVVM


def sourceCodeHandler(func,*args):

    @wraps(func)
    def wrapper(source,*args,**kwargs):
        source , length = func(source,*args,**kwargs)
        source = source_parser.parse(source)
        # exec source in globals(),locals()
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

codecs.register(QMVVM_search_function)