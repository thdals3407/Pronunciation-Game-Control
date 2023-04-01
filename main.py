import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
import pydirectinput
import time
windowSize = 640, 480

from multiprocessing import Process

from Streaming_code import Pstreaming
from allosaurus.app import read_recognizer
model = read_recognizer('latest')
windowSize = 640, 480

def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    #pstreaming =Pstreaming(model, "갸")
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    print("setting Print : ", level, screen, dashboard, sound)
    clock = pygame.time.Clock()
    pstreaming.sequence_streaming_setting()
    while not mario.restart:
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        pstreaming.sequence_streaming()
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
    pstreaming = Pstreaming(model, "갸")
    #p1 = Process(target=pstreaming.streaming_start)
    #exitmessage = 'restart'
    #p1.start()
    while exitmessage == 'restart':
        print("Game Start")
        exitmessage = main()

# pstreaming = Pstreaming(model, "갸")
# p1 = Process(target=pstreaming.streaming_start())
# exitmessage = 'restart'
# p1.start()


#exitmessage = 'restart'
#model = read_recognizer('latest')
#pstreaming =Pstreaming(model, "갸")
#main()
#p1 = Process(target=pstreaming.streaming_start, args=(model, "마이크"))
#p2 = Process(target=main)
#p1.start()
#p2.start()