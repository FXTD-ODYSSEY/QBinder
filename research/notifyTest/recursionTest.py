# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-27 14:54:39'

"""

"""


def retrieveVal(val):
    
    itr = val.items() if type(val) is dict else enumerate(val) if type(val) is list else []
    for k,v in itr:        
        if isinstance(v, dict):
            retrieveVal(v)
            print v
        elif isinstance(v, list):            
            retrieveVal(v)
            print v

data = {
    1: {
        2: {
            "a": ['a',12,3,4],
            "b": [1]
        },
        3: {
            4: 5,
            6: 7
        }
    },
    2: {
        3: {
            4: 5
        },
        4: {
            6: 7
        }
    }
}

retrieveVal(data)
