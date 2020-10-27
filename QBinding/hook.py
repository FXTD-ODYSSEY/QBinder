# coding:utf-8

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-04-17 15:35:39'

"""
自动绑定配置表
"""
import six
import inspect
from functools import partial

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

HOOKS = {
    QtWidgets.QComboBox: {
        "setCurrentIndex": {
            "type":int,   
        },
        "setItemText": {
            "type":str,
        },
    },
    QtWidgets.QLineEdit: {
        "setText":{
            "type":str,
        },
    },
    
    QtWidgets.QLabel: {
        "setText":{
            "type":str,
        },
    },

    QtWidgets.QCheckBox: {
        "setChecked":{
            "type":bool,
        },
        "setText":{
            "type":str,
        },
    },


    # QtWidgets.QAction: {
    #     bool:{
    #         "getter": "isChecked",
    #         "setter": "setChecked",
    #         "signals": "toggled",
    #     }
    # },
    # # QtWidgets.QActionGroup: (_get_QActionGroup, _set_QActionGroup, _event_QActionGroup),
    # QtWidgets.QPushButton: {
    #     bool:{
    #         "getter": "isChecked",
    #         "setter": "setChecked",
    #         "signals": "toggled",
    #     }
    # },
    # QtWidgets.QSpinBox: {
    #     int:{
    #         "getter": "value",
    #         "setter": "setValue",
    #         "signals": "valueChanged",
    #     }
    # },
    # QtWidgets.QDoubleSpinBox: {
    #     float:{
    #         "getter": "value",
    #         "setter": "setValue",
    #         "signals": "valueChanged",
    #     }
    # },
    # # QtWidgets.QPlainTextEdit: {
    # #     str:{
    # #         "getter": "value",
    # #         "setter": "setPlainText",
    # #         "signals": "valueChanged",
    # #     }
    # # },
    # # QtWidgets.QListWidget: (_get_QListWidget, _set_QListWidget, _event_QListWidget),
    # # QtWidgets.QSlider: (_get_QSlider, _set_QSlider, _event_QSlider),
    # # QtWidgets.QButtonGroup: (_get_QButtonGroup, _set_QButtonGroup, _event_QButtonGroup),
    # # QtWidgets.QTabWidget: (_get_QTabWidget, _set_QTabWidget, _event_QTabWidget)
}


def StateHandler(func,options=None):
    """
    # NOTE initialize the Qt Widget setter 
    """
    options = options if options is not None else {}
    typ = options.get("type")
    signals = options.get("signals",[])
    signals = [signals] if isinstance(signals,six.string_types) else signals
    def wrapper(self,value,*args, **kwargs):
        if callable(value):
            # NOTE  get the outter frame state attribute from the
            frame = inspect.currentframe().f_back
            parent = frame.f_locals.get('self')
            STATE = parent.state if hasattr(parent,"state") else None
            if STATE:
                self.STATE_DICT = {} if not hasattr(self,"STATE_DICT") else self.STATE_DICT
                self.STATE_DICT.setdefault(STATE,{})
                callback = self.STATE_DICT.get(STATE).get(func)
                # NOTE clear old callback
                STATE._model.itemChanged.disconnect(callback) if callback else None
                
                callback = partial(lambda value,state:(func(self,typ(value()) if typ else value(),*args, **kwargs)),value)
                self.STATE_DICT[STATE][func] = callback
                STATE._model.itemChanged.connect(callback)

            value = value()
            value = typ(value) if typ else value

        res = func(self,value,*args,**kwargs)
        return res
    return wrapper

# global hook_dict
hook_dict = {}
def hookInitialize():
    """
    # NOTE Dynamic wrap the Qt Widget setter base on the HOOKS Definition
    """
    # global hook_dict
    for widget,(setter,func) in hook_dict.items():
        setattr(widget,setter,func)

    for widget,setters in HOOKS.items():
        for setter,options in setters.items():
            hook_dict[widget] = (setter,getattr(widget,setter))
            setattr(widget,setter,StateHandler(getattr(widget,setter),options))
            # NOTE example code -> setattr(QtWidgets.QCheckBox,"setText",StateHandler(QtWidgets.QCheckBox.setText))

# HOOKS = {
#     QComboBox: (_get_QComboBox, _set_QComboBox, _event_QComboBox),
#     QCheckBox: (_get_QCheckBox, _set_QCheckBox, _event_QCheckBox),
#     QAction: (_get_QAction, _set_QAction, _event_QAction),
#     QActionGroup: (_get_QActionGroup, _set_QActionGroup, _event_QActionGroup),
#     QPushButton: (_get_QPushButton, _set_QPushButton, _event_QPushButton),
#     QSpinBox: (_get_QSpinBox, _set_QSpinBox, _event_QSpinBox),
#     QDoubleSpinBox: (_get_QDoubleSpinBox, _set_QDoubleSpinBox, _event_QDoubleSpinBox),
#     QPlainTextEdit: (_get_QPlainTextEdit, _set_QPlainTextEdit, _event_QPlainTextEdit),
#     QLineEdit: (_get_QLineEdit, _set_QLineEdit, _event_QLineEdit),
#     QListWidget: (_get_QListWidget, _set_QListWidget, _event_QListWidget),
#     QSlider: (_get_QSlider, _set_QSlider, _event_QSlider),
#     QButtonGroup: (_get_QButtonGroup, _set_QButtonGroup, _event_QButtonGroup),
#     QTabWidget: (_get_QTabWidget, _set_QTabWidget, _event_QTabWidget)
# }

