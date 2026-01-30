#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 11/25/2021

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
        self.leftMouseButtonDown = False

        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

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

        # Get a screen shot and save to png file.
        if event.key == K_F12:
            path = datetime.datetime.now().strftime('ScreenShot_%Y_%m_%d_%H-%M-%S.%f.png')
            image = self.ge.getScreenImage()
            image.save(path)

        # Reset box to center and dimensions to 1 X 1.
        if event.key == K_r:
            self.ge.box.setSize(1, 1)
            self.ge.box.setCenter(0, 0)

    # Gets the viewport dimensions and input mouse position to convert the mouse location
    # from pixel positions to world positions.
    def MouseToScreenConversion(self, mousePosition):
        x, y = mousePosition
        lx, ux, ly, uy = self.ge.getScreenBounds()
        ulx, ulr, w, h = self.ge.getViewport()
        screenPos = [x / w * (ux - lx) + lx, uy - y / h * (uy - ly)]
        return screenPos

    def processMouse(self):
        # Get the mouse states, buttons, position, and relative movement.
        buttons = pygame.mouse.get_pressed(5)
        pos = pygame.mouse.get_pos()
        rel = pygame.mouse.get_rel()

        # Boolean for the mouse moved.
        moved = rel[0] != 0 or rel[1] != 0

        # Click of left button.
        if buttons[0] and (not self.leftMouseButtonDown):
            self.leftMouseButtonDown = True
            screenPos = self.MouseToScreenConversion(pos)
            self.ge.box.setCenter(screenPos[0], screenPos[1])
            self.lastScreenPos = screenPos

        # Mouse up of left button.
        if not buttons[0]:
            self.leftMouseButtonDown = False

        # Click and drag of left button.
        if self.leftMouseButtonDown and moved:
            screenPos = self.MouseToScreenConversion(pygame.mouse.get_pos())
            w = 2 * (screenPos[0] - self.lastScreenPos[0])
            h = 2 * (screenPos[1] - self.lastScreenPos[1])
            self.ge.box.setSize(w, h)
