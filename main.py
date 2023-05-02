import pyaudio
import pygame
import time
import pydirectinput
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
from multiprocessing import Process, Queue
from allosaurus.app import read_recognizer
from util.PhoneRecognition import PhoneRecognition
from util.GoP import GoPScoring
from util.DPRA import DPRA
from util.ToolArray import Mic_device_detector, frame2wav
from util.UITool import startUI, scoreUI
from PyQt5.QtWidgets import *
import audioop
audio_queue = Queue()
feedback_queue = Queue()

def StartUI(threshold, device_list, index_list):
    app = QApplication([])
    StartUI = startUI("util/StartUI.ui", device_list, threshold)
    StartUI.show()
    app.exec_()

    user_name = StartUI.get_userName()
    userid = StartUI.get_userId()
    target_word = StartUI.get_targetWord()
    threshold = StartUI.get_threshold()
    device_index = index_list[device_list.index(StartUI.get_audioDevice())]
    print("-------In system-------")
    print(f"Name: {user_name}, ID: {userid}, Word: {target_word}, Threshold: {threshold}, Audio: {device_index}")
    print("-----------------------")
    #StartUI.close()
    app.exit()
    return user_name, userid, target_word, threshold, device_index

def ScoreUI(feedback, user_name):
    app = QApplication([])
    ScoreUI = scoreUI("util/ScoreUI.ui", feedback, user_name)
    ScoreUI.show()
    app.exec_()
    app.exit()

def get_audio(audio_queue,feedback_queue, target_word, threshold, device_index, userid):
    # Audio Setting
    format_type = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 3000
    audio = pyaudio.PyAudio()
    device_list, index_list = Mic_device_detector(audio)
    # GoP Setting
    model = read_recognizer('uni2005')
    phoneRecognition = PhoneRecognition(model, audio, format=format_type, channels=channels, rate=rate,
                                        frames_per_buffer=frames_per_buffer, lang="kor")
    phoneRecognition.set_topK(5)
    phoneRecognition.set_emit(1)

    gop = GoPScoring(target_word, lang="kor")
    dpra = DPRA(threshold, focus_variable=0.1)
    dpra.set_userid(userid)
    #gop.set_target_word(target_word)
    #dpra.set_Thread(threshold)

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
    while True:
        while loop:
            data = stream.read(frames_per_buffer)
            rms = audioop.rms(data, 2)
            if rms > 2000:  # 소리를 감지
                frames.extend(data)
                cur_ipa = phoneRecognition.get_ipa(frames)
                if len(cur_ipa) > 0: # 음소 요소가 있음을 감지
                    score = gop.GoP_Score1(cur_ipa)
                    print("User Score: ",score)
                    if press_check: # 이번 발화에서 버튼을 누를 필요가 있는가?
                        if dpra.InputScore(score):  # Score가 통과 기준이 되는가?
                            print("Pass")
                            pydirectinput.press(["1"])
                            press_check = False
                    if top_scoring_check < score: # 최고 Score을 업데이트
                        top_frames = frames
                if len(frames) > rate * 5:  # 5초 이상 데이터를 쌓이지 않도록 초기화
                    dpra.addGoP(score)  # 음성 정보 저장
                    frame2wav([top_frames], "UserAudioClip/User_{}_phase{}_speech_{}.wav".format(userid, phase, label),
                              rate, audio, format_type, channels)
                    label += 1  # 데이터 저장
                    press_check = True
                    top_scoring_check = 0.0
                    top_frames = bytearray()
                    frames = bytearray() # 파라미터 초기화

            else:   # 소리 없음을 감지
                if len(frames) > 0: # 앞 선 루프에 소리가 있었음을 감지
                    if len(frames) >= frames_per_buffer * 2 and score > 0: # 적어도 2번 이상의 루프에 감지 했음을 확인
                        dpra.addGoP(score)  # 음성 정보 저장
                        frame2wav([top_frames],     
                                  "UserAudioClip/User_{}_phase{}_speech_{}.wav".format(userid, phase, label),
                                  rate, audio, format_type, channels)   # Wav로 사용자 음성 저장
                        label += 1  # 데이터 저장
                        press_check = True
                        score = 0.0
                        top_scoring_check = 0.0
                        top_frames = bytearray()
                        frames = bytearray()  # 파라미터 초기화
                    else:   #한번만 인식되었다는 것
                        press_check = True
                        top_scoring_check = 0.0
                        top_frames = bytearray()
                        frames = bytearray()  # 파라미터 초기화

            """
            frames.extend(data)
            cur_ipa = phoneRecognition.get_ipa(frames)  # 모델이 쌓인 Frames를 읽는 부분
            if len(cur_ipa) > 0:
                score = gop.GoP_Score1(cur_ipa)
                print(score)
                if dpra.InputScore(score):   # Score이 Threshold보다 커지는지 확인하는 코드
                    print("over check")
                    pydirectinput.press(["1"])
                    frame2wav([frames], "UserAudioClip/User_{}_phase{}_speech_{}.wav".format(userid, phase, label), rate, audio, format_type, channels)
                    frames = bytearray()
                    dpra.addGoP(score)
                    label += 1
                elif len(frames) > rate * 2:  # 3초 이상 데이터를 쌓아두지 않도록 초기화 작업
                    dpra.addGoP(score)
                    frames = bytearray()
            elif len(frames) > rate * 2:  # 3초 이상 데이터를 쌓아두지 않도록 초기화 작업
                frames = bytearray()
            """
            if not audio_queue.empty(): # Loop out Control
                loop = audio_queue.get_nowait()
                frames = bytearray()
                #print("-----------------------")
                #print(dpra.get_Report())
                feedback_queue.put(dpra.get_Report())
                #print("-----------------------")
        if not audio_queue.empty(): # Loop in Control
            loop = audio_queue.get_nowait()
            frames = bytearray()
            phase += 1
        time.sleep(0.1)

def MarioPygameLoop():
    windowsize = (640, 480)
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowsize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()
    mario = Mario(0, 0, level, screen, dashboard, sound)
    audio_queue.put(True)
    print("Speech process start")
    clock = pygame.time.Clock()
    time.sleep(2)
    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'

if __name__ == "__main__":
    # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
    #                    frames_per_buffer=3000, input_device_index=device_index)
    # UI Setting Paramter
    user_name = ""
    userid = 0
    target_word = "마이크"
    threshold = 0.15
    audio = pyaudio.PyAudio()
    device_list, index_list = Mic_device_detector(audio)
    device_index = 1

    user_name, userid, target_word, threshold, device_index = StartUI(threshold, device_list, index_list)
    audio_process = Process(target=get_audio, args=(audio_queue, feedback_queue, target_word, threshold, device_index, userid, ))
    audio_process.start()
    exitmessage = 'restart'
    while exitmessage == 'restart':     # 게임의 시작과 종료를 반복시키는 루핑입니다.
        print("Game Start")
        exitmessage = MarioPygameLoop()
        audio_queue.put(False)
        time.sleep(2)
        ScoreUI(feedback_queue.get_nowait(), user_name)

    pygame.quit()
    audio.terminate()
    audio_process.kill()
    audio_process.join()