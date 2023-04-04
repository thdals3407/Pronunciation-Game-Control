from util.IPATool import korean_to_ipa

class GoPScoring:
    def __init__(self, target_word):
        self.target_word = target_word
        self.target_ipa = korean_to_ipa(target_word)

    def set_target_word(self, target_word):
        self.target_word = target_word
        self.target_ipa = korean_to_ipa(target_word)
    def get_target_word(self):
        return self.target_word
    def get_target_ipa(self):
        return self.target_ipa
    def GoP_Score1(self, input_ipa):
        score = 0.0
        tmp_ipa = input_ipa
        for i in range(len(self.target_ipa)):
            if self.target_ipa[i] != " ":
                if self.target_ipa[i] in tmp_ipa:
                    tmp_ipa = input_ipa[input_ipa.find(self.target_ipa[i]):]
                    score += float(tmp_ipa[tmp_ipa.find("(") + 1:tmp_ipa.find(")")])
        return score / len(self.target_ipa)

