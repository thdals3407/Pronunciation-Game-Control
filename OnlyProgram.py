import pyaudio
import pygame
import time
import pydirectinput
from multiprocessing import Process, Queue
from allosaurus.app import read_recognizer
from util.PhoneRecognition import PhoneRecognition
from util.GoP import GoPScoring
from util.DPRA import DPRA
from util.IPATool import get_highest_symbols, ipa_to_korean, string_to_hangul, korean_to_ipa
from util.ToolArray import Mic_device_detector, frame2wav
from util.UITool import startUI_all, scoreUI, AllMainUI, settingUI
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
    #userid = StartUI.get_userId()
    target_word = StartUI.get_targetWord()
    if target_word == "":
        target_word = "마이크테스트"
    inputKey = StartUI.get_inputKey()
    threshold = StartUI.get_threshold()
    device_index = index_list[device_list.index(StartUI.get_audioDevice())]
    print("-------In system-------")
    print(f"Name: {user_name}, Word: {target_word}, Threshold: {threshold}, Audio: {device_index}, key: {inputKey}")
    print("-----------------------")
    #StartUI.close()
    return user_name, target_word, threshold, device_index, inputKey

def SettingUI(userName, target_word, threshold, inputKey):
    SettingUI = settingUI("util/SettingUI.ui", userName, target_word, threshold, inputKey) 
    SettingUI.show()
    app.exec_()
    userName = SettingUI.get_userName()
    #userid = StartUI.get_userId()
    target_word = SettingUI.get_targetWord()
    if target_word == "":
        target_word = "마이크테스트"
    threshold = SettingUI.get_threshold()
    inputKey = SettingUI.get_inputKey()
    print("-------In system-------")
    print(f"Name: {userName}, Word: {target_word}, Threshold: {threshold}, key: {inputKey}")
    print("-----------------------")
    #StartUI.close()
    return userName, target_word, threshold, inputKey



"""def ScoreUI_set(ScoreUI, feedback):
    ScoreUI.get_feedback_Scoring(feedback)
    ScoreUI.show()
    app.exec_()"""

def MainUI_set(MainUI):
    MainUI.show()
    app.exec_()




