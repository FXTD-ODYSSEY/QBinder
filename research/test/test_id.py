# -*- coding: utf-8 -*-
"""
https://blog.csdn.net/majian/article/details/109386757

https://stackoverflow.com/questions/41186818/how-to-generate-a-random-uuid-which-is-reproducible-with-a-seed-in-python
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-06 22:51:41'


import uuid
import random

rd = random.Random()
rd.seed(0)
val = uuid.UUID(int=rd.getrandbits(128))
print(dir(val))
print(val.hex)
print(type(val.hex))
print(val.int)
print(type(val.int))
val = uuid.UUID(int=rd.getrandbits(128))
print(val)
