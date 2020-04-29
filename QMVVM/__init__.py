
import sys
import os

try:
    import Qt
except:
    DIR = os.path.dirname(__file__)
    MODULE = os.path.join(DIR,"_vender")
    if MODULE not in sys.path:
        sys.path.append(MODULE)
    import Qt

from . import codec_wrapper as _codec
from .hook import HOOKS
from .QMVVM import store
