import tokenize_rt
from textwrap import dedent
code = dedent(u"""
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
    import os
    import sys
    import QMVVM

    class Counter(QtWidgets.QWidget):

        @QMVVM.store({
            r"state":{
                "text":"",
            },
        })
        def __init__(self):
            super(Counter,self).__init__()
            self.initialize()

        def initialize(self):
            layout = QtWidgets.QVBoxLayout()
            self.setLayout(layout)
        
            self.line = QtWidgets.QLineEdit()
            self.line.setText(self.state.text)
            label = QtWidgets.QLabel()
            layout.addWidget(self.line)
            layout.addWidget(label)
            
""")

def _is_f(token):
    import tokenize_rt

    prefix, _ = tokenize_rt.parse_string_literal(token.src)
    print tokenize_rt.parse_string_literal(token.src),token
    return 'f' in prefix.lower()

tokens = tokenize_rt.src_to_tokens(code)

to_replace = []
start = end = seen_f = None

for i, token in enumerate(tokens):
    # print token
    if start is None:
        if token.name == 'STRING':
            start, end = i, i + 1
            seen_f = _is_f(token)
    elif token.name == 'STRING':
        end = i + 1
        seen_f |= _is_f(token)
    elif token.name not in tokenize_rt.NON_CODING_TOKENS:
        if seen_f:
            to_replace.append((start, end))
        start = end = seen_f = None
