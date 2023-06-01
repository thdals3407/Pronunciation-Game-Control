from util.IPATool import korean_to_ipa, split_ipa, ipa_to_korean#, english_to_ipa

class GoPScoring:
    def __init__(self, target_word, lang = "kor"):
        self.target_word = target_word
        self.lang = lang
        if self.lang == "kor":
            self.target_ipa = split_ipa(korean_to_ipa(target_word))
        #else:
            #self.target_ipa = english_to_ipa(target_word)
    def set_target_word(self, target_word):
        self.target_word = target_word
        if self.lang == "kor":
            self.target_ipa = split_ipa(korean_to_ipa(target_word))
        #else:
            #self.target_ipa = english_to_ipa(target_word)
    def get_target_word(self):
        return self.target_word
    def get_target_ipa(self):
        return self.target_ipa
    def GoP_Score1(self, input_ipa):
        score = 0.0
        tmp_ipa = input_ipa
        userText= ""
        for i in range(len(self.target_ipa)):
            if self.target_ipa[i] != " ":
                if self.target_ipa[i] in tmp_ipa:
                    tmp_ipa = input_ipa[input_ipa.find(self.target_ipa[i]):]
                    score += float(tmp_ipa[tmp_ipa.find("(") + 1:tmp_ipa.find(")")])
                    userText += self.target_ipa[i]
        # print(input_ipa.count("|") + 1, " | ", score / len(self.target_ipa))
        # if len(self.target_ipa) < input_ipa.count("|") + 1:
        #     return (score / len(self.target_ipa)) / (input_ipa.count("|") + 1 - len(self.target_ipa))
        # else:
        return (score / len(self.target_ipa))