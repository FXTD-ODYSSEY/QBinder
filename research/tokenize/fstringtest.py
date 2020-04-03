import tokenize_rt
from textwrap import dedent
code = dedent(u"""
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
    import os
    import sys
    import QMVVM
    hello = "yes"
    test = f"happy {hello}"

    data = f'''
        common {test}
    '''

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

def _fstring_parse_outer(s, i, level, parts, exprs):
    print "_fstring_parse_outer before",s
    for q in ('"' * 3, "'" * 3, '"', "'"):
        if s.startswith(q):
            s = s[len(q):len(s) - len(q)]
            break
    else:
        raise AssertionError('unreachable')
    parts.append(q)
    print "_fstring_parse_outer after",s
    # ret = _fstring_parse(s, i, level, parts, exprs)
    # parts.append(q)
    return ret

def _make_fstring(tokens):
    import tokenize_rt

    new_tokens = []
    exprs = []

    for i, token in enumerate(tokens):
        if token.name == 'STRING' and _is_f(token):
            prefix, s = tokenize_rt.parse_string_literal(token.src)
            parts = []
            _fstring_parse_outer(s, 0, 0, parts, exprs)
      
            if 'r' in prefix.lower():
                parts = [s.replace('\\', '\\\\') for s in parts]
            token = token._replace(src=''.join(parts))
        elif token.name == 'STRING':
            new_src = token.src.replace('{', '{{').replace('}', '}}')
            token = token._replace(src=new_src)
        new_tokens.append(token)

    # exprs = ('({})'.format(expr) for expr in exprs)
    # format_src = '.format({})'.format(', '.join(exprs))
    # new_tokens.append(tokenize_rt.Token('FORMAT', src=format_src))

    return new_tokens

def _is_f(token):
    import tokenize_rt

    prefix, _ = tokenize_rt.parse_string_literal(token.src)
    # print tokenize_rt.parse_string_literal(token.src),token
    return 'f' in prefix.lower()

tokens = tokenize_rt.src_to_tokens(code)

to_replace = []
start = end = seen_f = None

for i, token in enumerate(tokens):
    print token
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

print to_replace

for start, end in reversed(to_replace):
    tokens[start:end] = _make_fstring(tokens[start:end])
#     return tokenize_rt.tokens_to_src(tokens), length
