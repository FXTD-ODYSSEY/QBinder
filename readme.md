
## QBinder

> **Python Qt Data Binding Framework** [Wiki Documentation](https://wiki.l0v0.com/Python/QBinder/)

---

## Overview


![todo](https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/01_example.gif)

> &emsp;&emsp;Refer to the data binding concept of front-end framework Vue for more flexible data binding and data synchronization for the Python Qt framework.  
> &emsp;&emsp;Data binding is very convenient for style updates and component data synchronization, and user only need to pay attention to data changes and reduce development costs.

## How To Use

![edit 案例](https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/02_edit.gif)

```py
import sys
from PySide2 import QtWidgets
from QBinder import Binder

# NOTES: Create a Data Container
state = Binder()
state.text = "text"

app = QtWidgets.QApplication(sys.argv)

widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
widget.setLayout(layout)

edit = QtWidgets.QLineEdit()
label = QtWidgets.QLabel()
label2 = QtWidgets.QLabel()

# NOTES: Use Lambda mark the binding data
edit.setText(lambda: state.text)
label.setText(lambda: state.text)
label2.setText(lambda: "Exapmle Lable : %s" % state.text)

layout.addWidget(edit)
layout.addWidget(label)
layout.addWidget(label2)

widget.show()
app.exec_()
```

> &emsp;&emsp;Data binding with binder instances is done with lambda pass parameters.  
> &emsp;&emsp;Simple to operate, forward compatible, and works with ui files to fit Python 2 and 3  
> &emsp;&emsp;Two-way data binding is automatically implemented in a common scenario.     


## The scenario  

![remember](https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/03_remember.gif)

> &emsp;&emsp;Automatic storage and loading of data filled in by the last input.  
 
---

![slider](https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/04_slider.gif)

> &emsp;&emsp;slider detect the min max value    

---

![todo](https://cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/05_todo.gif)

[source code](https://github.com/FXTD-ODYSSEY/QBinder/blob/master/example/todo_app/todo.py)

> &emsp;&emsp;This case is mimic the todo MVC example provided in the Vue documentation [link](https://vuejs.org/v2/examples/todomvc.html)     
> &emsp;&emsp;Work with setStyleSheet binding style sheets for dynamic style updates.   
> &emsp;&emsp;It can run in a stand-alone environment.       

## Features

+ Binding data with lambda parameters is simple  
+ Data is automatically dumped and loaded  
+ QEventHook for global event hook  
+ Compat Python 2 & 3
+ Pure Python, fully support [DCC](https://vfxplatform.com/about/) software & Qt Designer

