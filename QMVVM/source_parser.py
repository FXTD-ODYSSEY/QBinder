# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 21:12:27'

"""

"""

import re

def getClassContent(source):
    keyword = "class "

    class_content_split_list = []
    # Note 清空无关class的文件信息
    check = False
    split_string = ""
    for line in source.split("\n"):
        if line.startswith("class"):
            split_string += "\n" + line + "\n"
            check = True
        # Note 清除if开头的语句
        elif line.startswith("if") or line.startswith("def"):
            check = False

        if check and line.startswith(" "):
            split_string += line + "\n"

    split_list = re.split(r"\s%s"%keyword, split_string)
    for i,content in enumerate(split_list):
        if not content:
            continue
        elif i!=0:
            # Note 获取切除之后 class 之前的字符串信息
            tmp = split_list[i-1].split("\n")[-1]
            # Note 将文件的内容切成数组 每个元素只有一个class
            class_content_split_list.append(tmp + keyword + content)
        else:
            class_content_split_list.append(content)

    return class_content_split_list

def getQMVVMDecorator(content):
    reg = r'''
        ^class(.*?)\((.*?)\):                       (?# 匹配类名和继承)
        (?:.|\n)*?                                  (?# 匹配换行符或者任意内容)
        @(?:QMVVM\.store|store)\(((?:.|\n)*?)\)     (?# 匹配 QMVVM sotre 装饰器 | 获取传入的参数)
        (\s*)def\s*__init__.*?:                      (?# 匹配 __init__)
        ((?:.|\n)*?)\4(?:\Z|\S)                     (?# 匹配 __init__函数内部的代码 基于缩进)
    '''
    match = re.match(re.compile(reg,re.X|re.M),content)
    return match
    
def getInitDef(init):
    reg = r'''
        self\.(\S*?)\(  (?# 匹配执行的函数)
    '''
    match = re.findall(re.compile(reg,re.X|re.M),init)
    return match

def getDefContent(Def,content):
    # TODO 获取 Def 内容
    reg = r'''
        (\s*)def\s*%s\(.*?\):\n
        \1\1(.*?)
    ''' % Def
    print content
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match

def getStateRelationship(content):
    reg = r'(\S*?)\(self\.state\.(\S*?)\)'
    match = re.findall(re.compile(reg,re.X|re.M),content)
    return match

def parse(source):
    for class_content in getClassContent(source):
        match = getQMVVMDecorator(class_content)
        if not match:continue
        class_name = match.group(1).strip()
        class_type = match.group(2).strip()
        option = match.group(3).strip()
        init = match.group(5)
        state_list = getStateRelationship(init)
        
        for Def in getInitDef(init):
            print getDefContent(Def,class_content)
            # state_list.extend(getStateRelationship(Def))
            # print match
    
    return source