def get_audio(audio_queue, feedback_queue, target_word, threshold, device_index, inputKey, result_queue, user_name):
    # Audio Setting
    format_type, channels, rate, frames_per_buffer = pyaudio.paInt16, 1, 16000, 3000
    audio = pyaudio.PyAudio()
    device_list, index_list = Mic_device_detector(audio)

    # GoP Setting
    model = read_recognizer('kor2023')
    phoneRecognition = PhoneRecognition(model, audio, format=format_type, channels=channels, rate=rate,
                                        frames_per_buffer=frames_per_buffer, lang="kor")
    phoneRecognition.set_topK(2)
    phoneRecognition.set_emit(1)
    if target_word == "" or target_word == " ":
        target_word = "테스트"
    gop = GoPScoring(target_word, lang="kor")

    # DPRA Setting
    dpra = DPRA(threshold/100, focus_variable=0.1)
    dpra.set_userid(0) # 그냥 오류 방지용으로 설정, 이후에 필요하다면 ID값은 여기서 설정
    print("Mic device : ", device_list[index_list.index(device_index)])
    stream = audio.open(format=format_type, channels=channels, rate=rate, input=True,
                        frames_per_buffer=frames_per_buffer, input_device_index=device_index)
    
    # Initial Setting
    frames, top_frames = bytearray(), bytearray()
    score, top_scoring = 0.0, 0.0
    press_check, loop = True, False
    label, phase, top_ipa = 0, 0, ""

    while True:
        while loop == True:
            data = stream.read(frames_per_buffer)
            rms = audioop.rms(data, 2)
            if rms > 300:  # 소리를 감지
                frames.extend(data)
                cur_ipa = phoneRecognition.get_ipa(frames)
                #print(cur_ipa)
                if len(cur_ipa) > 0: # 음소 요소가 있음을 감지
                    score = gop.GoP_Score1(cur_ipa)
                    print("User Score: ", score)
                    if press_check and dpra.InputScore(score): # 이번 발화에서 버튼을 누를 필요가 있는가?
                        #print("Pass")
                        if inputKey == "click":
                            pydirectinput.click()
                        else:
                            pydirectinput.press([inputKey])
                        press_check = False
                        top_ipa = cur_ipa
                    if top_scoring < score: # 최고 Score을 업데이트
                        top_scoring, top_frames, top_ipa = score, frames, cur_ipa

                if len(frames) > rate * 5:  # 5초 이상 데이터를 쌓이지 않도록 초기화 >> 거의 없음..
                    print("Initialize Setting")
                    dpra.addGoP(score)  # 음성 정보 저장
                    frame2wav([top_frames], "UserAudioClip/E2_User_{}_speech_{}.wav".format(user_name, phase, label),
                              rate, audio, format_type, channels)
                    #print("user Text", get_highest_symbols(top_ipa))
                    label += 1  # 데이터 저장
                    press_check = True
                    top_scoring, top_frames, top_ipa = 0.0, bytearray(), ""
                    frames = bytearray() # 파라미터 초기화

            else:   # 소리 없음을 감지
                if len(frames) > 0: # 앞 선 루프에 소리가 있었음을 감지
                    if len(frames) >= frames_per_buffer * 2 and score > 0: # 적어도 2번 이상의 루프에 감지 했음을 확인
                        passChecker = dpra.addGoP(top_scoring)  # 음성 정보 저장
                        frame2wav([top_frames],
                                  "UserAudioClip/User_{}_phase{}_speech_{}.wav".format(user_name, phase, label),
                                  rate, audio, format_type, channels)   # Wav로 사용자 음성 저장
                        #print("top_ipa", top_ipa)
                        #print("Test check", get_highest_symbols(top_ipa))
                        try:
                            result_hangul = string_to_hangul(ipa_to_korean(get_highest_symbols(top_ipa)))
                        except:
                            print("index error")
                            result_hangul = ""
                        if len(result_hangul) > 0:
                            result_queue.put([result_hangul, ipa_to_korean(get_highest_symbols(top_ipa)), top_scoring, dpra.get_Thread(), passChecker])
                        label += 1  # 데이터 저장
                        score = 0.0 
                    # 셋팅 초기화
                    press_check = True
                    top_scoring, top_frames, top_ipa = 0.0, bytearray(), ""
                    frames = bytearray()  # 파라미터 초기화
            if not audio_queue.empty(): # Loop out Control
                loop = audio_queue.get_nowait()
                if loop == 'exit':  # 종료 신호 확인
                    break
                frames = bytearray()
                # print("-----------------------")
                # print(dpra.get_Report())
                # feedback_queue.put(dpra.get_Report())
                # print("-----------------------")
                # dpra.restart()
        if not audio_queue.empty(): # Loop in Control
            loop = audio_queue.get_nowait()
            if loop == 'exit':  # 종료 신호 확인
                break
            if type(loop) == list:  # [user_name, target_word, threshold, inputKey]
                print("Change Setting :", loop)
                user_name = loop[0]
                target_word = loop[1]
                gop.set_target_word(target_word)
                # threshold는 일단 보류
                inputKey = loop[3]
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
    threshold = 70  
    audio = pyaudio.PyAudio()
    device_list, index_list = Mic_device_detector(audio)
    device_index = 1
    
    app = QApplication([])
    user_name, target_word, threshold, device_index, inputKey = StartUI(threshold, device_list, index_list)
    #ScoreUI = scoreUI("util/ScoreUI.ui")
    #ScoreUI.get_userName(user_name)
    MainUI = AllMainUI("util/AllMainUI.ui", result_queue, threshold)
    MainUI.setTargetText(target_word + "({})\n".format(korean_to_ipa(target_word)[1]) + korean_to_ipa(target_word)[2])
    MainUI.setUserName(user_name)
    MainUI.setkeySetting(inputKey)
    audio_process = Process(target=get_audio, args=(audio_queue, feedback_queue, target_word, threshold, device_index, inputKey, result_queue, user_name, ))
    audio_process.start()
    exitmessage = 'restart'
    while True:
        audio_queue.put(True)   # 오디오 THread 켜기
        time.sleep(4) # 오디오 설정과 프로그램 시간을 맞추기 위한 설정
        MainUI_set(MainUI)
        audio_queue.put(False)  # 오디오 THread 끄기
        loopchekcer = MainUI.getNextUIIndex()
        if loopchekcer == 1:    #설정창 열기
            user_name, target_word, threshold, inputKey = SettingUI(user_name, target_word, threshold, inputKey)
            MainUI.setNextUIIndex(-1)
            MainUI.setTargetText(target_word + "({})\n".format(korean_to_ipa(target_word)[1]) + korean_to_ipa(target_word)[2])
            MainUI.setUserName(user_name)
            MainUI.setkeySetting(inputKey)
            MainUI.setFixedThreshold(threshold)
            audio_queue.put([user_name, target_word, threshold, inputKey])
            time.sleep(0.5)
        else:
            break

    # System Exit Code
    print("System Exit")
    time.sleep(0.1)
    audio_queue.put('exit')
    audio_process.join()
    app.exit()
    audio.terminate()