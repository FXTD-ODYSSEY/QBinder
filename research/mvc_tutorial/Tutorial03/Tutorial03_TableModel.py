from PySide import QtGui, QtCore
import sys






class PaletteTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, colors = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__colors = colors
        self.__headers = headers



    def rowCount(self, parent):
        return len(self.__colors)
    
    
    def columnCount(self, parent):
        return len(self.__colors[0])


    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    def data(self, index, role):
        
        
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__colors[row][column].name()
        
        
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return "Hex code: " + self.__colors[row][column].name()
        

        if role == QtCore.Qt.DecorationRole:
            
            row = index.row()
            column = index.column()
            value = self.__colors[row][column]
            
            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)
            
            icon = QtGui.QIcon(pixmap)
            
            return icon

              
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            column = index.column()
            value = self.__colors[row][column]
            
            return value.name()


    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            column = index.column()
            
            color = QtGui.QColor(value)
            
            if color.isValid():
                self.__colors[row][column] = color
                self.dataChanged.emit(index, index)
                return True
        return False




    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
            else:
                return "Color %s" % section



    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            
            defaultValues = [QtGui.QColor("#000000") for i in range(self.columnCount(None))]
            self.__colors.insert(position, defaultValues)
        
        self.endInsertRows()
        
        return True


    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        
        rowCount = len(self.__colors)
        
        for i in range(columns):
            for j in range(rowCount):
                self.__colors[j].insert(position, QtGui.QColor("#000000"))
        
        self.endInsertColumns()
        
        return True







if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")


    #ALL OF OUR VIEWS
    listView = QtGui.QListView()
    listView.show()

    comboBox = QtGui.QComboBox()
    comboBox.show()

    tableView = QtGui.QTableView()
    tableView.show()
    
 
    
    red   = QtGui.QColor(255,0,0)
    green = QtGui.QColor(0,255,0)
    blue  = QtGui.QColor(0,0,255)
    


    rowCount = 4
    columnCount = 6

    headers = ["Pallete0", "Colors", "Brushes", "Omg", "Technical", "Artist"]
    tableData0 = [ [ QtGui.QColor("#FFFF00") for i in range(columnCount)] for j in range(rowCount)]
   
    model = PaletteTableModel(tableData0, headers)
    model.insertColumns(0, 5)
    
    listView.setModel(model)
    comboBox.setModel(model)
    tableView.setModel(model)

    
    sys.exit(app.exec_())