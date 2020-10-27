
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


from .hook import HOOKS,hookInitialize,hook_dict
from .init import init

hookInitialize()