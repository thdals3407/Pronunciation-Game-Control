from allosaurus.app import read_recognizer
import pyaudio
import wave
import numpy as np
from allosaurus.audio import Audio
from typing import Optional
from g2pk import G2p
from KoreanTool import ipa_to_korean



# load your model
model = read_recognizer('latest')
emit_this = 1.2

def Stt_ipa(wav_path):
    print("Wav File : ")
    print("----------------------")
    #ipa1 = model.recognize(wav_path, lang_id='kor', timestamp=False, emit=emit_this)
    ipa = model.recognize(wav_path, lang_id='kor', timestamp=True, emit=emit_this, topk=5)
    print(ipa)
    #print(ipa_to_korean(ipa1))
    print("----------------------")

def test_code():
    #Stt_ipa("MicSample1.wav")
    for i in range(1, 8):
        Stt_ipa("Sample" + str(i) + ".wav")


class AudioRecorder:
    def __init__(self, filename='AudioSample/output.wav', format=pyaudio.paInt16, channels=1, rate=16000, frames_per_buffer=2048):
        self.filename = filename
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.audio = pyaudio.PyAudio()

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
        print("check_st_nchannels", self.channels)
        print("check_st_sampwith", self.audio.get_sample_size(self.format))
        print("check_st_rate", self.rate)
        print("check_st_frame", len(b''.join(self.frames)))
        waveFile.close()

    def record(self, duration):
        for i in range(int(self.rate / self.frames_per_buffer * duration)):
            data = self.stream.read(self.frames_per_buffer)
            self.frames.append(data)

    def streaming_start(self, model):
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.data = self.stream.read(4000)
        model.streaming_setting(self.channels, self.rate, len(self.data), self.audio.get_sample_size(self.format))
        while True:
            self.data = self.stream.read(4000)
            # print("check_st_nchannels", self.channels)
            # print("check_st_sampwith", self.audio.get_sample_size(self.format))
            # print("check_st_rate", self.rate)
            # print("check_st_frame", len(self.data))
            text = model.recognize_Streaming(self.data)
            print(ipa_to_korean(text))


if __name__ == '__main__':
    #test_code()
    recorder = AudioRecorder()
    #recorder.start()
    #recorder.record(0.18)  # 5초 동안 녹음
    #recorder.stop()
    #Stt_ipa("AudioSample/output.wav")
    recorder.streaming_start(model)