from static.util import ipa_to_korean, korean_to_ipa
import numpy as np

# load your model


class DPRA:
    def __init__(self, threshold, target_acc=0.8, r=0.4):
        self.threshold = threshold
        self.target_acc = target_acc
        self.learning_rate = r

    def get_threshold(self):
        return self.threshold

    def goP_Calculater(self, input_ipa, target_ipa):
        score = 0.0
        tmp_ipa = input_ipa
        for i in range(len(target_ipa)):
            if target_ipa[i] != " ":
                if target_ipa[i] in tmp_ipa:
                    tmp_ipa = input_ipa[input_ipa.find(target_ipa[i]):]
                    score += float(tmp_ipa[tmp_ipa.find("(") + 1:tmp_ipa.find(")")])
        return score

    def Mgop_Scoring(self):
        self.streaming = False
        self.score_array = np.array(self.gop_List)
        if len(self.score_array) > 0:
            self.score_acc = self.accuracy_caculater(self.score_array, self.threshold)
            print(self.score_array)
            print("Mean of GoP    :", np.mean(self.score_array))
            print("Acc of Score   :", self.score_acc)
            self.DPRA(self.score_acc)

    def DPRA(self, acc, target_acc=0.8, r=0.4):
        if len(self.gop_List) > 0:
            self.threshold -= r * (target_acc - acc)
            self.gop_List = []
            print("update Thershold :", self.threshold + r * (target_acc - acc),  " >> ", self.threshold)
        else:
            print("There isn't any data of user score")

    def accuracy_caculater(self, score_array, threshold):
        count = 0
        for i in score_array:
            if i > threshold:
                count += 1
        return count / len(score_array)
