from .listget import ListGet
from .collapsible import CollapsibleWidget
from collections import defaultdict

# NOTE https://stackoverflow.com/a/8702435
nestdict = lambda: defaultdict(nestdict)
