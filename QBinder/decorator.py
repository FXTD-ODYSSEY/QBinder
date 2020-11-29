# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-15 20:56:50"

import six
import inspect
from .binder import Binder
from functools import wraps


def inject(binder):
    frame = inspect.currentframe().f_back
    for name, v in frame.f_locals.items():
        if v is binder:
            break

    def caller(func):
        @six.wraps(func)
        def wrapper(self, *args, **kwargs):
            # NOTE inject class binder to self binder
            # TODO FnBinding point to self
            _binder = Binder()
            for k, v in binder._var_dict_.items():
                setattr(_binder, k, v)
            setattr(self, name, _binder)
            res = func(self, *args, **kwargs)
            return res

        return wrapper

    return caller
