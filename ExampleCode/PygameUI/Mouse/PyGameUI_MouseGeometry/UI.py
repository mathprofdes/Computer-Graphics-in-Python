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
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

        if event.type == MOUSEMOTION:
            self.processMouseMotion(event)

        if event.type == MOUSEBUTTONDOWN:
            self.processMouseButtonDown(event)

        if event.type == MOUSEWHEEL:
            self.processMouseWheel(event)

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

    def processMouseMotion(self, event):
        buttons = pygame.mouse.get_pressed()

        # If left button down on drag resize the box so the corner is on the mouse
        # and center at last mousedown position.
        if buttons[0]:
            screenPos = self.MouseToScreenConversion(pygame.mouse.get_pos())
            w = 2 * (screenPos[0] - self.lastScreenPos[0])
            h = 2 * (screenPos[1] - self.lastScreenPos[1])
            self.ge.box.setSize(w, h)

    def processMouseButtonDown(self, event):
        # Set the center to the click position.
        screenPos = self.MouseToScreenConversion(pygame.mouse.get_pos())
        self.ge.box.setCenter(screenPos[0], screenPos[1])
        self.lastScreenPos = screenPos

    def processMouseWheel(self, event):
        # Increase or decrease the size of the box by the y value of the wheel movement.
        sz = self.ge.box.getSize()
        self.ge.box.setSize(sz[0] + event.y * 0.01, sz[1] + event.y * 0.01)

    # Gets the viewport dimensions and input mouse position to convert the mouse location
    # from pixel positions to world positions.
    def MouseToScreenConversion(self, mousePosition):
        x, y = mousePosition
        lx, ux, ly, uy = self.ge.getScreenBounds()
        ulx, ulr, w, h = self.ge.getViewport()
        screenPos = [x / w * (ux - lx) + lx, uy - y / h * (uy - ly)]
        return screenPos
