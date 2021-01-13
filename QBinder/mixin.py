# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-19 00:05:51"

import six
from .binder import Binder, BinderBase
from Qt import QtCore


class ItemMeta(type(QtCore.QObject)):
    def __new__(cls, name, bases, attrs):
        init = attrs.get("__init__")
        if init:
            binder_dict = {
                name: binder
                for name, binder in attrs.items()
                if isinstance(binder, BinderBase)
            }
            attrs["__init__"] = cls.init_deco(init, binder_dict)

        return super(ItemMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def init_deco(cls, func, binder_dict):
        @six.wraps(func)
        def wrapper(self, *args, **kwargs):
            # NOTE inject class binder to self binder
            # TODO FnBinding point to self
            name = ""
            for name, binder in binder_dict.items():
                _binder = Binder()
                for k, v in binder._var_dict_.items():
                    setattr(_binder, k, v)
                setattr(self, name, _binder)

            return func(self, *args, **kwargs)

        return wrapper


@six.add_metaclass(ItemMeta)
class ItemMixin(object):
    __binder__ = ""
    __data__ = {}
    __items__ = []
    __filter__ = []
    __layout__ = None
