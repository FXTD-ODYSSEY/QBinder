
## QBinder

> **Python Qt 数据绑定框架** [Wiki 文档](https://wiki.l0v0.com/Python/QBinder/)

---

## 概述


![todo 案例](//cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/01_example.gif)

> &emsp;&emsp;参考前端框架 Vue 的数据绑定概念，针对 Python Qt 框架实现更灵活的数据绑定和数据同步。     
> &emsp;&emsp;数据绑定对于样式更新、组件数据同步的使用情况非常方便，使用者只需要关注数据的变化，降低开发成本。    

## 使用概要

![edit 案例](//cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/02_edit.gif)

```py
import sys
from PySide2 import QtWidgets
from QBinder import Binder

# 构建绑定容器 & 变量
state = Binder()
state.text = "text"

app = QtWidgets.QApplication(sys.argv)

widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
widget.setLayout(layout)

edit = QtWidgets.QLineEdit()
label = QtWidgets.QLabel()
label2 = QtWidgets.QLabel()

# 使用 lambda 作为参数进行绑定
edit.setText(lambda:state.text)
label.setText(lambda:state.text)
label2.setText(lambda: "Exapmle Lable : %s" % state.text)

layout.addWidget(edit)
layout.addWidget(label)
layout.addWidget(label2)

widget.show()
app.exec_()
```

> &emsp;&emsp;通过 lambda 传递参数配合 binder 实例进行数据绑定。   
> &emsp;&emsp;操作简单，向前兼容，可配合 ui 文件使用，适配 Python 2 & 3    
> &emsp;&emsp;通用场景下自动实现双向数据绑定。    


## 应用场景

![remember 案例](//cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/03_remember.gif)

> &emsp;&emsp;自动存储和加载上次组件填写的数据。    
 
---

![slider 案例](//cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/04_slider.gif)

> &emsp;&emsp;slider 最大值最小值同步检测。    

---

![todo 案例](//cdn.jsdelivr.net/gh/FXTD-ODYSSEY/CG_wiki@gh-pages/Python/QBinder/_img/05_todo.gif)

[案例代码](https://github.com/FXTD-ODYSSEY/QBinder/blob/master/example/todo_app/todo.py)

> &emsp;&emsp;这个案例是模仿 Vue 文档提供的 todo MVC 案例做的 [链接](https://vuejs.org/v2/examples/todomvc.html)     
> &emsp;&emsp;配合 setStyleSheet 绑定样式表，实现样式动态更新。     
> &emsp;&emsp;可以在独立环境运行。     

## 特性

+ 利用 lambda 参数绑定数据 操作简单
+ 数据自动存储和记载
+ QEventHook 全局事件钩子
+ Python 2 & 3 兼容
+ 纯 Python 编写 兼容 DCC 软件

## 同步机制

> &emsp;&emsp;关于 QBinder 的前世今生以及 绑定的实现机制可以参阅我博客的文章 [链接](https://blog.l0v0.com/posts/301b3c35.html)


