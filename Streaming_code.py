from allosaurus.app import read_recognizer
import pyaudio
import wave
from KoreanTool import ipa_to_korean, korean_to_ipa
import pydirectinput
import numpy as np
import keyboard
import time
# load your model

Thread_parameter = 0.5
model = read_recognizer('latest')
emit_this = 1.2

def Stt_ipa(wav_path):
    print("Wav File : ")
    print("----------------------")
    ipa = model.recognize(wav_path, lang_id='kor', emit=1)
    print(ipa)
    print(ipa_to_korean(ipa))
    print("----------------------")

def test_code():
    #Stt_ipa("MicSample1.wav")
    for i in range(1, 8):
        Stt_ipa("Sample" + str(i) + ".wav")

class AudioRecorder:
    def __init__(self, model, target_word, threshold=0.5, filename='AudioSample/output.wav', format=pyaudio.paInt16, channels=1, rate=16000, frames_per_buffer=2048):
        self.threshold = threshold
        self.filename = filename
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.audio = pyaudio.PyAudio()
        self.model = model
        self.target_word = target_word

    def set_target_word(self, target_word):
        self.target_word = target_word
        print("target_word ", self.target_word)

    def set_Thread(self, threshold):
        self.threshold = threshold
        print("Setting the intitial threshold : ", self.threshold)

    def start(self):
        print("recording Start")
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.frames = []

    def stop(self):
        print("recording Stop")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        waveFile = wave.open(self.filename, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()
        Stt_ipa("AudioSample/output.wav")

    def record(self, duration):
        for i in range(int(self.rate / self.frames_per_buffer * duration)):
            data = self.stream.read(self.frames_per_buffer)
            self.frames.append(data)

    def streaming_start(self):
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.data = self.stream.read(4000)
        self.model.streaming_setting(self.channels, self.rate, len(self.data), self.audio.get_sample_size(self.format))
        self.over_check = 2
        self.text = ""
        print("Start Streaming")
        while True:
            self.data = self.stream.read(4000)
            self.ipa = self.model.recognize_Streaming(self.data, lang_id="kor")
            if self.ipa != "":
                self.text += self.ipa
            else:
                if self.over_check < 0:
                    if self.text != "":
                        print("all ", self.text)
                        self.text = ""
                        self.over_check = 2
                else:
                    self.over_check -= 1

    def gop_streaming_start(self):
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.data = self.stream.read(3000)
        self.model.streaming_setting(self.channels, self.rate, len(self.data), self.audio.get_sample_size(self.format))
        self.over_check = 1
        self.text = ""
        self.score = 0
        self.gop_List = []
        print("Start Streaming")
        self.ipa_target_word = korean_to_ipa(self.target_word)
        while True:
            self.data = self.stream.read(3000)
            self.ipa = self.model.recognize_Streaming(self.data, lang_id="kor", topk=10, emit=emit_this)
            if self.ipa != "":
                self.text += self.ipa
            else:
                if self.text != "":
                    self.score = self.goP_Calculater(self.text, self.ipa_target_word)
                    self.gop_score_check(self.score)
                # if self.text != "":
                #     self.score = GoP_Calculater(self.text, self.ipa_target_word)
                #     print("target_word :", target_word, "-- Gop_Score :",self.score)
                #     self.gop_List.append(self.score)
                # self.text = ""
                if self.over_check < 0:
                    if self.text != "":
                        print("target_word :", self.target_word, "-- Gop_Score :", self.score)
                        self.gop_List.append(self.score)
                        self.text = ""
                        self.over_check = 3
                else:
                    self.over_check -= 1
            if keyboard.is_pressed("9"):
                self.Mgop_Scoring()
                break

    def goP_Calculater(self, input_ipa, target_ipa):
        score = 0.0
        tmp_ipa = input_ipa
        for i in range(len(target_ipa)):
            if target_ipa[i] != " ":
                if target_ipa[i] in tmp_ipa:
                    tmp_ipa = input_ipa[input_ipa.find(target_ipa[i]):]
                    score += float(tmp_ipa[tmp_ipa.find("(") + 1:tmp_ipa.find(")")])
        return score

    def gop_score_check(self, score):
        if score > self.threshold:
            pydirectinput.press(["p"])

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
    def delay_maker(self):
        while True:
            if keyboard.is_pressed("8"):
                break
            time.sleep(0.1)
            print("delay check")
if __name__ == '__main__':
    #test_code()
    recorder = AudioRecorder(model, "점프")
    #recorder.start()1
    #recorder.stop()
    #recorder.streaming_start(model)
    while True:
        recorder.delay_maker()
        recorder.gop_streaming_start()
