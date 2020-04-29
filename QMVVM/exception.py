# coding:utf-8
from __future__ import print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-19 09:03:20'

"""
解析错误类型
"""
import os
import sys
# from codecs import open
import linecache
import re

from .codec_parser import getQMVVMDecorator,getClassContent

def returnSelfWrapper(func):
    def wrapper(self,*args, **kwargs):
        func(self,*args, **kwargs)
        return self
    return wrapper

def getCallable(content):
    reg = r'''
        \=\s*?(\S*?)\(  
    '''
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match[0] if match else None

def getClass(key,content):
    reg = r'''
        class\s+?%s\s*?(?:\(|\:)
    ''' % key
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match[0] if match else None

def getErrorLine(key,content):
    reg = r'''
        (\S*?)\|\s*?(?:\'|\")\s*?%s\s*?(?:\'|\")\s*?\:
    ''' % key
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match[0] if match else -1

class SchemeParseError(Exception,object):

    @returnSelfWrapper
    def parseErrorLine(self,option,err=None):
        option = {"method":option} if type(option) is str else option
        frame = sys._getframe().f_back.f_back.f_back
        file_path = os.path.realpath(frame.f_code.co_filename)

        if not os.path.exists(file_path):
            print ("*> cannot find the source code")
            return

        err_line = linecache.getline(file_path,frame.f_lineno)
        class_name = getCallable(err_line)

        lineno_source = "".join(["%s|%s" % (str(n).zfill(5),line) for n,line in enumerate(linecache.getlines(file_path))])
        lineno_source = re.sub(r'[ \t\r\f]*?(#.*)','',lineno_source)

        # TODO support import module trace
        if not getClass(class_name,lineno_source):
            print ("*> trace fail | cannot find the class in the file\nfile_path: %s\nclass_name: %s" % (file_path,class_name) )
            return

        # NOTE 说明当前文件存在 class
        for start_lineno,_class_name,class_type,class_content,end_lineno in getClassContent(lineno_source):
            if class_name != _class_name: continue
            match = getQMVVMDecorator(class_content)
            if not match:continue
            QMVVM_option,_,_ = match[0]
            break
        else:
            print ("*> trace fail | cannot find the QMVVM option\nfile_path: %s\nclass_name: %s" % (file_path,class_name) )
            return
        
        # NOTE 获取报错出行号
        method = option.get("method")
        lineno = int(getErrorLine(method,QMVVM_option)) + 1
        if not lineno:
            print ("*> trace fail | cannot find the error line\nfile_path: %s\nclass_name: %s" % (file_path,class_name) )
            return

        err_print = ["%-5s%-2s%s" % (l,'' if l != lineno else '->',linecache.getline(file_path,l)) for l in range(lineno-2,lineno+3)]
        print ('*> "%s", line %s' % (file_path,lineno))
        print ("".join(err_print))
        if err:
            raise err