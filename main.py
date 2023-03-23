import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
import pydirectinput
import time
windowSize = 640, 480

#from multiprocessing import Process

from Streaming_code import AudioRecorder
from allosaurus.app import read_recognizer
windowSize = 640, 480

def main():
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

    pydirectinput.keyDown("9")
    time.sleep(0.5)
    pydirectinput.keyUp("9")
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        print("test1")
        pydirectinput.keyDown("8")
        time.sleep(0.5)
        pydirectinput.keyUp("8")
        exitmessage = main()

    #exitmessage = 'restart'
    #model = read_recognizer('latest')
    #recorder = AudioRecorder()
    #main()
    #p1 = Process(target=recorder.gop_streaming_start, args=(model, "마이크"))
    #p2 = Process(target=main)
    #p2.start()
    #p1.start()