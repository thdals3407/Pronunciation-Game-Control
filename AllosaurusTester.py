from allosaurus.app import read_recognizer
import pyaudio
import wave
from util.IPATool import ipa_to_korean, korean_to_ipa
import pydirectinput
import numpy as np

model = read_recognizer('eng2102')
topk = 1
emit = 1.0
Text_1_path = 'TestCode/TestSound/word_pronunciation.wav'
Text_2_path = 'TestCode/TestSound/world_pronunciation.wav'

print(model.recognize(Text_1_path, lang_id='eng', topk=topk, emit=emit, timestamp=False))
print(model.recognize(Text_2_path, lang_id='eng', topk=topk, emit=emit, timestamp=False))

print("-----------------------------------------------------------------------")

Text2_1_path = 'TestCode/TestSound/word_j.wav'
Text2_2_path = 'TestCode/TestSound/world_j.wav'

print(model.recognize(Text2_1_path, lang_id='eng', topk=topk, emit=emit, timestamp=False))
print(model.recognize(Text2_2_path, lang_id='eng', topk=topk, emit=emit, timestamp=False))
