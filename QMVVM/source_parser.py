# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 21:12:27'

"""

"""

import re
import pprint
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

def parse(source):
    lineno_source = '\n'.join('%s|%s' % (str(i).zfill(5),line) for i,line in enumerate(source.split("\n"),1))
    for start_lineno,class_name,class_type,class_content,end_lineno in getClassContent(lineno_source):
        match = getQMVVMDecorator(class_content)
        if not match:continue
        option,_,init = match[0]
        state_list = getStateRelationship(init)
        all_def_content = init
        for Def in getInitDef(init):
            def_content = getDefContent(Def,class_content)
            all_def_content += '\n%s' % def_content
            state_list.extend(getStateRelationship(def_content))

        # print all_def_content
        binding = {}
        for setter,state in state_list:
            widget,_,_ = setter.rpartition(".")
            if not binding.has_key(state):
                binding[state] = []
            
            widget = widget[5:] if widget.startswith("self.") else "@%s" % widget
            
            binding[state].append(widget)
            # # NOTE 判断是否存在变量多次赋值的情况
            # for lineno,valuewidget_type in getWidgetType(widget,all_def_content)
            #     pass
        
        
        # # NOTE 去掉行号 并且 转换为 字典
        # option = eval('\n'.join([line for line in re.split("\d{5}?\|",option)]))
        # for state,val in option["state"].items():
        #     val = val() if callable(val) else val
            

        print binding
        # print state_list
    
    return source