import os
import sys

try:
    import Qt
    import six
except:
    DIR = os.path.dirname(__file__)
    MODULE = os.path.join(DIR, "_vendor")
    if MODULE not in sys.path:
        sys.path.insert(0,MODULE)
    import Qt
    import six


from .util import ListGet
from .hook import HOOKS, hook_initialize
from .binding import Model, Binding, FnBinding
from .binder import GBinder, Binder, BinderCollector, BinderTemplate
from .eventhook import QEventHook
from .decorator import inject


# NOTE hook Qt caller to accept lambda argument
hook_initialize(HOOKS)
