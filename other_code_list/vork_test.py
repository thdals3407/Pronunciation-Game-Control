"""import vosk
import sys
import os
import pyaudio

# 모델과 언어 모델 로드
model_path = 'vosk-model-small-ko-0.22'
if not os.path.exists(model_path):
    print("Please download a model for your language from https://alphacephei.com/vosk/models")
    exit(1)

model = vosk.Model(model_path)

# 마이크 스트림 시작
sample_rate=16000
frame_size=4000
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=frame_size)

# Vosk ASR 인식기 초기화
rec = vosk.KaldiRecognizer(model, sample_rate)

while True:
    data = stream.read(frame_size)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        print(result)

# 나머지 음성 데이터 처리
result = rec.FinalResult()
print(result)"""

import vosk
import pyaudio
import json

model_path = "vosk-model-small-ko-0.22"
sample_rate = 16000
channels = 1
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, sample_rate)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=4000)

while True:
    data = stream.read(4000)
    #print(data)
    if len(data) == 0:
        break
    print("check1", channels)
    print("check2")
    print("check3")
    print("check4")
    print("check5")
    if rec.AcceptWaveform(data):
        if rec.Result() != "":
            text = rec.Result()
            #print(rec.Result())
    else:
        text = rec.PartialResult()
        if(text[16: len(text)-2] != '""'):
            print(text[16: len(text)-2])
        #print(rec.PartialResult())

result = json.loads(rec.FinalResult())
print(result['text'])