#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 12/8/2021

import pygame
from pygame.locals import *
import datetime
from GraphicsEngine import *


class UI():
    # Constructor, links the graphics engine to the user interface for easy
    # one-way communication from the UI to the GE.
    def __init__(self, GE):
        self.ge = GE
        self.lastScreenPos = [0, 0]
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    # Process events
    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

        if event.type == pygame.VIDEORESIZE:
            self.ge.setProjectionMatrices(event.size)

        if event.type == MOUSEMOTION:
            self.processMouseMotion(event)

        if event.type == MOUSEBUTTONDOWN:
            self.processMouseButtonDown(event)

        if event.type == MOUSEWHEEL:
            self.processMouseWheel(event)

    # Process key down.
    def processKeydown(self, event):
        # Set the rendering mode to fill.
        if event.key == K_F1:
            self.ge.setFill()

        # Set the rendering mode to line.
        if event.key == K_F2:
            self.ge.setLine()

        # Set the rendering mode to point.
        if event.key == K_F3:
            self.ge.setPoint()

        # Toggle double precision.
        if event.key == K_d:
            self.ge.toggleDoublePre()

        # Toggle smooth rendering.
        if event.key == K_s:
            self.ge.toggleSmooth()

        # Reset fractal to its original attributes.
        if event.key == K_F8:
            self.ge.resetFractal()

        # Get and print fractal information to the console.
        if event.key == K_F11:
            print(self.ge.getFractalInformation())

        # Get a screen shot and save to png file.
        if event.key == K_F12:
            path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H-%M-%S.%f')
            image = self.ge.getScreenImage()
            image.save(path + ".png")
            infofile = open(path + "_info.txt", "w")
            infofile.write(self.ge.getFractalInformation())
            infofile.close()

    # Process key states.
    def processKeyStates(self):
        key = pygame.key.get_pressed()
        if key[K_z]:
            if key[K_UP]:
                self.ge.multScaleFactor(0.99)
            if key[K_DOWN]:
                self.ge.multScaleFactor(1.01)
        elif key[K_i]:
            if key[K_UP]:
                self.ge.addToMaxIter(1)
            if key[K_DOWN]:
                self.ge.addToMaxIter(-1)
            if key[K_1]:
                self.ge.setMaxIter(50)
            if key[K_2]:
                self.ge.setMaxIter(100)
            if key[K_3]:
                self.ge.setMaxIter(250)
            if key[K_4]:
                self.ge.setMaxIter(500)
            if key[K_5]:
                self.ge.setMaxIter(1000)
            if key[K_6]:
                self.ge.setMaxIter(2500)
            if key[K_7]:
                self.ge.setMaxIter(5000)
            if key[K_8]:
                self.ge.setMaxIter(7500)
            if key[K_9]:
                self.ge.setMaxIter(10000)
            if key[K_0]:
                self.ge.setMaxIter(20000)

        elif key[K_u]:
            if key[K_UP]:
                self.ge.addToMaxIter(10)
            if key[K_DOWN]:
                self.ge.addToMaxIter(-10)
        elif key[K_y]:
            if key[K_UP]:
                self.ge.addToMaxIter(100)
            if key[K_DOWN]:
                self.ge.addToMaxIter(-100)
        elif key[K_m]:
            if key[K_UP]:
                self.ge.addToBorderFactor(-0.001)
            if key[K_DOWN]:
                self.ge.addToBorderFactor(0.001)
            if key[K_1]:
                self.ge.setBorderFactor(0.1)
            if key[K_2]:
                self.ge.setBorderFactor(0.2)
            if key[K_3]:
                self.ge.setBorderFactor(0.3)
            if key[K_4]:
                self.ge.setBorderFactor(0.4)
            if key[K_5]:
                self.ge.setBorderFactor(0.5)
            if key[K_6]:
                self.ge.setBorderFactor(0.6)
            if key[K_7]:
                self.ge.setBorderFactor(0.7)
            if key[K_8]:
                self.ge.setBorderFactor(0.8)
            if key[K_9]:
                self.ge.setBorderFactor(0.9)
            if key[K_0]:
                self.ge.setBorderFactor(0)

        elif key[K_w]:
            if key[K_UP]:
                self.ge.multIterationScale(1.01)
            if key[K_DOWN]:
                self.ge.multIterationScale(0.99)
            if key[K_1]:
                self.ge.setIterationScale(0.1)
            if key[K_2]:
                self.ge.setIterationScale(0.25)
            if key[K_3]:
                self.ge.setIterationScale(0.5)
            if key[K_4]:
                self.ge.setIterationScale(0.75)
            if key[K_5]:
                self.ge.setIterationScale(1)
            if key[K_6]:
                self.ge.setIterationScale(2.5)
            if key[K_7]:
                self.ge.setIterationScale(5)
            if key[K_8]:
                self.ge.setIterationScale(10)
            if key[K_9]:
                self.ge.setIterationScale(25)
            if key[K_0]:
                self.ge.setIterationScale(50)

        elif key[K_o]:
            if key[K_UP]:
                self.ge.addIterationOffset(0.1)
            if key[K_DOWN]:
                self.ge.addIterationOffset(-0.1)
            if key[K_1]:
                self.ge.setIterationOffset(10)
            if key[K_2]:
                self.ge.setIterationOffset(20)
            if key[K_3]:
                self.ge.setIterationOffset(30)
            if key[K_4]:
                self.ge.setIterationOffset(40)
            if key[K_5]:
                self.ge.setIterationOffset(50)
            if key[K_6]:
                self.ge.setIterationOffset(60)
            if key[K_7]:
                self.ge.setIterationOffset(70)
            if key[K_8]:
                self.ge.setIterationOffset(80)
            if key[K_9]:
                self.ge.setIterationOffset(90)
            if key[K_0]:
                self.ge.setIterationOffset(0)

        elif key[K_t]:
            if key[K_1]:
                self.ge.setColorScheme(1)
            if key[K_2]:
                self.ge.setColorScheme(2)
            if key[K_3]:
                self.ge.setColorScheme(3)
            if key[K_4]:
                self.ge.setColorScheme(4)
            if key[K_5]:
                self.ge.setColorScheme(5)
            if key[K_6]:
                self.ge.setColorScheme(6)
            if key[K_7]:
                self.ge.setColorScheme(7)
            if key[K_8]:
                self.ge.setColorScheme(8)
            if key[K_9]:
                self.ge.setColorScheme(9)
            if key[K_0]:
                self.ge.setColorScheme(10)

        elif key[K_n]:
            if key[K_UP]:
                self.ge.multBailoutRadius(1.01)
            if key[K_DOWN]:
                self.ge.multBailoutRadius(0.99)
        elif key[K_e]:
            if key[K_1]:
                self.ge.setExponent(2)
            if key[K_2]:
                self.ge.setExponent(2)
            if key[K_3]:
                self.ge.setExponent(3)
            if key[K_4]:
                self.ge.setExponent(4)
            if key[K_5]:
                self.ge.setExponent(5)
            if key[K_6]:
                self.ge.setExponent(6)
            if key[K_7]:
                self.ge.setExponent(7)
            if key[K_8]:
                self.ge.setExponent(8)
            if key[K_9]:
                self.ge.setExponent(9)
            if key[K_0]:
                self.ge.setExponent(10)
        elif key[K_c]:
            col = self.ge.getSolidColor()
            if key[K_r]:
                if key[K_UP]:
                    col.r += 0.005
                if key[K_DOWN]:
                    col.r -= 0.005
            if key[K_g]:
                if key[K_UP]:
                    col.g += 0.005
                if key[K_DOWN]:
                    col.g -= 0.005
            if key[K_b]:
                if key[K_UP]:
                    col.b += 0.005
                if key[K_DOWN]:
                    col.b -= 0.005

            if col.r > 1:
                col.r = 1

            if col.g > 1:
                col.g = 1

            if col.b > 1:
                col.b = 1

            if col.r < 0:
                col.r = 0

            if col.g < 0:
                col.g = 0

            if col.b < 0:
                col.b = 0

            col.a = 1
            self.ge.setSolidColor(col)

        else:  # No modifiers
            if key[K_UP]:
                self.ge.addToCenter(0, 0.01)

            if key[K_DOWN]:
                self.ge.addToCenter(0, -0.01)

            if key[K_LEFT]:
                self.ge.addToCenter(-0.01, 0)

            if key[K_RIGHT]:
                self.ge.addToCenter(0.01, 0)

    # Process mouse move events.
    def processMouseMotion(self, event):
        buttons = pygame.mouse.get_pressed()

        if buttons[0]:
            screenPos = self.MouseToScreenConversion(pygame.mouse.get_pos())
            screenMove = [screenPos[0] - self.lastScreenPos[0],
                          screenPos[1] - self.lastScreenPos[1]]

            self.ge.addToCenter(screenMove[0], screenMove[1])
            self.lastScreenPos = screenPos

    # Process mouse button events.
    def processMouseButtonDown(self, event):
        key = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()

        # Set the center to the click position.
        screenPos = self.MouseToScreenConversion(pygame.mouse.get_pos())

        if buttons[2]:
            self.ge.setCenterBySC(screenPos[0], screenPos[1])

        self.lastScreenPos = screenPos

    # Process mouse wheel events.
    def processMouseWheel(self, event):
        key = pygame.key.get_pressed()
        #print(event)
        if key[K_LCTRL] or key[K_RCTRL]:  # Either control key down.
            self.ge.multScaleFactor(1 + event.y / 10)
        else:
            self.ge.multScaleFactor(1 + event.y / 100)

    # Gets the viewport dimensions and input mouse position to convert the mouse location
    # from pixel positions to world positions.
    def MouseToScreenConversion(self, mousePosition):
        x, y = mousePosition
        lx, ux, ly, uy = self.ge.getScreenBounds()
        ulx, ulr, w, h = self.ge.getViewport()
        screenPos = [x / w * (ux - lx) + lx, uy - y / h * (uy - ly)]
        return screenPos

