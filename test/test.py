from QBinder import Binder, Model
from Qt import QtWidgets

state = Binder()

state.text = "text"
state.num_1 = "1"
state.num_2 = "2"
state.num_3 = "3"
state.num_4 = "4"

# NOTE 构建 QStandardItemModel
state.model = Model(
    [
        state["num_1"],
        state["num_2"],
        state["num_3"],
        state["num_4"],
    ]
)


app = QtWidgets.QApplication([])

combo = QtWidgets.QComboBox()
combo.setModel(state.model)

state.num_1 = "change_1"
state.num_2 = "change_2"

combo.show()

app.exec_()