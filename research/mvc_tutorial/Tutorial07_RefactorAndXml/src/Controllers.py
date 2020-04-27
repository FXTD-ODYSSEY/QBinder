from PyQt4 import QtCore, QtGui, QtXml, uic
import sys
import Resources


from Data import Node, TransformNode, CameraNode, LightNode, LIGHT_SHAPES
from Models import SceneGraphModel
    
    
class XMLHighlighter(QtGui.QSyntaxHighlighter):
 
    #INIT THE STUFF
    def __init__(self, parent=None):
        super(XMLHighlighter, self).__init__(parent)
 
        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkMagenta)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)
 
        keywordPatterns = ["\\b?xml\\b", "/>", ">", "<"]
 
        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]
 
        xmlElementFormat = QtGui.QTextCharFormat()
        xmlElementFormat.setFontWeight(QtGui.QFont.Bold)
        xmlElementFormat.setForeground(QtCore.Qt.green)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=[\s/>])"), xmlElementFormat))
 
        xmlAttributeFormat = QtGui.QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QtCore.Qt.blue)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\=)"), xmlAttributeFormat))
 
        self.valueFormat = QtGui.QTextCharFormat()
        self.valueFormat.setForeground(QtCore.Qt.red)
 
        self.valueStartExpression = QtCore.QRegExp("\"")
        self.valueEndExpression = QtCore.QRegExp("\"(?=[\s></])")
 
        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.gray)
        self.highlightingRules.append((QtCore.QRegExp("<!--[^\n]*-->"), singleLineCommentFormat))
 
    #VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING
    def highlightBlock(self, text):
 
        #for every pattern
        for pattern, format in self.highlightingRules:
 
            #Create a regular expression from the retrieved pattern
            expression = QtCore.QRegExp(pattern)
 
            #Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)
 
            #While the index is greater than 0
            while index >= 0:
 
                #Get the length of how long the expression is true, set the format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, format)
 
                #Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)
 
        #HANDLE QUOTATION MARKS NOW.. WE WANT TO START WITH " AND END WITH ".. A THIRD " SHOULD NOT CAUSE THE WORDS INBETWEEN SECOND AND THIRD TO BE COLORED
        self.setCurrentBlockState(0)
 
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.valueStartExpression.indexIn(text)
 
        while startIndex >= 0:
            endIndex = self.valueEndExpression.indexIn(text, startIndex)
 
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.valueEndExpression.matchedLength()
 
            self.setFormat(startIndex, commentLength, self.valueFormat)
 
            startIndex = self.valueStartExpression.indexIn(text, startIndex + commentLength);    











base, form = uic.loadUiType("Views/Window.ui")

class WndTutorial06(base, form):
    

    def updateXml(self):
        
        print "UPDATING XML"
        
        xml = self._rootNode.asXml()
        
        self.uiXml.setPlainText(xml)


        
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._rootNode   = Node("Root")
        childNode0 = TransformNode("A",    self._rootNode)
        childNode1 = LightNode("B",        self._rootNode)
        childNode2 = CameraNode("C",       self._rootNode)
        childNode3 = TransformNode("D",    self._rootNode)
        childNode4 = LightNode("E",        self._rootNode)
        childNode5 = CameraNode("F",       self._rootNode)
        childNode6 = TransformNode("G",    childNode5)
        childNode7 = LightNode("H",        childNode6)
        childNode8 = CameraNode("I",       childNode7)
       

        
        self._proxyModel = QtGui.QSortFilterProxyModel(self)
        
        """VIEW <------> PROXY MODEL <------> DATA MODEL"""

        self._model = SceneGraphModel(self._rootNode, self)
        

        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        
        self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        self._proxyModel.setFilterRole(SceneGraphModel.filterRole)
        self._proxyModel.setFilterKeyColumn(0)
        
        self.uiTree.setModel(self._proxyModel)
        

        QtCore.QObject.connect(self.uiFilter, QtCore.SIGNAL("textChanged(QString)"), self._proxyModel.setFilterRegExp)

        self._propEditor = PropertiesEditor(self)
        self.layoutMain.addWidget(self._propEditor)
        
        self._propEditor.setModel(self._proxyModel)
        
        

        
        QtCore.QObject.connect(self.uiTree.selectionModel(), QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self._propEditor.setSelection)
        QtCore.QObject.connect(self._model, QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), self.updateXml)
        
        #Create our XMLHighlighter derived from QSyntaxHighlighter
        highlighter = XMLHighlighter(self.uiXml.document())

        self.updateXml()


