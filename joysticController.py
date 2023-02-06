#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 et
#
# This tool runs fine on both Python 2 and Python 3.
#
# https://github.com/denilsonsa/pygame-joystick-test

from __future__ import division
from __future__ import print_function

import os

# I see no reason to disable screensaver for this tool.
os.environ["SDL_VIDEO_ALLOW_SCREENSAVER"] = "1"

# Maybe people want to keep watching the joystick feedback even when this
# window doesn't have focus. Possibly by capturing this window into OBS.
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# A tiny performance/latency hit isn't a problem here. Instead, it's more
# important to keep the desktop compositing effects running fine. Disabling
# compositing is known to cause issues on KDE/KWin/Plasma/X11 on Linux.
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"


import sys
import pygame
from pygame.locals import *

import pyautogui
import gspeech

class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes    = self.joy.get_numaxes()
        self.numballs   = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats    = self.joy.get_numhats()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))


class input_test(object):
    class program:
        "Program metadata"
        name    = "Pygame Joystick Test"
        version = "0.2"
        author  = "Denilson Figueiredo de Sá Maia"
        nameversion = name + " " + version

    class default:
        "Program constants"
        fontnames = [
            # Bold, Italic, Font name
            (0, 0, "Bitstream Vera Sans Mono"),
            (0, 0, "DejaVu Sans Mono"),
            (0, 0, "Inconsolata"),
            (0, 0, "LucidaTypewriter"),
            (0, 0, "Lucida Typewriter"),
            (0, 0, "Terminus"),
            (0, 0, "Luxi Mono"),
            (1, 0, "Monospace"),
            (1, 0, "Courier New"),
            (1, 0, "Courier"),
        ]
        # TODO: Add a command-line parameter to change the size.
        # TODO: Maybe make this program flexible, let the window height define
        #       the actual font/circle size.
        fontsize     = 20
        circleheight = 10
        resolution   = (640, 480)

    def load_the_fucking_font(self):
        # The only reason for this function is that pygame can find a font
        # but gets an IOError when trying to load it... So I must manually
        # workaround that.

        # self.font = pygame.font.SysFont(self.default.fontnames, self.default.fontsize)
        for bold, italic, f in self.default.fontnames:
            try:
                filename = pygame.font.match_font(f, bold, italic)
                if filename:
                    self.font = pygame.font.Font(filename, self.default.fontsize)
                    # print("Successfully loaded font: %s (%s)" % (f, filename))
                    break
            except IOError as e:
                # print("Could not load font: %s (%s)" % (f, filename))
                pass
        else:
            self.font = pygame.font.Font(None, self.default.fontsize)
            # print("Loaded the default fallback font: %s" % pygame.font.get_default_font())

    def pre_render_circle_image(self):
        size = self.default.circleheight
        self.circle = pygame.surface.Surface((size,size))
        self.circle.fill(Color("magenta"))
        basecolor  = ( 63,  63,  63, 255)  # RGBA
        lightcolor = (255, 255, 255, 255)
        for i in range(size // 2, -1, -1):
            color = (
                lightcolor[0] + i * (basecolor[0] - lightcolor[0]) // (size // 2),
                lightcolor[1] + i * (basecolor[1] - lightcolor[1]) // (size // 2),
                lightcolor[2] + i * (basecolor[2] - lightcolor[2]) // (size // 2),
                255
            )
            pygame.draw.circle(
                self.circle,
                color,
                (int(size // 4 + i // 2) + 1, int(size // 4 + i // 2) + 1),
                i,
                0
            )
        self.circle.set_colorkey(Color("magenta"), RLEACCEL)

    def init(self):
        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))
        # I'm assuming Font module has been loaded correctly
        self.load_the_fucking_font()
        # self.fontheight = self.font.get_height()
        self.fontheight = self.font.get_linesize()
        self.background = Color("black")
        self.statictext = Color("#FFFFA0")
        self.dynamictext = Color("white")
        self.antialias = 1
        self.pre_render_circle_image()
        # self.clock = pygame.time.Clock()
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            self.quit(1)
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))

        # Find out the best window size
        rec_height = max(
            5 + joy.numaxes + joy.numballs + joy.numhats + (joy.numbuttons + 9) // 10
            for joy in self.joy
        ) * self.fontheight
        rec_width = max(
            [self.font.size("W" * 13)[0]] +
            [self.font.size(joy.name)[0] for joy in self.joy]
        ) * self.joycount
        self.resolution = (rec_width, rec_height)

        self.overValue = 0.8
        self.stick_0_left = "left"
        self.stick_0_right = "right"
        self.stick_0_up = "up"
        self.stick_0_down = "down"
        self.current_vector = [False, False, False, False]
        self.stick_1_left = ""
        self.stick_1_right = ""
        self.stick_1_up = ""
        self.stick_1_down = ""

        self.left_hat = ""
        self.right_hat = ""
        self.up_hat = ""
        self.down_hat = ""

        self.buttonMappingList = ["r", "space", "", "q", "w", "", "", "", "", "", "", "", "", "", "", ""]


    def Axis_Setting(self, type, left, right, up, down):
        if type == 0:
            self.stick_0_left = left
            self.stick_0_right = right
            self.stick_0_up = up
            self.stick_0_down = down
        elif type == 1:
            self.stick_1_left = left
            self.stick_1_right = right
            self.stick_1_up = up
            self.stick_1_down = down


    def Hat_Setting(self, points, key):
        if points == (-1, 0):
            self.left_hat = key
        elif points == (1, 0):
            self.right_hat = key
        elif points == (0, 1):
            self.up_hat = key
        elif points == (0, -1):
            self.down_hat = key
        else:
            print("That point is not matched")
    def Button_Setting(self, n, key):
        if n < 16:
            self.buttonMappingList[n] = key
        else:
            print("Index out of range, The max index is 15")

    def keyBoardPress(self, word):
        if word != "":
            pyautogui.press(word)
    def keyUpdown(self, word, updown):
        if word != "":
            if updown:
                pyautogui.keyDown(word)
            else:
                pyautogui.keyUp(word)
    def Axis_Mapping(self, n, value):
        if n == 0:
            if value < -self.overValue and not self.current_vector[0]:
                self.current_vector[0] = True
                self.keyUpdown(self.stick_0_left, True)
            elif value > self.overValue and not self.current_vector[1]:
                self.current_vector[1] = True
                self.keyUpdown(self.stick_0_right, True)
            else:
                if self.current_vector[0]:
                    self.current_vector[0] = False
                    self.keyUpdown(self.stick_0_left, False)
                if self.current_vector[1]:
                    self.current_vector[1] = False
                    self.keyUpdown(self.stick_0_right, False)
        elif n == 1:
            if value < -self.overValue and not self.current_vector[2]:
                self.current_vector[2] = True
                self.keyUpdown(self.stick_0_up, True)
            elif value > self.overValue and not self.current_vector[3]:
                self.current_vector[3] = True
                self.keyUpdown(self.stick_0_down, True)
            else:
                if self.current_vector[2]:
                    self.current_vector[2] = False
                    self.keyUpdown(self.stick_0_up, False)
                if self.current_vector[3]:
                    self.current_vector[3] = False
                    self.keyUpdown(self.stick_0_down, False)
            #else:
            #    self.keyUpdown(self.stick_0_up, False)
            #    self.keyUpdown(self.stick_0_down, False)
        """
        elif n == 3:
            if value < -self.overValue:
                self.keyUpdown(self.stick_1_left, True)
            elif value > self.overValue:
                self.keyUpdown(self.stick_1_right, True)
            else:
                self.keyUpdown(self.stick_1_left, False)
                self.keyUpdown(self.stick_1_right, False)
        elif n == 4:
            if value < -self.overValue:
                self.keyUpdown(self.stick_1_up, True)
            elif value > self.overValue:
                self.keyUpdown(self.stick_1_down, True)
            else:
                self.keyUpdown(self.stick_1_up, False)
                self.keyUpdown(self.stick_1_down, False)
        """
    def Hat_Mapping(self, points):
        if points[0] == -1:
            self.keyBoardPress(self.left_hat)
        elif points[0] == 1:
            self.keyBoardPress(self.right_hat)
        elif points[1] == -1:
            self.keyBoardPress(self.up_hat)
        elif points[1] == 1:
            self.keyBoardPress(self.down_hat)

    def Button_Mapping(self, n):
        if n < 16:
            self.keyBoardPress(self.buttonMappingList[n])


    def run(self):
        self.screen = pygame.display.set_mode(self.resolution, RESIZABLE)
        pygame.display.set_caption(self.program.nameversion)
        self.circle.convert()
        self.gsp = gspeech.Gspeech()
        while True:
            for i in range(self.joycount):
                self.draw_joy(i)
            pygame.display.flip()
            # self.clock.tick(30)
            for event in [pygame.event.wait(), ] + pygame.event.get():
                # QUIT             none
                # ACTIVEEVENT      gain, state
                # KEYDOWN          unicode, key, mod
                # KEYUP            key, mod
                # MOUSEMOTION      pos, rel, buttons
                # MOUSEBUTTONUP    pos, button
                # MOUSEBUTTONDOWN  pos, button
                # JOYAXISMOTION    joy, axis, value
                # JOYBALLMOTION    joy, ball, rel
                # JOYHATMOTION     joy, hat, value
                # JOYBUTTONUP      joy, button
                # JOYBUTTONDOWN    joy, button
                # VIDEORESIZE      size, w, h
                # VIDEOEXPOSE      none
                # USEREVENT        code
                if event.type == QUIT:
                    self.quit()
                elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
                    self.quit()
                elif event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, RESIZABLE)
                elif event.type == JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    self.Axis_Mapping(event.axis, event.value)
                    print("Joystick mapping : ", event.axis, event.value)
                elif event.type == JOYBALLMOTION:
                    self.joy[event.joy].ball[event.ball] = event.rel
                elif event.type == JOYHATMOTION:
                    self.joy[event.joy].hat[event.hat] = event.value
                    self.Hat_Mapping(event.value)
                    print("Hat mapping      : ", event.value)
                elif event.type == JOYBUTTONUP:
                    self.joy[event.joy].button[event.button] = 0
                    #print("JOYBUTTONUP", event.button)
                elif event.type == JOYBUTTONDOWN:
                    self.joy[event.joy].button[event.button] = 1
                    self.Button_Mapping(event.button)
                    print("Button mapping   : ", event.button)

    def rendertextline(self, text, pos, color, linenumber=0):
        self.screen.blit(
            self.font.render(text, self.antialias, color, self.background),
            (pos[0], pos[1] + linenumber * self.fontheight)
            # I can access top-left coordinates of a Rect by indexes 0 and 1
        )

    def draw_slider(self, value, pos):
        width  = pos[2]
        height = self.default.circleheight
        left   = pos[0]
        top    = pos[1] + (pos[3] - height) // 2
        self.screen.fill(
            (127, 127, 127, 255),
            (left + height // 2, top + height // 2 - 2, width - height, 2)
        )
        self.screen.fill(
            (191, 191, 191, 255),
            (left + height // 2, top + height // 2, width - height, 2)
        )
        self.screen.fill(
            (127, 127, 127, 255),
            (left + height // 2, top + height // 2 - 2, 1, 2)
        )
        self.screen.fill(
            (191, 191, 191, 255),
            (left + height // 2 + width - height - 1, top + height // 2 - 2, 1, 2)
        )
        self.screen.blit(
            self.circle,
            (left + (width - height) * (value + 1) // 2, top)
        )

    def draw_hat(self, value, pos):
        xvalue =  value[0] + 1
        yvalue = -value[1] + 1
        width  = min(pos[2], pos[3])
        height = min(pos[2], pos[3])
        left   = pos[0] + (pos[2] - width ) // 2
        top    = pos[1] + (pos[3] - height) // 2
        self.screen.fill((127, 127, 127, 255), (left, top              , width, 1))
        self.screen.fill((127, 127, 127, 255), (left, top + height // 2, width, 1))
        self.screen.fill((127, 127, 127, 255), (left, top + height  - 1, width, 1))
        self.screen.fill((127, 127, 127, 255), (left             , top, 1, height))
        self.screen.fill((127, 127, 127, 255), (left + width // 2, top, 1, height))
        self.screen.fill((127, 127, 127, 255), (left + width  - 1, top, 1, height))
        offx = xvalue * (width  - self.circle.get_width() ) // 2
        offy = yvalue * (height - self.circle.get_height()) // 2
        # self.screen.fill((255,255,255,255),(left + offx, top + offy) + self.circle.get_size())
        self.screen.blit(self.circle, (left + offx, top + offy))

    def draw_joy(self, joyid):
        joy = self.joy[joyid]
        width = self.screen.get_width() // self.joycount
        height = self.screen.get_height()
        pos = Rect(width * joyid, 0, width, height)
        self.screen.fill(self.background, pos)

        # This is the number of lines required for printing info about this joystick.
        # self.numlines = 5 + joy.numaxes + joy.numballs + joy.numhats + (joy.numbuttons+9)//10

        # Joy name
        # 0 Axes:
        # -0.123456789
        # 0 Trackballs:
        # -0.123,-0.123
        # 0 Hats:
        # -1,-1
        # 00 Buttons:
        # 0123456789

        # Note: the first character is the color of the text.
        text_colors = {
            "D": self.dynamictext,
            "S": self.statictext,
        }
        output_strings = [
            "S%s"             % joy.name,
            "S%d axes:"       % joy.numaxes
        ]+[ "D    %d=% .3f"   % (i, v) for i, v in enumerate(joy.axis) ]+[
            "S%d trackballs:" % joy.numballs
        ]+[ "D%d=% .2f,% .2f" % (i, v[0], v[1]) for i, v in enumerate(joy.ball) ]+[
            "S%d hats:"       % joy.numhats
        ]+[ "D  %d=% d,% d"   % (i, v[0], v[1]) for i, v in enumerate(joy.hat ) ]+[
            "S%d buttons:"    % joy.numbuttons
        ]
        for l in range(joy.numbuttons // 10 + 1):
            s = []
            for i in range(l * 10, min((l + 1) * 10, joy.numbuttons)):
                if joy.button[i]:
                    s.append("%d" % (i % 10))
                else:
                    s.append(" ")
            output_strings.append("D" + "".join(s))

        for i, line in enumerate(output_strings):
            color = text_colors[line[0]]
            self.rendertextline(line[1:], pos, color, linenumber=i)

        tmpwidth = self.font.size("    ")[0]
        for i, v in enumerate(joy.axis):
            self.draw_slider(
                v,
                (
                    pos[0],
                    pos[1] + (2 + i) * self.fontheight,
                    tmpwidth,
                    self.fontheight
                )
            )

        tmpwidth = self.font.size("  ")[0]
        for i, v in enumerate(joy.hat):
            self.draw_hat(
                v,
                (
                    pos[0],
                    pos[1] + (4 + joy.numaxes + joy.numballs + i) * self.fontheight,
                    tmpwidth,
                    self.fontheight
                )
            )
        # self.draw_hat((int(joy.axis[3]),int(joy.axis[4])), (pos[0], pos[1] + (4+joy.numaxes+joy.numballs+0)*self.fontheight, tmpwidth, self.fontheight))

    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)


if __name__ == "__main__":
    program = input_test()
    program.init()
    program.run()  # This function should never return
