import pyaudio
import pygame
import time
import pydirectinput
from multiprocessing import Process, Queue
from allosaurus.app import read_recognizer
from util.PhoneRecognition import PhoneRecognition
from util.GoP import GoPScoring
from util.DPRA import DPRA
from util.IPATool import get_highest_symbols, ipa_to_korean
from util.ToolArray import Mic_device_detector, frame2wav
from util.UITool import startUI_all, scoreUI, mainUI
from PyQt5.QtWidgets import *
import audioop
audio_queue = Queue()
feedback_queue = Queue()
result_queue = Queue()
def StartUI(threshold, device_list, index_list):
    StartUI = startUI_all("util/StartUI_all.ui", device_list, threshold)
    StartUI.show()
    app.exec_()
    user_name = StartUI.get_userName()
    userid = StartUI.get_userId()
    target_word = StartUI.get_targetWord()
    inputKey = StartUI.get_inputKey()
    threshold = StartUI.get_threshold()
    device_index = index_list[device_list.index(StartUI.get_audioDevice())]
    print("-------In system-------")
    print(f"Name: {user_name}, ID: {userid}, Word: {target_word}, Thord: {threshold}, Audio: {device_index}, key: {inputKey}")
    print("-----------------------")
    #StartUI.close()
    return user_name, userid, target_word, threshold, device_index, inputKey

def ScoreUI_set(ScoreUI, feedback):
    ScoreUI.get_feedback_Scoring(feedback)
    ScoreUI.show()
    app.exec_()

def MainUI_set(MainUI):
    MainUI.show()
    app.exec_()

def get_audio(audio_queue,feedback_queue, target_word, threshold, device_index, userid, inputkey, result_queue):
    # Audio Setting
    format_type = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 3000
    audio = pyaudio.PyAudio()
    device_list, index_list = Mic_device_detector(audio)
    # GoP Setting
    model = read_recognizer('kor2023')
    phoneRecognition = PhoneRecognition(model, audio, format=format_type, channels=channels, rate=rate,
                                        frames_per_buffer=frames_per_buffer, lang="kor")
    phoneRecognition.set_topK(5)
    phoneRecognition.set_emit(1)
    if target_word == "" or target_word == " ":
        target_word = "테스트"
    gop = GoPScoring(target_word, lang="kor")
    dpra = DPRA(threshold/100, focus_variable=0.1)
    dpra.set_userid(userid)
    print("Mic device : ", device_list[index_list.index(device_index)])
    stream = audio.open(format=format_type, channels=channels, rate=rate, input=True,
                        frames_per_buffer=frames_per_buffer, input_device_index=device_index)
    frames = bytearray()
    loop = False
    label = 0
    phase = 0
    score = 0.0
    top_scoring_check = 0.0
    top_frames = bytearray()
    press_check = True
    top_ipa = ""
    while True:
        while loop:
            data = stream.read(frames_per_buffer)
            rms = audioop.rms(data, 2)
            if rms > 300:  # 소리를 감지
                frames.extend(data)
                cur_ipa = phoneRecognition.get_ipa(frames)
                if len(cur_ipa) > 0: # 음소 요소가 있음을 감지
                    score = gop.GoP_Score1(cur_ipa)
                    print("User Score: ", score)
                    if press_check: # 이번 발화에서 버튼을 누를 필요가 있는가?
                        if dpra.InputScore(score):  # Score가 통과 기준이 되는가?
                            print("Pass")
                            if inputkey == "click":
                                pydirectinput.click()
                            else:
                                pydirectinput.press([inputkey])
                            press_check = False
                            top_ipa = cur_ipa
                    if top_scoring_check < score: # 최고 Score을 업데이트
                        top_scoring_check = score
                        top_frames = frames
                        top_ipa = cur_ipa
                if len(frames) > rate * 5:  # 5초 이상 데이터를 쌓이지 않도록 초기화
                    dpra.addGoP(score)  # 음성 정보 저장
                    frame2wav([top_frames], "UserAudioClip/E2_User_{}_speech_{}.wav".format(userid, phase, label),
                              rate, audio, format_type, channels)
                    print("user Text", get_highest_symbols(top_ipa))
                    label += 1  # 데이터 저장
                    press_check = True
                    top_scoring_check = 0.0
                    top_frames = bytearray()
                    top_ipa = ""
                    frames = bytearray() # 파라미터 초기화

            else:   # 소리 없음을 감지
                if len(frames) > 0: # 앞 선 루프에 소리가 있었음을 감지
                    if len(frames) >= frames_per_buffer * 2 and score > 0: # 적어도 2번 이상의 루프에 감지 했음을 확인
                        dpra.addGoP(top_scoring_check)  # 음성 정보 저장
                        frame2wav([top_frames],
                                  "UserAudioClip/User_{}_phase{}_speech_{}.wav".format(userid, phase, label),
                                  rate, audio, format_type, channels)   # Wav로 사용자 음성 저장
                        print("user Text", ipa_to_korean(get_highest_symbols(top_ipa)), "top Score : ", top_scoring_check)
                        result_queue.put("입력 발음 : \n" + ipa_to_korean(get_highest_symbols(top_ipa))+ "\n\n 점수 : {}".format(int(top_scoring_check*100))+"점")
                        label += 1  # 데이터 저장
                        press_check = True
                        score = 0.0
                        top_scoring_check = 0.0
                        top_frames = bytearray()
                        top_ipa = ""
                        frames = bytearray()  # 파라미터 초기화
                    else:   #한번만 인식되었다는 것
                        press_check = True
                        top_scoring_check = 0.0
                        top_frames = bytearray()
                        top_ipa = ""
                        frames = bytearray()  # 파라미터 초기화

            if not audio_queue.empty(): # Loop out Control
                loop = audio_queue.get_nowait()
                frames = bytearray()
                #print("-----------------------")
                #print(dpra.get_Report())
                feedback_queue.put(dpra.get_Report())
                #print("-----------------------")
                dpra.restart()
        if not audio_queue.empty(): # Loop in Control
            loop = audio_queue.get_nowait()
            frames = bytearray()
            phase += 1
        time.sleep(0.1)

if __name__ == "__main__":
    # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
    #                    frames_per_buffer=3000, input_device_index=device_index)
    # UI Setting Paramter
    user_name = ""
    userid = 0
    target_word = "마이크"
    threshold = 15
    audio = pyaudio.PyAudio()
    device_list, index_list = Mic_device_detector(audio)
    device_index = 1
    app = QApplication([])
    user_name, userid, target_word, threshold, device_index, inputkey = StartUI(threshold, device_list, index_list)
    ScoreUI = scoreUI("util/ScoreUI.ui")
    ScoreUI.get_userName(user_name)
    MainUI = mainUI("util/MainUI.ui", result_queue)
    audio_process = Process(target=get_audio, args=(audio_queue, feedback_queue, target_word, threshold, device_index, userid, inputkey,result_queue, ))
    audio_process.start()
    exitmessage = 'restart'
    audio_queue.put(True)
    while exitmessage == 'restart':     # 게임의 시작과 종료를 반복시키는 루핑입니다.
        MainUI_set(MainUI)
        audio_queue.put(False)
        time.sleep(2)
        if feedback_queue.empty():
            ScoreUI_set(ScoreUI, "")
        else:
            ScoreUI_set(ScoreUI, feedback_queue.get_nowait())
        audio_queue.put(True)
    app.exit()
    audio.terminate()
    #audio_process.kill()
    audio_process.join()