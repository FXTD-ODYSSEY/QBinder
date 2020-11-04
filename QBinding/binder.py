# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-04 15:30:25"

import inspect
from contextlib import contextmanager
from .type import BinderBase, GBinder, Binding


@contextmanager
def init_binder(singleton=False):
    binder = BinderBase()
    yield binder

    # NOTE get the outer frame
    stacks = inspect.stack()
    frame = stacks[2][0]

    _var_dict_ = {n: s for n, s in inspect.getmembers(binder) if isinstance(s, Binding)}

    if singleton:
        for n, s in _var_dict_.items():
            setattr(GBinder, n, s)
        GBinder._var_dict_.update(_var_dict_)
        cls = GBinder
    else:
        _var_dict_.update({"_var_dict_": _var_dict_})

        class Binder(BinderBase):

            locals().update(_var_dict_)

            def __setattr__(self, key, value):
                binding = self._var_dict_.get(key)
                binding.set(value)

        cls = Binder

    # NOTE add to the local dict
    for k, v in frame.f_locals.items():
        if binder is v:
            frame.f_locals.update({k: cls()})
            break