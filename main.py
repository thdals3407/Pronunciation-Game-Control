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
from util.ToolArray import Mic_device_detector

windowSize = 640, 480

# UI Setting Paramter
user_name = ""
userid = 0
target_word = "mike"
threshold = 0.15
audio = pyaudio.PyAudio()
device_list, index_list = Mic_device_detector(audio)
device_index = 1

audio_queue = Queue()

# Audio Setting
format_type = pyaudio.paInt16
channels = 1
rate = 16000
frames_per_buffer = 3000
stream = audio.open(format=format_type, channels=channels, rate=rate, input=True,
                    frames_per_buffer=frames_per_buffer, input_device_index=device_index)

# GoP Setting
model = read_recognizer('eng2102')
phoneRecognition = PhoneRecognition(model, audio, format=pyaudio.paInt16, channels=channels, rate=rate,
                                    frames_per_buffer=frames_per_buffer, lang="eng")
phoneRecognition.set_topK(5)
phoneRecognition.set_emit(1)

gop = GoPScoring(target_word)
dpra = DPRA(threshold)

def get_audio(audio_queue):
    frames = bytearray()
    loop = False
    while True:
        while loop:
            data = stream.read(frames_per_buffer)
            frames.extend(data)
            cur_ipa = phoneRecognition.get_ipa(frames)  # 모델이 쌓인 Frames를 읽는 부분
            if len(cur_ipa) > 0:
                score = gop.GoP_Score1(cur_ipa)
                print(score)
                if score > threshold:   # Score이 Threshold보다 커지는지 확인하는 코드
                    frames = bytearray()    #
                    print("ket Input")
                    pydirectinput.press(["1"])
                elif len(frames) > rate * 2:  # 3초 이상 데이터를 쌓아두지 않도록 초기화 작업
                    frames = bytearray()
            elif len(frames) > rate * 2:  # 3초 이상 데이터를 쌓아두지 않도록 초기화 작업
                frames = bytearray()



            if not audio_queue.empty(): # Loop out Control
                loop = audio_queue.get_nowait()
                frames = bytearray()
        if not audio_queue.empty(): # Loog in Control
            loop = audio_queue.get_nowait()
            frames = bytearray()
        time.sleep(0.1)

def MarioPygameLoop():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
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
    print("setting Print : ", level, screen, dashboard, sound)
    clock = pygame.time.Clock()
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
    audio_process = Process(target=get_audio, args=(audio_queue,))
    audio_process.start()
    exitmessage = 'restart'
    while exitmessage == 'restart':
        print("Game Start")
        exitmessage = MarioPygameLoop()
        audio_queue.put(False)

    pygame.quit()
    audio.terminate()
    audio_process.join()