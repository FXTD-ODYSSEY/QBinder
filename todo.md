## todolist

- [ ] ~~模仿 vuex 添加 Binder action commit~~
- [ ] 制作类似 vue-devtools 的调试面板 (mpdb 面板)
- [ ] 参考 Vue & Velocity 动画管理
- [ ] 使用 Qt State Machine 管理状态变化
- [ ] 用户任意扩展 handler
- [ ] Model 实现可扩展
- [ ] combobox update delay

- [ ] doc string 补充 | 生成 sphinx 
- [ ] english readme

- [x] drap drop test
- [x] dict load order

- [x] 单例模式 - 数据全局共享
- [x] 数据 dump 输入输出
- [x] 自动加载上次的配置 利用 QTimer 0 timeout 实现 idle 执行 https://doc.qt.io/qtforpython/PySide2/QtCore/QCoreApplication.html
- [x] Qt model 进行数据绑定
- [ ] HOOK 添加自定义的 setter getter updater
- [x] 利用 Qt MetaMethod 自动 Hook 
- [x] Binder 绑定函数
- [x] Create todo app example
- [ ] ~~GBinder 括号 传入字符串参数作为分组~~
- [ ] ~~全局数据分组管理 - vue submodule~~
- [x] 使用 application eventFilter Hook 事件队列 
- [x] 数组 | 字典 update 更新视图，性能优化问题~


- [x] QBinding emit 将事件触发统一到 set 里面，最后通过 timer 实现 idle 触发
- [x] 实例化的时候记录所有的 binder 方便后续进行 dump 统一存储
- [x] 解决 DCC 环境导致的 binders 数组叠加问题
- [x] 尝试用 lambda 来实现函数绑定
- [x] 指定 binder 取消 autodump
- [x] 自动 bind QGroupBox RadioButton
- [x] self.state = Binder() 如何自动绑定实例化的函数
- [x] hook setStylesheet
- [x] meta hook 改良 (目前没有 hook 到所有的方法) ~~使用 json 定义 hook 的方法~~
- [x] 改良 hook 兼容 C++ static method (无法区隔 Qt 的 C++ static 函数 | 只能用 json 名单解决)
- [x] 查 autodump 的 BUG
- [x] GState 单例模式使用类似 index 计数修复方法解决共享冲突。 (todo_app 在 DCC 端的冲突)
- [x] FnHook 和 FnBinding 合并
- [x] PyQt Model 不支持 BUG (event 相关的函数去掉 hook)
- [x] pip 发布

- [x] 修复 six 版本问题 #issue4
- [x] 修复 DataStream 错误 #issue5
- [x] 修复 BinderTemplate Python 2 & 3 兼容问题

[Qt 文档索引](https://github.com/FXTD-ODYSSEY/MayaScript/blob/master/_QtDemo/_QtDoc/overviews.md)    
[PyQt mvc 教程](https://www.youtube.com/watch?v=2sRoLN337cs&list=PL8B63F2091D787896&index=2)    

