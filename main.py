import pyaudio
import pygame

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

windowSize = 640, 480

audio = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
audio_queue = Queue()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
model = read_recognizer('latest')
target_word = '테스트'
threshold = 0.3



def get_audio(audio_queue):
    while True:
        data = stream.read(CHUNK)
        audio_queue.put(data)

def main(audio_queue):
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    recorder = PhoneRecognition(model, audio, format=pyaudio.paInt16, channels=CHANNELS, rate=RATE,
                                frames_per_buffer=CHUNK)
    gop = GoPScoring(target_word)
    dpra = DPRA(threshold = threshold)
    while not menu.start:
        menu.update()
    mario = Mario(0, 0, level, screen, dashboard, sound)
    print("setting Print : ", level, screen, dashboard, sound)
    print("voice Setting Print : ", target_word, threshold)
    clock = pygame.time.Clock()
    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        if not audio_queue.empty():
            data = audio_queue.get()
            print(recorder(data))
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    audio_process = Process(target=get_audio, args=(audio_queue,))
    audio_process.start()
    exitmessage = 'restart'
    while exitmessage == 'restart':
        print("Game Start")
        exitmessage = main(audio_queue)

    pygame.quit()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_process.join()