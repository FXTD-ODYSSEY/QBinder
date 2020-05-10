
import sys
import os

try:
    import Qt
    import six
except:
    DIR = os.path.dirname(__file__)
    MODULE = os.path.join(DIR,"_vendor")
    if MODULE not in sys.path:
        sys.path.append(MODULE)
    import Qt
    import six


from .QBinding import store,hookInitialize
from . import codec_wrapper as _codec
from .hook import HOOKS

hookInitialize()