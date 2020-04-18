# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 21:12:27'

"""
正则表达式 提取分析源码
"""

import re
import time

def printTime(func):
    def wrapper(*args, **kwargs):
        cur = time.time()
        res = func(*args, **kwargs)
        print "elapsed time:",time.time() - cur
        return res
    return wrapper

def getClassContent(source):
    reg = r'''
        (\d{5}?)\|class\s+(\S+?)\s*?\((.*?)\):    (?# 匹配类名和继承)
        ((?:.|\n)*?)                                       (?# 匹配换行符或者任意内容)
        (?:(\d{5}?)\|\S|\Z)
    '''
    # start_lineno,class_name,class_type,class_content,end_lineno = re.findall(re.compile(reg,re.X|re.M),source)
    match = re.findall(re.compile(reg,re.X|re.M),source)
    return match

def getQMVVMDecorator(content):
    reg = r'''
        @(?:QMVVM\.store|store)\s*?\(((?:.|\n)*)\)     (?# 匹配 QMVVM sotre 装饰器 | 获取传入的参数)
        (?:.|\n)*?
        \d{5}?\|(\s*)def\ +__init__.*?:                      (?# 匹配 __init__)
        ((?:.|\n)*?)\d{5}?\|\2(?:\Z|\S)                     (?# 匹配 __init__函数内部的代码 基于缩进)
    '''
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match
    
def getInitDef(init):
    reg = r'''
        self\.(\S*?)\(  (?# 匹配执行的函数)
    '''
    match = re.findall(re.compile(reg,re.X|re.M),init)
    return match

def getDefContent(Def,content):
    reg = r'''
        \d{5}?\|(\s*?)def\ *%s\((?:.*?)\):
        ((?:.|\n)*?)(?:\Z|\d{5}?\|\1\S)   
    ''' % Def 
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match[0][1] if match else ''

    # match = match if match else []
    # return [m for i,m in match]

def getStateRelationship(content):
    reg = r'''
        (\S*?)\(self\.state\.(\S*?)\)
    '''
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match

def getWidgetType(widget,content):
    reg = r'''
        (\d{5}?)\|\s*%s\s*=\s*(\S*)
    ''' % widget
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match

def getDefCall(content):
    reg = r'''
        (\S*?)\s*?\((.*)\)
    '''
    return {method:arg for method,arg in re.findall(re.compile(reg,re.X|re.M),content) if "." in method and arg}

def getDefCall(content):
    reg = r'''
        (\S*?)\s*?\((.*)\)
    '''
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return {method:arg for method,arg in re.findall(re.compile(reg,re.X|re.M),content) if "." in method and arg}

# @printTime
def parse(source):
    # NOTE 加入行号
    lineno_source = '\n'.join('%s|%s' % (str(i).zfill(5),line) for i,line in enumerate(source.split("\n"),1))
    # NOTE 清空注释
    lineno_source = re.sub(r'[ \t\r\f]*?(#.*)','',lineno_source)
    for start_lineno,class_name,class_type,class_content,end_lineno in getClassContent(lineno_source):
        match = getQMVVMDecorator(class_content)
        if not match:continue
        option,_,init = match[0]
        # NOTE 获取 init 下相关的所有函数内容
        all_def_content = init
        for Def in getInitDef(init):
            def_content = getDefContent(Def,class_content)
            all_def_content += '\n%s' % def_content
    
        # NOTE 截取所有带参数的 Def 
        methods = {}
        for method,arg in getDefCall(all_def_content).items():
            print method,arg
            # NOTE 如果没有 self 则将 method 转为 local
            if not method.startswith("self."):
                method = "@%s" % method
            
            
        
        # # print all_def_content
        # binding = {}
        # for setter,state in state_list:
        #     widget,_,_ = setter.rpartition(".")
        #     if not binding.has_key(state):
        #         binding[state] = []
            
        #     widget = widget[5:] if widget.startswith("self.") else "@%s" % widget
            
        #     binding[state].append(widget)
        #     # # NOTE 判断是否存在变量多次赋值的情况
        #     # for lineno,valuewidget_type in getWidgetType(widget,all_def_content)
        #     #     pass
        
        
        # # NOTE 去掉行号 并且 转换为 字典
        # option = eval('\n'.join([line for line in re.split("\d{5}?\|",option)]))
        # for state,val in option["state"].items():
        #     val = val() if callable(val) else val
            

    return lineno_source