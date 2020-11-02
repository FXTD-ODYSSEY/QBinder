import os
import sys

try:
    import Qt
    import six
except:
    DIR = os.path.dirname(__file__)
    MODULE = os.path.join(DIR, "_vendor")
    if MODULE not in sys.path:
        sys.path.append(MODULE)
    import Qt
    import six


from .hook import HOOKS,hook_initialize
# from .init import init
from .type import Binder, connect_binder

hook_initialize()