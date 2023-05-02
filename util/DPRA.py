import pydirectinput
import numpy as np
from util.IPATool import ipa_to_korean, korean_to_ipa
class DPRA:
    def __init__(self, threshold=0.11, outputKeySetting = "1", target_acc=0.7, focus_variable=0.01, userid=0):
        self.threshold = threshold
        self.outputKeySetting = outputKeySetting
        self.gop_list = []
        self.scoring_list = []
        self.pass_list = []
        self.threshold_list = []
        self.target_acc = target_acc
        self.r = focus_variable
        self.userid = userid
        self.outputString = "User id : {} \n\n".format(self.userid) # Reporter 구분용 코드
        #self.threshold_list.append(threshold)
    def Initialize(self):
        self.gop_list = []
        self.pass_list = []
        self.score_array = np.array([])
        self.threshold_list = []
        self.scoring_list = []
    def set_Thread(self, threshold):
        self.threshold = threshold
    def set_outputKeySetting(self, keyString):
        self.outputKeySetting = keyString
    def set_userid(self, userid):
        self.userid = userid
    def get_Thread(self):
        return self.threshold
    def get_outputKeySetting(self):
        return self.outputKeySetting
    def InputScore(self, score):  # Threshold보다 값이 크면 키가 입력되도록 설정하s는 코드
        return score > self.threshold
    def addGoP(self, FinalGop):
        self.gop_list.append(FinalGop)
        if FinalGop > self.threshold: #통과하는지 여부 체크용 함수
            self.pass_list.append(1)
        else:
            self.pass_list.append(0)
        if len(self.gop_list) > 9:  # 10회 진행할 경우 DPRA가 적용되도록 설정
            self.Mgop_Scoring()
    def accuracy_caculater(self):
        return sum(self.pass_list) / len(self.pass_list)

    def outputString_Scoring(self, score_array):
        self.outputString += "각 발음별 점수      : \n"
        for i in range(len(score_array)):
            self.outputString += f"{i+1} 회:" + str(int(score_array[i]*100)) + "점\n"
    def outputString_Threshold(self, beforeThreshold, atferThreshold):
        self.outputString += "난이도 변경 :  {}  >>  {} \n".format(beforeThreshold, atferThreshold)
        self.outputString += "--------------------"
    def outputString_TotalScoring(self, meanScoring, accuruacy):
        self.outputString +="--------------------"
        self.outputString += "평균: {} / 100, 정확도: {} \n".format(meanScoring, accuruacy)
        self.outputString += "정확도    :  {} % \n".format(accuruacy)

    def Mgop_Scoring(self): # 최종적으로 Threasold를 업데이트 시키는 함수
        self.score_array = np.array(self.gop_list)
        if len(self.score_array) > 0:
            self.score_acc = self.accuracy_caculater()
            #self.outputString_Scoring(self.score_array)
            #self.outputString_TotalScoring(int(np.mean(self.score_array)*100), int(self.score_acc * 100))
            print(self.score_array)
            print("평균 점수    :", int(np.mean(self.score_array) * 100))
            print("정확도  :", int(self.score_acc * 100))
            self.update_Threshold(self.score_acc)
            self.Initialize()
    def update_Threshold(self, acc):
        if len(self.gop_list) > 0:
            self.threshold -= self.r * (self.target_acc - acc)
            #self.outputString_Threshold(self.threshold + self.r * (self.target_acc - acc), self.threshold)
            print("Update Thershold :", self.threshold + self.r * (self.target_acc - acc), " >> ", self.threshold)
            self.threshold_list.append(self.threshold)
            self.scoring_list.append(self.gop_list)
        else:
            print("There isn't any data of user score")

    def get_Report(self):
        #return self.outputString
        self.scoring_list.append(self.gop_list)
        self.threshold_list.append(self.threshold)
        output = []
        output.append(self.threshold_list)
        output.append(self.scoring_list)
        return output