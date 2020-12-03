import os
import sys

try:
    import Qt
    import six

    # NOTE fix six version #issue4
    num = six.__version__.split(".")[1]
    if int(num) < 15:
        del six
        del sys.modules["six"]
        raise ImportError
except ImportError:
    DIR = os.path.dirname(__file__)
    MODULE = os.path.join(DIR, "_vendor")
    if MODULE not in sys.path:
        sys.path.insert(0, MODULE)
    import Qt
    import six

__version__ = "1.0.5"

from .util import ListGet
from .hook import HOOKS, hook_initialize
from .binding import Model, Binding, FnBinding
from .binder import GBinder, Binder, BinderCollector, BinderTemplate
from .eventhook import QEventHook
from .decorator import inject

# NOTE hook Qt caller to accept lambda argument
hook_initialize(HOOKS)
