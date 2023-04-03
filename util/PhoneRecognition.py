from allosaurus.app import read_recognizer
import pyaudio
from util.IPATool import korean_to_ipa

class PhoneRecognition:
    def __init__(self, model, audio, format=pyaudio.paInt16, channels=1, rate=16000, frames_per_buffer=2048):
        self.model = model
        self.audio = audio
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
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
    def get_ipa(self, data):
        self.over_check = 1
        self.text = ""
        self.ipa = self.model.recognize_Streaming(data, lang_id="kor", topk=10, emit=1.1)
        return self.ipa


if __name__ == '__main__':
    audio = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 1024
    for index in range(audio.get_device_count()):
        desc = audio.get_device_info_by_index(index)
        device_list = []
        index_list = []
        if "마이크" in desc['name'] or "mic" in desc['name']:
            device_list.append(desc['name'] )
            index_list.append(index)
    for i in range(len(index_list)):
        print("DEVICE: {device}, INDEX: {index}".format(
            device=device_list[i], index=index_list[i]))

    stream = audio.open(format=format, channels=channels, rate=rate, input=True,
                                  frames_per_buffer=frames_per_buffer, input_device_index=0)

    model = read_recognizer('latest')
    recorder = PhoneRecognition(model, audio, format=pyaudio.paInt16, channels=channels, rate=rate, frames_per_buffer=frames_per_buffer)
    while True:
        data = stream.read(frames_per_buffer)
        ipa = recorder.get_ipa(data)
        if len(ipa) > 0:
            print(recorder.get_ipa(data))