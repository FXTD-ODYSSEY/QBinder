# -*- coding: utf-8 -*-
"""
# TODO create a Vuex like pannel
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-07 22:24:50'

import os
import re
import sys
import time
from textwrap import dedent

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

from .util import CollapsibleWidget

DIR = os.path.dirname(__file__)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(393, 713)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Var_Toggle = QtWidgets.QPushButton(Form)
        self.Var_Toggle.setObjectName("Var_Toggle")
        self.verticalLayout.addWidget(self.Var_Toggle)
        self.Filter_Table = FilterTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Filter_Table.sizePolicy().hasHeightForWidth())
        self.Filter_Table.setSizePolicy(sizePolicy)
        self.Filter_Table.setMinimumSize(QtCore.QSize(0, 0))
        self.Filter_Table.setObjectName("Filter_Table")
        self.verticalLayout.addWidget(self.Filter_Table)
        self.Scope_Toggle = QtWidgets.QPushButton(Form)
        self.Scope_Toggle.setObjectName("Scope_Toggle")
        self.verticalLayout.addWidget(self.Scope_Toggle)
        self.Scope_List = QtWidgets.QListWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Scope_List.sizePolicy().hasHeightForWidth())
        self.Scope_List.setSizePolicy(sizePolicy)
        self.Scope_List.setMinimumSize(QtCore.QSize(0, 0))
        self.Scope_List.setObjectName("Scope_List")
        self.verticalLayout.addWidget(self.Scope_List)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self):
        # Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.Var_Toggle.setText(QtWidgets.QApplication.translate("Form", "Scope Variable", None, -1))
        self.Scope_Toggle.setText(QtWidgets.QApplication.translate("Form", "Function Scope", None, -1))
        
        
class LineEditDelegate(QtWidgets.QStyledItemDelegate):

    moveCurrentCellBy = QtCore.Signal(int, int)
    varaibleModified = QtCore.Signal(QtWidgets.QStyledItemDelegate,str)

    def __init__(self, parent=None):
        super(LineEditDelegate, self).__init__(parent)
        self.modified = True
        
    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QLineEdit(parent)
        self.editor.setFrame(False)
        self.editor.installEventFilter(self)
        self.editor.modelIndex = index
        return self.editor

    def setEditorData(self, editor, index):
        """setEditorData 
        Get cell data to lineEdit 
        
        :param editor: lineEdit widget
        :type editor: QLineEdit
        :param index: cell index
        :type index: QtCore.QModelIndex
        """
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def eventFilter(self, target, event):
        if target is self.editor:
            # NOTE 点击其他地方 取消修改
            if event.type() == QtCore.QEvent.Type.FocusAboutToChange:
                self.closeEditor.emit(self.editor, QtWidgets.QAbstractItemDelegate.NoHint)
                
            if event.type() == QtCore.QEvent.KeyPress:

                if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                    # NOTE 变量修改
                    self.varaibleModified.emit(self,self.editor.text())
                    if self.modified:
                        self.commitData.emit(self.editor)
                    else:
                        self.modified = True

                    self.closeEditor.emit(self.editor, QtWidgets.QAbstractItemDelegate.NoHint)

                if self.editor.hasFocus():
                    # NOTE 阻断上下箭头的 Layout
                    if event.key() in [QtCore.Qt.Key_Down,QtCore.Qt.Key_Up]:
                        return True
                    return False

                moveCell, row, column = False, 0, 0
                if event.key() == QtCore.Qt.Key_Down:
                    moveCell, row, column = True, 1, 0
                if event.key() == QtCore.Qt.Key_Up:
                    moveCell, row, column = True, -1, 0
                if event.key() in (QtCore.Qt.Key_Right, QtCore.Qt.Key_Tab):
                    moveCell, row, column = True, 0, 1
                if event.key() in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Backtab):
                    moveCell, row, column = True, 0, -1

                if moveCell:
                    self.commitData.emit(self.editor)
                    self.closeEditor.emit(self.editor, QtWidgets.QAbstractItemDelegate.NoHint)
                    self.moveCurrentCellBy.emit(row, column)
                    return True

        return False   

class FilterTableWidget(QtWidgets.QWidget):
    """
    # NOTE https://stackoverflow.com/questions/14068823/how-to-create-filters-for-qtableview-in-pyqt
    """
    def __init__(self, parent=None):
        super(FilterTableWidget, self).__init__(parent)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.view     = QtWidgets.QTableView(self)
        self.comboBox = QtWidgets.QComboBox(self)
        self.label    = QtWidgets.QLabel(self)

        # NOTE 延长Header
        self.view.horizontalHeader().setStretchLastSection(True)            

        self.view.setWordWrap(True)
        self.view.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.view.resizeRowsToContents()

        self.delegate = LineEditDelegate()
        self.view.setItemDelegate(self.delegate)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.view, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox.setMinimumWidth(150)
        self.model = QtGui.QStandardItemModel(self)

        self.proxy = QtCore.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        self.view.setModel(self.proxy)

        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)

        self.horizontalHeader = self.view.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)

        self.retranslateUi()
    
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        super(FilterTableWidget, self).changeEvent(event)

    def retranslateUi(self):
        self.label.setText(QtWidgets.QApplication.translate("label", "Regular Expression"))

        # NOTE 修改行名称
        header_list = [
            QtWidgets.QApplication.translate("header", "Variable Name"),
            QtWidgets.QApplication.translate("header", "Variable Value"),
        ]
        for column,label in enumerate(header_list):
            self.model.setHeaderData(column, QtCore.Qt.Horizontal,label)

        self.comboBox.clear()
        self.comboBox.addItems(header_list)
    
    def addItems(self,data):

        for var,val in data.items():
            var_item = QtGui.QStandardItem(str(var))
            var_item.setEditable(False)
            var_item.setToolTip(str(type(val)))


            val_item = QtGui.QStandardItem('"%s"' % val if type(val) == str else str(val))


            self.model.invisibleRootItem().appendRow([var_item,val_item])

        self.retranslateUi()

    def clearItems(self):
        for i in range(self.model.rowCount()):
            self.model.removeRows(i,self.model.rowCount())

    def setModel(self,model):
        self.model = model
        self.proxy.setSourceModel(self.model)

    @QtCore.Slot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        self.logicalIndex   = logicalIndex
        self.menuValues     = QtWidgets.QMenu(self)
        self.signalMapper   = QtCore.QSignalMapper(self)  

        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = [    self.model.item(row, self.logicalIndex).text()
                            for row in range(self.model.rowCount())
                            ]

        actionAll = QtWidgets.QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()

        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):              
            action = QtWidgets.QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)  
            action.triggered.connect(self.signalMapper.map)  
            self.menuValues.addAction(action)

        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)  

        self.headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())        

        posY = self.headerPos.y() + self.horizontalHeader.height()
        posX = self.headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    @QtCore.Slot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(  "",
                                        QtCore.Qt.CaseInsensitive,
                                        QtCore.QRegExp.RegExp
                                        )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    @QtCore.Slot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(  stringAction,
                                        QtCore.Qt.CaseSensitive,
                                        QtCore.QRegExp.FixedString
                                        )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    @QtCore.Slot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(    text,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )

        self.proxy.setFilterRegExp(search)

    @QtCore.Slot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)



class InfoPanel(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(InfoPanel,self).__init__()

        self.setupUi(self)
        # ui_path = os.path.join(DIR,"ui","debugVar.ui")
        # loadUi(ui_path,self)

        self.var_toggle_anim = CollapsibleWidget.install(self.Var_Toggle,self.Filter_Table)
        self.scope_toggle_anim = CollapsibleWidget.install(self.Scope_Toggle,self.Scope_List)
    
    def initialize(self):
        self.Scope_List.itemClicked.connect(self.itemClickEvent)
        self.Filter_Table.delegate.varaibleModified.connect(self.modifyScopeEvent)

    def modifyScopeEvent(self,delegate,val):
        delegate.modified = True
        model_index = delegate.editor.modelIndex
        row = model_index.row()
        v_model = self.Filter_Table.view.verticalHeader().model()
        row_label = v_model.headerData(row, QtCore.Qt.Vertical) 

        model = self.Filter_Table.model
        var_name = model.item(row_label-1, 0).text()
        item = self.Scope_List.currentItem()

        globals = item.globals
        locals = item.locals
        # try:
        #     code = "%s = %s\n" % (var_name,val)
        #     code = compile(code, '<stdin>', 'single')
        #     exec code in globals, locals

        #     val = item.locals[var_name]
        #     val = '"%s"' % val if type(val) == str else str(val)
        #     delegate.editor.setText(val)
        # except:
        #     t, v = sys.exc_info()[:2]
        #     if type(t) == type(''):
        #         exc_type_name = t
        #     else: exc_type_name = t.__name__
        #     print >>sys.stdout, '***', exc_type_name + ':', v
        #     delegate.modified = False

    def retranslateUi(self):
        drop_icon = self.Var_Toggle.text()[:1]
        self.Var_Toggle.setText(drop_icon + QtWidgets.QApplication.translate("info","Scope Variable"))
        drop_icon = self.Scope_Toggle.text()[:1]
        self.Scope_Toggle.setText(drop_icon + QtWidgets.QApplication.translate("info","Function Scope"))

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        super(InfoPanel, self).changeEvent(event)

    def itemClickEvent(self,item):
        self.Filter_Table.clearItems()
        self.Filter_Table.addItems(item.locals)
        
        # NOTE 定位代码文件
        path = item.text()
        lineno = re.search("\d+$",path[:-1]).group(0)
        filename = path[:-len(lineno)-2]
        
        # # NOTE 代码显示
        # if not os.path.exists(filename):
        #     code = "%s %s" % (filename , QtWidgets.QApplication.translate("reading", "file not exists"))
        # elif self.panel.link.path == filename:
        #     code = ''
        # else:
        #     try:
        #         with open(filename,'r') as f:
        #             code = f.read()
        #     except:
        #         code = "%s %s" % (filename , QtWidgets.QApplication.translate("reading", "read fail"))
        
        # self.panel.link.setText(filename,lineno)
        # self.panel.editor.setPlainText(code) if code else None
        # self.panel.editor.paintLine(int(lineno))
        
        # self.Filter_Table.lineEdit.clear()

    def addItems(self,data):
        self.Filter_Table.addItems(data)

    def clear(self):
        self.Filter_Table.clearItems()

class PanelEvent(QtCore.QObject):
    
    def __init__(self):
        super(PanelEvent,self).__init__()
        event = QtCore.QEvent(QtCore.QEvent.User)
        QtWidgets.QApplication.postEvent(self, event)
        self.installEventFilter(self)

    def eventFilter(self,receiver,event):
        global __QBinder_info_panel__
        __QBinder_info_panel__ = InfoPanel()
        __QBinder_info_panel__.show()
        return False

def show_info_panel():
    # NOTE show pannel with event loop 
    global __QBinder_info_panel__
    __QBinder_info_panel__ = PanelEvent()

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)

    widget = InfoPanel()
    widget.show()

    sys.exit(app.exec_())
    