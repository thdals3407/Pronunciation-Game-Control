from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
#import matplotlib.pyplot as mlt
#from pyqtgraph import PlotWidget, plot
#import pyqtgraph as pg
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import copy
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
    def __init__(self, ui_path, audioList, threshold = 20):
        super().__init__()

        # Load the UI
        loadUi(ui_path, self)

        # Get the combo box object
        self.name_box = self.findChild(QLineEdit, "nameText")
        #self.id_box = self.findChild(QLineEdit, "lineEdit_2")
        self.word_box = self.findChild(QLineEdit, "wordText")
        self.inputKey = self.findChild(QComboBox, "keyBox")
        self.threshold_box = self.findChild(QDoubleSpinBox, "thresholdBox")
        self.audio_box = self.findChild(QComboBox, 'comboBox')
        self.startButton= self.findChild(QPushButton, 'pushButton')
        
        # Set the items of the combo box
        self.audio_box.addItems(audioList)
        self.inputKey.addItems(["click", "space", "enter", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
        self.threshold_box.setValue(threshold)
        # Save text values when window is closed
        self.startButton.clicked.connect(self.save_text_values)

    def save_text_values(self):
        self.name_text = self.name_box.text()
        #self.id_text = self.id_box.text()
        self.word_text = self.word_box.text()
        self.inputKey_text = self.inputKey.currentText()
        self.threshold_value = self.threshold_box.value()
        self.audio_text = self.audio_box.currentText()
        #print(f"Name: {self.name_text}, Word: {self.word_text}, Audio: {self.audio_text}")
        self.close()

    def get_userName(self):
        return self.name_text

    #def get_userId(self):
    #    return self.id_text

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
        self.timer.start(100)  # Update every 100 milliseconds (0.1 second)
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
        # print("test scoring:" , scoring)   
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
            plt.ylim(0, 100)
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


class AllMainUI(QDialog):
    value_changed = pyqtSignal(int)

    def __init__(self, uipath, queue, fixedThreshold):
        super().__init__()

        self.queue = queue
        # Load the UI
        loadUi(uipath, self)

        # Find child widgets
        self.GoPScore = self.findChild(QTextBrowser, "GopText")
        self.InputText = self.findChild(QTextBrowser, 'InputText')
        self.KeySetting = self.findChild(QTextBrowser, 'KeyText')
        self.LogText = self.findChild(QTextBrowser, 'LogText')
        self.TargetText = self.findChild(QTextBrowser, 'TargetText')
        self.UserName = self.findChild(QTextBrowser, 'NameText')
        self.Graph = self.findChild(QVBoxLayout, "graph_verticalLayout")
        self.exitButton = self.findChild(QToolButton, 'exitButton')
        self.settingButton = self.findChild(QToolButton, 'settingButton')
        
        self.exitButton.clicked.connect(self.pressExitButton)
        self.settingButton.clicked.connect(self.pressSettingButton)
        self.fixedThreshold = fixedThreshold
        self.logString = ""
        self.threshold = []
        self.gop_list  = []
        self.targetThreshold = []

        # Initialize the matplotlib figure and canvas
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        # Initialize the timer for updating UI elements
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)
        self.timer.start(100)  # Update every 100 milliseconds

        # Add the initial canvas to the layout
        self.Graph.addWidget(self.canvas)

        self.nextUiIndex = -1 # Main창 이후에 어떤 UI를 사용할지 선택하는 값(-1은 종료, 1은 setting ~~)

    def get_feedback_Scoring(self, top_score, threshold):
        try:
            #  print("Score Test", scoring)
            #  shallow_copied_list = copy.deepcopy(scoring)
            self.threshold.append(threshold*100)
            self.gop_list.append(top_score*100)
            self.targetThreshold.append(copy.copy(self.fixedThreshold))
            self.passThreshold(top_score > self.fixedThreshold/100)
            if len(self.gop_list) > 0:
                self.fig.clf()  # Clear the existing figure

                y1, y2, y3 = np.array(self.gop_list), np.array(self.threshold), np.array(self.targetThreshold)
                x = np.arange(1, len(y1) + 1)

                ax = self.fig.add_subplot(111)
                ax.plot(x, y1)
                ax.plot(x, y2)
                ax.plot(x, y3)

                ax.set_ylim(0, 100)  # Y축의 범위를 0에서 100으로 설정

                self.canvas.draw()  # Draw the new graph

                if self.Graph.count() > 0:
                    self.Graph.takeAt(0)  # 기존에 있던 위젯을 제거합니다.

                self.Graph.addWidget(self.canvas)  # 새로운 캔버스를 추가합니다."""
        except:
            print("error")
            pass 

    def splitText(self, input, splitText = "--"):
        parts = input.split(splitText)
        return parts

    def update_label(self):
        while not self.queue.empty():
            value = self.queue.get_nowait() #[입력 단어, 입력 단어 형태소(+ 점수), top_score, threshold, pass]
            #print("valueTest", value)
            self.InputText.setText(value[0] + "({})".format(value[1])) 
            self.InputText.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #self.InputText.setFont(QtGui.QFont("굴림",15)) #폰트,크기 조절
            #self.InputText.setStyleSheet("Color : green") #글자색 변환

            self.GoPScore.setText(str(int(value[2]*100)) + "점")
            self.GoPScore.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #self.GoPScore.setFont(QtGui.QFont("굴림",15)) #폰트,크기 조절
            #self.GoPScore.setStyleSheet("Color : green") #글자색 변환

            self.setUpdateLog(value[0] + "({}): ".format(value[1]) + str(int(value[2]*100)) )
            self.get_feedback_Scoring(value[2], value[3])

            self.passKeyUIupdate(value[4])

    def pressExitButton(self):
        self.nextUiIndex = -1
        self.close()

    def pressSettingButton(self):
        self.nextUiIndex = 1
        self.close()

    def getNextUIIndex(self):
        return self.nextUiIndex

    def setNextUIIndex(self, nextUiIndex):
        self.nextUiIndex = nextUiIndex

    def setFixedThreshold(self, fixedThreshold):
        self.fixedThreshold = fixedThreshold

    def setUserName(self, userName):
        self.UserName.setText(userName)
        self.UserName.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #self.UserName.setFont(QtGui.QFont("굴림",15)) #폰트,크기 조절

    def setTargetText(self, targetText):
        self.TargetText.setText(targetText)
        self.TargetText.setStyleSheet("Color : blue") #글자색 변환
        #self.TargetText.setFont(QtGui.QFont("굴림",12)) #폰트,크기 조절

    def setkeySetting(self, keySetting):
        self.KeySetting.setText(keySetting)
        self.KeySetting.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #self.KeySetting.setFont(QtGui.QFont("굴림",20)) #폰트,크기 조절
        #self.KeySetting.setStyleSheet("Color : blue") #글자색 변환

    def setUpdateLog(self, inputText):
        self.logString += inputText + "\n"
        self.LogText.setText(self.logString)

    def passKeyUIupdate(self, passChecker):
        if passChecker:
            self.KeySetting.setStyleSheet("Color : white;"
                                          "background-color: green;")
            
        else:
            self.KeySetting.setStyleSheet("Color : black;"
                                          "background-color: white;")
            
    def passThreshold(self, passChecker):
        if passChecker:
            self.InputText.setStyleSheet("Color : blue")
            self.GoPScore.setStyleSheet("Color : blue")
        else:
            self.InputText.setStyleSheet("Color : red")
            self.GoPScore.setStyleSheet("Color : red")

class settingUI(QDialog):
    def __init__(self, ui_path, userName, targetText, threshold, inputKey):
        super().__init__()

        # Load the UI
        loadUi(ui_path, self)

        # Get the combo box object
        self.nameText = self.findChild(QLineEdit, "nameText")
        self.targetText = self.findChild(QLineEdit, "targetText")
        self.thresholdBox = self.findChild(QDoubleSpinBox, "thresholdBox")
        self.inputKey = self.findChild(QComboBox, "keyBox")
        self.confirmButton= self.findChild(QPushButton, 'confirmButton')
        self.inputKey.addItems(["click", "space", "enter", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
        
        self.nameText.setText(userName)
        self.targetText.setText(targetText)
        self.thresholdBox.setValue(threshold)
        self.inputKey.setCurrentText(inputKey)

        # Set the items of the combo box
        #self.threshold_box.setValue(threshold)
        # Save text values when window is closed
        self.confirmButton.clicked.connect(self.save_text_values)

    def save_text_values(self):
        self.nameText = self.nameText.text()
        self.targetText = self.targetText.text()
        self.thresholdBox = self.thresholdBox.value()
        self.inputKey = self.inputKey.currentText()
        self.close()

    def get_userName(self):
        return self.nameText

    def get_targetWord(self):
        return self.targetText

    def get_threshold(self):
        return self.thresholdBox  #이건 코드상 오류가 발생될 수 있어서 임시로 설정

    def get_inputKey(self):
        return self.inputKey





if __name__ == '__main__':
    app = QApplication(sys.argv)
    uipath = 'path_to_your_ui_file.ui'  # Replace with your UI file path
    queue = []  # Replace with your data queue
    mainUI = AllMainUI(uipath, queue)
    mainUI.show()
    sys.exit(app.exec_())










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