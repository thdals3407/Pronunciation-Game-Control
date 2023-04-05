from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import pyaudio
from ToolArray import Mic_device_detector

class startUI(QDialog):
    def __init__(self, audioList):
        super().__init__()

        # Load the UI
        loadUi('StartUI.ui', self)

        # Get the combo box object
        self.name_box = self.findChild(QLineEdit, "lineEdit")
        self.id_box = self.findChild(QLineEdit, "lineEdit2")
        self.word_box = self.findChild(QLineEdit, "lineEdit3")
        self.threshold_box = self.findChild(QDoubleSpinBox, "doubleSpinBox")
        self.audio_box = self.findChild(QComboBox, 'comboBox')
        self.startButton= self.findChild(QPushButton, 'pushButton')
        # Set the items of the combo box
        self.audio_box.addItems(audioList)

        # Save text values when window is closed
        self.startButton.clicked.connect(self.save_text_values)

    def save_text_values(self):
        self.name_text = self.name_box.text()
        self.id_text = self.id_box.text()
        self.word_text = self.word_box.text()
        self.threshold_value = self.threshold_box.value()
        self.audio_text = self.audio_box.currentText()
        print(f"Name: {self.name_text}, ID: {self.id_text}, Word: {self.word_text}, Threshold: {self.threshold_value}, Audio: {self.audio_text}")



if __name__ == '__main__':
    audio = pyaudio.PyAudio()
    d_list, index_list = Mic_device_detector(audio)
    app = QApplication([])
    dialog = startUI(d_list)
    dialog.show()
    app.exec_()