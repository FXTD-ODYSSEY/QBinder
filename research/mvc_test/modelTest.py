# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-29 13:34:11'

"""

"""

import os
import sys
DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR,"..","..","QBinding","_vender")
if MODULE not in sys.path:
    sys.path.insert(0,MODULE)

import Qt
from Qt import QtGui,QtWidgets, QtCore
from functools import partial

class PaletteListModel(QtCore.QAbstractListModel):
    
    def __init__(self, colors = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors



    # def headerData(self, section, orientation, role):
        
    #     if role == QtCore.Qt.DisplayRole:
            
    #         if orientation == QtCore.Qt.Horizontal:
    #             return"Palette"
    #         else:
    #             return "Color %s" % section

    def rowCount(self, parent):
        return len(self.__colors)


    def data(self, index, role):
        
        
        if role == QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()
        
        
        if role == QtCore.Qt.ToolTipRole:
            return "Hex code: " + self.__colors[index.row()].name()
        

        if role == QtCore.Qt.DecorationRole:
            
            row = index.row()
            value = self.__colors[row]
            
            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)
            
            icon = QtGui.QIcon(pixmap)
            
            return icon

              
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__colors[row]
            
            return value.name()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            color = QtGui.QColor(value)
            
            if color.isValid():
                self.__colors[row] = color
                self.dataChanged.emit(index, index)
                return True
        return False


    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#
    def insertRows(self, position, rows,parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            self.__colors.insert(position, QtGui.QColor("#000000"))
        
        self.endInsertRows()
        
        return True


    
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)
             
        self.endRemoveRows()
        return True
    
class TestModel (QtCore.QAbstractListModel):

    def __init__(self, data = None, parent = None):
        super(TestModel,self).__init__( parent)
        self._data = data if data else []

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role):
        # NOTE https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
        val = self._data[index.row()] if len(self._data) > index.row() else next(iter(self._data), '')

        if role == QtCore.Qt.DisplayRole:
            return val

    def setData(self,data):
        self._data = data

    def getData(self):
        return self._data

class State(object):
    __repr__ = lambda self: self.val.__repr__()
    def __init__(self,val):
        self.val = val

class WidgetTest(QtWidgets.QWidget):
    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        #ALL OF OUR VIEWS
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()
        layout.addWidget(comboBox)
        comboBox.addItem("0")
        comboBox.addItem("1")
        comboBox.addItem("2")
        comboBox.addItem("3")
        comboBox.addItem("4")

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        red   = QtGui.QColor(255,0,0)
        green = QtGui.QColor(0,255,0)
        blue  = QtGui.QColor(0,0,255)

        rowCount = 4
        columnCount = 6

        self.model = PaletteListModel([red, green, blue])
        # red = State(123)
        # item_list = [red, "green", "blue"]
        # print(item_list)
        # self.model = TestModel(item_list)
        
        listView.setModel(self.model)
        comboBox.setModel(self.model)
        tableView.setModel(self.model)
        treeView.setModel(self.model)

        button = QtWidgets.QPushButton("change")
        button.clicked.connect(self.changeOrder)
        layout.addWidget(button)
        button = QtWidgets.QPushButton("change2")
        button.clicked.connect(partial(self.addComboBox,comboBox))
        layout.addWidget(button)

        self.model.dataChanged.connect(self.modifyData)

    def modifyData(self,topLeft,bottomRight,roles):
        pass
        # self.model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        # print ("modifyData",topLeft,bottomRight,roles)
        # print ("topLeft",topLeft.row())
        # print ("bottomRight",bottomRight.row())
        # model = topLeft.model()
        # print (model.stringList())
        
    def addComboBox(self,comboBox):
        print ("add")
        comboBox.addItem("asd")
        
    def changeOrder(self):
        # index = self.model.index(2,0)
        # self.model.setData(index,QtGui.QColor(100,233,255))
        # print(self.model.getColors())
        # colors = self.model.getColors()
        # colors.insert(0,QtGui.QColor(0,233,255))
        # self.model.setColors(colors)
        self.model.setData([])
        self.model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()


    widget.show()
    
    sys.exit(app.exec_())