# # QComboBox
# def _get_QComboBox(self):
#     """
#         Get value QCombobox via re-mapping filter
#     """
#     return self._get_map(self.currentText())


# def _set_QComboBox(self, v):
#     """
#         Set value QCombobox via re-mapping filter
#     """
#     self.setCurrentIndex(self.findText(unicode(self._set_map(v))))


# def _event_QComboBox(self):
#     """
#         Return QCombobox change event signal
#     """
#     return self.currentIndexChanged


# # QCheckBox
# def _get_QCheckBox(self):
#     """
#         Get state of QCheckbox
#     """
#     return self.isChecked()


# def _set_QCheckBox(self, v):
#     """
#         Set state of QCheckbox
#     """
#     self.setChecked(v)


# def _event_QCheckBox(self):
#     """
#         Return state change signal for QCheckbox
#     """
#     return self.stateChanged


# # QAction
# def _get_QAction(self):
#     """
#         Get checked state of QAction
#     """
#     return self.isChecked()


# def _set_QAction(self, v):
#     """
#         Set checked state of QAction
#     """
#     self.setChecked(v)


# def _event_QAction(self):
#     """
#         Return state change signal for QAction
#     """
#     return self.toggled


# # QActionGroup
# def _get_QActionGroup(self):
#     """
#         Get checked state of QAction
#     """
#     if self.checkedAction():
#         return self.actions().index(self.checkedAction())
#     else:
#         return None


# def _set_QActionGroup(self, v):
#     """
#         Set checked state of QAction
#     """
#     self.actions()[v].setChecked(True)


# def _event_QActionGroup(self):
#     """
#         Return state change signal for QAction
#     """
#     return self.triggered


# # QPushButton
# def _get_QPushButton(self):
#     """
#         Get checked state of QPushButton
#     """
#     return self.isChecked()


# def _set_QPushButton(self, v):
#     """
#         Set checked state of QPushButton
#     """
#     self.setChecked(v)


# def _event_QPushButton(self):
#     """
#         Return state change signal for QPushButton
#     """
#     return self.toggled


# # QSpinBox
# def _get_QSpinBox(self):
#     """
#         Get current value for QSpinBox
#     """
#     return self.value()


# def _set_QSpinBox(self, v):
#     """
#         Set current value for QSpinBox
#     """
#     self.setValue(v)


# def _event_QSpinBox(self):
#     """
#         Return value change signal for QSpinBox
#     """
#     return self.valueChanged


# # QDoubleSpinBox
# def _get_QDoubleSpinBox(self):
#     """
#         Get current value for QDoubleSpinBox
#     """
#     return self.value()


# def _set_QDoubleSpinBox(self, v):
#     """
#         Set current value for QDoubleSpinBox
#     """
#     self.setValue(v)


# def _event_QDoubleSpinBox(self):
#     """
#         Return value change signal for QDoubleSpinBox
#     """
#     return self.valueChanged


# # QPlainTextEdit
# def _get_QPlainTextEdit(self):
#     """
#         Get current document text for QPlainTextEdit
#     """
#     return self.document().toPlainText()


# def _set_QPlainTextEdit(self, v):
#     """
#         Set current document text for QPlainTextEdit
#     """
#     self.setPlainText(unicode(v))


# def _event_QPlainTextEdit(self):
#     """
#         Return current value changed signal for QPlainTextEdit box.

#         Note that this is not a native Qt signal but a signal manually fired on 
#         the user's pressing the "Apply changes" to the code button. Attaching to the 
#         modified signal would trigger recalculation on every key-press.
#     """
#     return self.sourceChangesApplied


# # QLineEdit
# def _get_QLineEdit(self):
#     """
#         Get current text for QLineEdit
#     """
#     return self._get_map(self.text())


# def _set_QLineEdit(self, v):
#     """
#         Set current text for QLineEdit
#     """
#     self.setText(unicode(self._set_map(v)))


# def _event_QLineEdit(self):
#     """
#         Return current value changed signal for QLineEdit box.
#     """
#     return self.textChanged


# # CodeEditor
# def _get_CodeEditor(self):
#     """
#         Get current document text for CodeEditor. Wraps _get_QPlainTextEdit.
#     """
#     _get_QPlainTextEdit(self)


