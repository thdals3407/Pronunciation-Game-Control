from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class startUI(QDialog):
    def __init__(self, ui_path, audioList, threshold):
        super().__init__()

        # Load the UI
        loadUi(ui_path, self)

        # Get the combo box object
        self.name_box = self.findChild(QLineEdit, "lineEdit")
        self.id_box = self.findChild(QLineEdit, "lineEdit_2")
        self.word_box = self.findChild(QLineEdit, "lineEdit_3")
        self.threshold_box = self.findChild(QDoubleSpinBox, "doubleSpinBox")
        self.audio_box = self.findChild(QComboBox, 'comboBox')
        self.startButton= self.findChild(QPushButton, 'pushButton')
        # Set the items of the combo box
        self.audio_box.addItems(audioList)
        self.threshold_box.setValue(threshold)
        # Save text values when window is closed
        self.startButton.clicked.connect(self.save_text_values)

    def save_text_values(self):
        self.name_text = self.name_box.text()
        self.id_text = self.id_box.text()
        self.word_text = self.word_box.text()
        self.threshold_value = self.threshold_box.value()
        self.audio_text = self.audio_box.currentText()
        print(f"Name: {self.name_text}, ID: {self.id_text}, Word: {self.word_text}, Threshold: {self.threshold_value}, Audio: {self.audio_text}")
        self.close()

    def get_userName(self):
        return self.name_text

    def get_userId(self):
        return self.id_text

    def get_targetWord(self):
        return self.word_text

    def get_threshold(self):
        return self.threshold_value

    def get_audioDevice(self):
        return self.audio_text

if __name__ == '__main__':
    import pyaudio
    from ToolArray import Mic_device_detector
    audio = pyaudio.PyAudio()
    d_list, index_list = Mic_device_detector(audio)
    app = QApplication([])
    StartUI = startUI(d_list, 0.12)
    StartUI.show()
    app.exec_()

    print(StartUI.get_audioDevice())