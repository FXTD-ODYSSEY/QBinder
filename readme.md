## 方案重写 TDOO

- [x] 单例模式 - 数据全局共享
- [ ] 数据 dump 输入输出
- [ ] 自动加载上次的配置 利用 QTimer 0 timeout 实现 idle 执行 https://doc.qt.io/qtforpython/PySide2/QtCore/QCoreApplication.html
- [x] Qt model 进行数据绑定
- [ ] HOOK 添加自定义的 setter getter updater
- [ ] ~~自动 Hook 尝试~~
- [x] Binder 绑定函数
- [x] Create todo app example
- [ ] 模仿 vuex 添加 Binder action commit
- [ ] 制作类似 vue-devtools 的调试面板 (mpdb 面板)
- [ ] GBinder 括号 传入字符串参数作为分组
- [ ] 全局数据分组管理 - vue submodule
- [ ] 使用 Qt State Machine 管理状态变化
- [x] 使用 application eventFilter Hook 事件队列 
- [ ] 数组 | 字典 update 更新视图，性能优化问题~

> 细化 Todo

- [ ] QBinding emit 将事件触发统一到 set 里面，最后通过 timer 实现 idle 触发
- [ ] combobox update delay
- [ ] 实例化的时候记录所有的 binder 方便后续进行 dump 统一存储
- [ ] Model 实现可扩展
- [ ] 实现 QCombobox addItem 扩展支持
- [ ] 自动 bind QGroupBox CheckBox 和 RadioButton
- [x] hook setStylesheet


[Qt 文档索引](https://github.com/FXTD-ODYSSEY/MayaScript/blob/master/_QtDemo/_QtDoc/overviews.md)
[PyQt mvc 教程](https://www.youtube.com/watch?v=2sRoLN337cs&list=PL8B63F2091D787896&index=2)

