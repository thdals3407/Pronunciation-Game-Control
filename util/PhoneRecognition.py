from allosaurus.app import read_recognizer
import pyaudio
from util.IPATool import korean_to_ipa
from util.ToolArray import Mic_device_detector, frame2wav

class PhoneRecognition:
    def __init__(self, model, audio, format=pyaudio.paInt16, channels=1, rate=16000, frames_per_buffer=3000, emit=1, topk=5, lang = "kor"):
        self.model = model
        self.audio = audio
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.emit = emit
        self.topk = topk
        self.lang = lang
        self.model.streaming_setting(self.channels, self.rate, frames_per_buffer * 2, self.audio.get_sample_size(self.format))

    def set_model(self, model):
        self.model = model
    def set_target_word(self, target_word):
        self.target_word = target_word
        self.ipa_target_word = korean_to_ipa(target_word)
        print("target_word :", self.target_word)
    def set_Threshold(self, threshold):
        self.threshold = threshold
        print("Setting threshold : ", self.threshold)
    def set_topK(self, topK):
        self.topk = topK
    def set_emit(self, emit):
        self.emit = emit

    def get_ipa(self, data):
        self.text = ""
        self.ipa = self.model.recognize_Streaming(data, lang_id=self.lang, topk=self.topk, emit=self.emit)
        return self.ipa


if __name__ == '__main__':
    from multiprocessing import Process, Queue
    from GoP import GoPScoring
    audio = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 3000
    device_list, index_list = Mic_device_detector(audio)
    stream = audio.open(format=format, channels=channels, rate=rate, input=True,
                                  frames_per_buffer=frames_per_buffer, input_device_index=1)
    model = read_recognizer('kor2023')
    phoneRecognition = PhoneRecognition(model, audio, format=pyaudio.paInt16, channels=channels, rate=rate, frames_per_buffer=frames_per_buffer, lang="eng")
    phoneRecognition.set_topK(1)
    phoneRecognition.set_emit(1)
    audio_queue = Queue()
    frames = bytearray()
    test = 0

    gopModel = GoPScoring("마이크")
    score = 0
    while True:
        data = stream.read(frames_per_buffer)
        frames.extend(data)
        cur_ipa = phoneRecognition.get_ipa(frames)
        if len(cur_ipa) > 0:
            print(cur_ipa)
        """
        if len(cur_ipa) > 0:
            score = gopModel.GoP_Score1(cur_ipa)
            if score > 0.17:
                frame2wav([frames], "AudioTest/Test_wav_{}.wav".format(test), rate, audio, format, channels)
                test += 1
                frames = bytearray()
                print("reset")
            elif len(frames) > rate * 2:  #3초 이상 데이터를 쌓아두지 않도록 초기화 작업
                frames = bytearray()"""
        if len(frames) > rate * 2:  # 3초 이상 데이터를 쌓아두지 않도록 초기화 작업
            frames = bytearray()