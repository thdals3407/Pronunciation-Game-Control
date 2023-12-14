from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
#import matplotlib.pyplot as mlt
#from pyqtgraph import PlotWidget, plot
#import pyqtgraph as pg
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer, pyqtSignal, QObject

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

class startUI_all(QDialog):
    def __init__(self, ui_path, audioList, threshold):
        super().__init__()

        # Load the UI
        loadUi(ui_path, self)

        # Get the combo box object
        self.name_box = self.findChild(QLineEdit, "lineEdit")
        self.id_box = self.findChild(QLineEdit, "lineEdit_2")
        self.word_box = self.findChild(QLineEdit, "lineEdit_3")
        self.inputKey = self.findChild(QLineEdit, "lineEdit_4")
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
        self.inputKey_text = self.inputKey.text()
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

    def get_inputKey(self):
        return self.inputKey_text

class mainUI(QDialog):
    value_changed = pyqtSignal(int)
    def __init__(self, uipath, queue):
        super().__init__()

        self.queue = queue
        # Load the UI
        loadUi(uipath, self)
        # Get the combo box object
        self.feedbackText = self.findChild(QTextEdit, "textEdit")
        self.windowButton = self.findChild(QPushButton, 'pushButton')
        self.settingButton = self.findChild(QPushButton, 'pushButton_2')
        self.windowButton.clicked.connect(self.pressButton)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)
        self.timer.start(100)  # Update every 1000 milliseconds (1 second)
    def pressButton(self):
        self.close()
    def update_label(self):
        while not self.queue.empty():
            value = self.queue.get_nowait()
            print("UI get data ", value)
            self.feedbackText.setText(value)

class scoreUI(QDialog):
    def __init__(self, uipath):
        super().__init__()

        # Load the UI
        loadUi(uipath, self)

        # Report the UI
        self.feedbackText = self.findChild(QTextEdit, "textEdit")
        self.username = ""
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
    def update_value(self):
        self.value += 1
        self.value_changed.emit(self.value)

    def get_feedback_Scoring(self, scoring):
        if len(scoring) > 0:
            self.fig.clf()
            self.feedbackText.setText(self.score_to_string(scoring, self.username))
            # for draw graph
            self.graph_verticalLayout.addWidget(self.canvas)
            y1, y2 = self.get_paramter_setting(scoring)
            x = np.arange(1, len(y1) + 1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y1)
            ax.plot(x, y2)
            # ax.xticks(x)
            # ax.set_xlabel("회차")
            # ax.set_xlabel("점수")

            # ax.set_title(username + " 점수 분석표")
            ax.legend()
            self.canvas.draw()
    def get_userName(self, name):
        self.username = name
    def score_to_string(self, scoring, username):
        reporter = "이름 :" + username + "\n\n"
        threshold_array = scoring[0]
        gop_array = scoring[1]
        print(scoring)
        if len(gop_array) > 0:
            for i in range(len(gop_array)):
                reporter += "각 발음별 점수      : \n"
                for j in range(len(gop_array[i])):
                    reporter += f"        {j + 1} 회:" + str(int(gop_array[i][j] * 100)) + "점\n"
                print("error check: ",i, len(gop_array)-1)
                if i < len(threshold_array)-1 and len(gop_array[i]) > 0:
                    reporter += "\n평균: {} , 정확도: {} % \n".format(int(sum(gop_array[i]) / len(gop_array[i]) * 100),
                                                                    self.get_acc(gop_array[i], threshold_array[i]))
                    reporter += "난이도 변경 :  {}  >>  {} \n".format(int(threshold_array[i]*100), int(threshold_array[i+1]*100))
                    reporter += "--------------------\n"
        return reporter
    def get_acc(self, gop_array, threshold):
        overcheck = 0
        for i in gop_array:
            if i >= threshold:
                overcheck += 1

        return int(overcheck / len(gop_array) * 100)

    def get_paramter_setting(self, scoring):
        y1 = []
        y2 = []
        threshold_array = scoring[0]
        gop_array = scoring[1]
        for i in range(len(gop_array)):
            for j in range(len(gop_array[i])):
                y1.append(gop_array[i][j])
                y2.append(threshold_array[i])
        return np.array(y1) * 100, np.array(y2) * 100

if __name__ == '__main__':
    #import pyaudio
    #from ToolArray import Mic_device_detector
    #audio = pyaudio.PyAudio()
    #d_list, index_list = Mic_device_detector(audio)
    app = QApplication([])
    #StartUI = scoreUI("ScoreUI.ui", "test")
    #StartUI.show()
    #app.exec_()

    MainUI = mainUI("MainUI.ui", "ScoreUI.ui", "test")
    MainUI.show()
    app.exec_()
    #print(StartUI.get_audioDevice())