propBase, propForm = uic.loadUiType("Views/Editors.ui")
nodeBase, nodeForm = uic.loadUiType("Views/NodeEditor.ui") 
lightBase, lightForm = uic.loadUiType("Views/LightEditor.ui")
cameraBase, cameraForm = uic.loadUiType("Views/CameraEditor.ui")
transformBase, transformForm = uic.loadUiType("Views/TransformEditor.ui")



"""PROPERTIESEDITOR"""
class PropertiesEditor(propBase, propForm):
    
    def __init__(self, parent = None):
        super(propBase, self).__init__(parent)
        self.setupUi(self)

        self._proxyModel = None

        self._nodeEditor = NodeEditor(self)
        self._lightEditor = LightEditor(self)
        self._cameraEditor = CameraEditor(self)
        self._transformEditor = TransformEditor(self)

        
        self.layoutNode.addWidget(self._nodeEditor)
        self.layoutSpecs.addWidget(self._lightEditor)
        self.layoutSpecs.addWidget(self._cameraEditor)
        self.layoutSpecs.addWidget(self._transformEditor)

        self._lightEditor.setVisible(False)
        self._cameraEditor.setVisible(False)
        self._transformEditor.setVisible(False)
               
    """INPUTS: QModelIndex, QModelIndex"""
    def setSelection(self, current, old):

        current = self._proxyModel.mapToSource(current)

        node = current.internalPointer()
        
        if node is not None:
            
            typeInfo = node.typeInfo()
            
        if typeInfo == "CAMERA":
            self._cameraEditor.setVisible(True)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)
        
        elif typeInfo == "LIGHT":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(True)
            self._transformEditor.setVisible(False)
             
        elif typeInfo == "TRANSFORM":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(True)
        else:
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)

        self._nodeEditor.setSelection(current)
        self._cameraEditor.setSelection(current)
        self._lightEditor.setSelection(current)
        self._transformEditor.setSelection(current)
        


        
    
    
    def setModel(self, proxyModel):
        
        self._proxyModel = proxyModel
        
        self._nodeEditor.setModel(proxyModel)
        self._lightEditor.setModel(proxyModel)
        self._cameraEditor.setModel(proxyModel)
        self._transformEditor.setModel(proxyModel)


"""NODE"""
class NodeEditor(nodeBase, nodeForm):
    
    def __init__(self, parent=None):
        super(nodeBase, self).__init__(parent)
        self.setupUi(self)
        
        self._dataMapper = QtGui.QDataWidgetMapper()
        
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiName, 0)
        self._dataMapper.addMapping(self.uiType, 1)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        


"""LIGHT"""
class LightEditor(lightBase, lightForm):
    
    def __init__(self, parent=None):
        super(lightBase, self).__init__(parent)
        self.setupUi(self)
        
        self._dataMapper = QtGui.QDataWidgetMapper()
   
        for i in LIGHT_SHAPES.names:
            if i != "End":
                self.uiShape.addItem(i)
   

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiLightIntensity, 2)
        self._dataMapper.addMapping(self.uiNear, 3)
        self._dataMapper.addMapping(self.uiFar, 4)
        self._dataMapper.addMapping(self.uiShadows, 5)
        self._dataMapper.addMapping(self.uiShape, 6, "currentIndex")
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        
        
"""CAMERA"""
class CameraEditor(cameraBase, cameraForm):
    
    def __init__(self, parent=None):
        super(cameraBase, self).__init__(parent)
        self.setupUi(self)
        
        self._dataMapper = QtGui.QDataWidgetMapper()
        
        
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiMotionBlur, 2)
        self._dataMapper.addMapping(self.uiShakeIntensity, 3)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        
"""TRANSFORM"""
class TransformEditor(transformBase, transformForm):
    
    def __init__(self, parent=None):
        super(transformBase, self).__init__(parent)
        self.setupUi(self)

        self._dataMapper = QtGui.QDataWidgetMapper()
        
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        
        self._dataMapper.addMapping(self.uiX, 2)
        self._dataMapper.addMapping(self.uiY, 3)
        self._dataMapper.addMapping(self.uiZ, 4)
        
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(current)
        
        
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    
    wnd = WndTutorial06()
    wnd.show()
    

 
 

    sys.exit(app.exec_())