# coding:utf-8
from __future__ import division, print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-04-29 17:07:57"

"""

"""

import os
import sys

from functools import wraps, partial
from collections import OrderedDict

DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR, "..")
if MODULE not in sys.path:
    sys.path.append(MODULE)
from QBinder import Binder

state = Binder()
state.num = 1

print(type(state.num))
# int
print(type(state["num"]))
# Binding