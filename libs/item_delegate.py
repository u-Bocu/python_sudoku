from PyQt5 import QtWidgets, QtCore
import libs.solver as solver

class item_delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, owner):
        super().__init__(owner)
        self._items = [" ", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def paint(self, painter, option, index):
        if isinstance(self.parent(), QtWidgets.QAbstractItemView):
            self.parent().openPersistentEditor(index)
        super(item_delegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.data(QtCore.Qt.DisplayRole) != 0:
            return
        editor = QtWidgets.QComboBox(parent)
        editor.currentIndexChanged.connect(self.commit_editor)
        editor.addItems(self._items)
        editor.setEditable(False)
        return editor

    def commit_editor(self):
        editor = self.sender()
        self.commitData.emit(editor)

    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        if (str(value) in self._items):
            i = self._items.index(str(value))
        else:
            i = 0
        editor.setCurrentIndex(i)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

        if solver.is_grid_valid(model._data):
            win_message_box = QtWidgets.QMessageBox()
            win_message_box.setWindowTitle("Congratulations!")
            win_message_box.setText("You won!")
            win_message_box.exec()

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)