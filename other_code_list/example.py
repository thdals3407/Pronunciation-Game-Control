# -*- coding: utf-8 -*-
import gspeech
import time
import pyautogui
from tkinter import *
import threading

def main():
    target_word = "가"
    target_key = "a"
    gsp = gspeech.Gspeech()
    print("STT code Start")
    while True:
        # 음성 인식 될때까지 대기 한다.
        stt = gsp.getText()
        if stt is None:
            break
        print(stt)
        if SamepleTextInChecker(stt, target_word):
            pyautogui.press([target_key])
        time.sleep(0.001)
        if ('끝내자' in stt):
            break


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

if __name__ == '__main__':
    main()
