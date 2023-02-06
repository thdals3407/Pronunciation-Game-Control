
import gspeech
import pyautogui
from tkinter import *
from multiprocessing import Process
from joysticController import input_test
import time

target_word = "가"
target_key = "a"


def STT_Speech():
    #gsp = gspeech.Gspeech()
    print("STT code Start")
"""    while True:
        # 음성 인식 될때까지 대기 한다.
        stt = gsp.getText()
        if stt is None:
            break
        print(stt)
        if SamepleTextInChecker(stt, target_word):
            pyautogui.press([target_key])
        #time.sleep(0.001)
        if ('끝' in stt):
            break"""

def SamepleTextInChecker(stt, target_word):
    text_length = len(target_word)
    user_score = 0
    for i in range(text_length):
        if target_word[i] in stt:
            user_score += 1
    if user_score/text_length > 0.4:
        return True
    else:
        return False

def TMP_key_setting():
    program.Axis_Setting(0, "a")

def Joystic_controller():
    program = input_test()
    program.init()
    program.run()  # This function should never return

if __name__ == '__main__':
    p0 = Process(target=STT_Speech)
    p1 = Process(target=Joystic_controller)
    p0.start()
    p1.start()
    print("main Process is done")