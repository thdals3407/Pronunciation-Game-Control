import pydirectinput
import numpy as np
from util.IPATool import ipa_to_korean, korean_to_ipa

class DPRA:
    def __init__(self, threshold=0.3, outputKeySetting = "1", target_acc = 0.8, focus_variable = 0.4):
        self.threshold = threshold
        self.outputKeySetting = outputKeySetting
        self.gop_list = []
        self.target_acc = target_acc
        self.r = focus_variable
    def Initialize(self):
        self.gop_list = []
    def set_Thread(self, threshold):
        self.threshold = threshold
    def set_outputKeySetting(self, keyString):
        self.outputKeySetting = keyString
    def get_Thread(self):
        return self.threshold
    def get_outputKeySetting(self):
        return self.outputKeySetting
    def InputScore(self, score):  # Threshold보다 값이 크면 키가 입력되도록 설정하는 코드
        if score > self.threshold:
            pydirectinput.press([self.outputKeySetting])
    def addGoP(self, FinalGop):
        self.gop_list.append(FinalGop)

    def accuracy_caculater(self, score_array, threshold):
        count = 0
        for i in score_array:
            if i > threshold:
                count += 1
        return count / len(score_array)

    def Mgop_Scoring(self): # mean of Scoring을 추출해서
        self.streaming = False
        self.score_array = np.array(self.gop_List)
        if len(self.score_array) > 0:
            self.score_acc = self.accuracy_caculater(self.score_array, self.threshold)
            print(self.score_array)
            print("Mean of GoP    :", np.mean(self.score_array))
            print("Acc of Score   :", self.score_acc)
            self.DPRA(self.score_acc)

    def DPRA(self, acc):
        if len(self.gop_List) > 0:
            self.threshold -= self.r * (self.target_acc - acc)
            self.gop_List = []
            print("update Thershold :", self.threshold + self.r * (self.target_acc - acc),  " >> ", self.threshold)
        else:
            print("There isn't any data of user score")