# def _set_CodeEditor(self, v):
#     """
#         Set current document text for CodeEditor. Wraps _set_QPlainTextEdit.
#     """
#     _set_QPlainTextEdit(self, unicode(v))


# def _event_CodeEditor(self):
#     """
#         Return current value changed signal for CodeEditor box. Wraps _event_QPlainTextEdit.
#     """
#     return _event_QPlainTextEdit(self)


# # QListWidget
# def _get_QListWidget(self):
#     """
#         Get currently selected values in QListWidget via re-mapping filter.

#         Selected values are returned as a list.
#     """
#     return [self._get_map(s.text()) for s in self.selectedItems()]


# def _set_QListWidget(self, v):
#     """
#         Set currently selected values in QListWidget via re-mapping filter.

#         Supply values to be selected as a list.
#     """
#     if v:
#         for s in v:
#             self.findItems(unicode(self._set_map(s)), Qt.MatchExactly)[
#                 0].setSelected(True)


# def _event_QListWidget(self):
#     """
#         Return current selection changed signal for QListWidget.
#     """
#     return self.itemSelectionChanged


# # QListWidgetWithAddRemoveEvent
# def _get_QListWidgetAddRemove(self):
#     """
#         Get current values in QListWidget via re-mapping filter.

#         Selected values are returned as a list.
#     """
#     return [self._get_map(self.item(n).text()) for n in range(0, self.count())]


# def _set_QListWidgetAddRemove(self, v):
#     """
#         Set currently values in QListWidget via re-mapping filter.

#         Supply values to be selected as a list.
#     """
#     block = self.blockSignals(True)
#     self.clear()
#     self.addItems([unicode(self._set_map(s)) for s in v])
#     self.blockSignals(block)
#     self.itemAddedOrRemoved.emit()


# def _event_QListWidgetAddRemove(self):
#     """
#         Return current selection changed signal for QListWidget.
#     """
#     return self.itemAddedOrRemoved


# # QColorButton
# def _get_QColorButton(self):
#     """
#         Get current value for QColorButton
#     """
#     return self.color()


# def _set_QColorButton(self, v):
#     """
#         Set current value for QColorButton
#     """
#     self.setColor(v)


# def _event_QColorButton(self):
#     """
#         Return value change signal for QColorButton
#     """
#     return self.colorChanged


# # QNoneDoubleSpinBox
# def _get_QNoneDoubleSpinBox(self):
#     """
#         Get current value for QDoubleSpinBox
#     """
#     return self.value()


# def _set_QNoneDoubleSpinBox(self, v):
#     """
#         Set current value for QDoubleSpinBox
#     """
#     self.setValue(v)


# def _event_QNoneDoubleSpinBox(self):
#     """
#         Return value change signal for QDoubleSpinBox
#     """
#     return self.valueChanged


# # QCheckTreeWidget
# def _get_QCheckTreeWidget(self):
#     """
#         Get currently checked values in QCheckTreeWidget via re-mapping filter.

#         Selected values are returned as a list.
#     """
#     return [self._get_map(s) for s in self._checked_item_cache]


# def _set_QCheckTreeWidget(self, v):
#     """
#         Set currently checked values in QCheckTreeWidget via re-mapping filter.

#         Supply values to be selected as a list.
#     """
#     if v:
#         for s in v:
#             f = self.findItems(unicode(self._set_map(s)),
#                                Qt.MatchExactly | Qt.MatchRecursive)
#             if f:
#                 f[0].setCheckState(0, Qt.Checked)


# def _event_QCheckTreeWidget(self):
#     """
#         Return current checked changed signal for QCheckTreeWidget.
#     """
#     return self.itemCheckedChanged


# # QSlider
# def _get_QSlider(self):
#     """
#         Get current value for QSlider
#     """
#     return self.value()


# def _set_QSlider(self, v):
#     """
#         Set current value for QSlider
#     """
#     self.setValue(v)


# def _event_QSlider(self):
#     """
#         Return value change signal for QSlider
#     """
#     return self.valueChanged


# # QButtonGroup
# def _get_QButtonGroup(self):
#     """
#         Get a list of (index, checked) tuples for the buttons in the group
#     """
#     return [(nr, btn.isChecked()) for nr, btn in enumerate(self.buttons())]


# def _set_QButtonGroup(self, v):
#     """
#         Set the states for all buttons in a group from a list of (index, checked) tuples
#     """
#     for idx, state in v:
#         self.buttons()[idx].setChecked(state)


# def _event_QButtonGroup(self):
#     """
#         Return button clicked signal for QButtonGroup
#     """
#     return self.buttonClicked


# # QTabWidget
# def _get_QTabWidget(self):
#     """
#         Get the current tabulator index
#     """
#     return self.currentIndex()


# def _set_QTabWidget(self, v):
#     """
#         Set the current tabulator index
#     """
#     self.setCurrentIndex(v)


# def _event_QTabWidget(self):
#     """
#         Return currentChanged signal for QTabWidget
#     """
#     return self.currentChanged
