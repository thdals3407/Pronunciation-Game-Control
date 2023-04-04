from PyQt5.QtWidgets import QApplication, QDialog, QComboBox
from PyQt5.uic import loadUi
#from PyQt5 import QtWidgets
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Load the UI
        loadUi('StartUI.ui', self)

        # Get the combo box object
        combo_box = self.findChild(QComboBox, 'comboBox')

        # Set the items of the combo box
        items = ['item1', 'item2', 'item3']
        combo_box.addItems(items)

if __name__ == '__main__':
    app = QApplication([])
    dialog = MyDialog()
    dialog.show()
    app.exec_()