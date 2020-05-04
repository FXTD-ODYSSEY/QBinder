# coding:utf-8
from __future__ import print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 21:12:08'

"""

"""

import re
import six
import codecs
import string
import encodings

from . import codec_parser
import QBinding


def sourceCodeHandler(func,*args):

    @six.wraps(func)
    def wrapper(source,*args,**kwargs):
        source , length = func(source,*args,**kwargs)
        source = codec_parser.parse(source)
        # exec source in globals(),locals()
        print('complete')
        # code = ast.parse(source)
        # print ast.dump(code)
        return source , length 

    return wrapper

def QBinding_search_function(encoding_name):
    QBinding = ''
    try:
        QBinding,encoding_name = encoding_name.split(";;")
    except ValueError:
        encoding_name = "utf-8"

    CODING = encodings.search_function(encoding_name)
    CODING.decode = sourceCodeHandler(CODING.decode) if "QBinding" in QBinding else CODING.decode

    CODING = codecs.CodecInfo(
        encode=CODING.encode,
        decode=sourceCodeHandler(CODING.decode),
        incrementalencoder=CODING.incrementalencoder,
        streamreader=CODING.streamreader,
        streamwriter=CODING.streamwriter,
    )

    return CODING

codecs.register(QBinding_search_function)