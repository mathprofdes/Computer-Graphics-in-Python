#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 11/21/2021

import pygame
from pygame.locals import *
import datetime
from GraphicsEngine import *

class UI():
    # Constructor, links the graphics engine to the user interface for easy
    # one-way communication from the UI to the GE.
    def __init__(self, GE):
        self.ge = GE
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

        if event.type == KEYUP:
            self.processKeyup(event)

        if event.type == MOUSEMOTION:
            self.processMouseMotion(event)

        if event.type == MOUSEBUTTONDOWN:
            self.processMouseButtonDown(event)

        if event.type == MOUSEBUTTONUP:
            self.processMouseButtonUp(event)

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

    def processKeyup(self, event):
        # Reset the display mode.
        if event.key == K_r:
            pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | RESIZABLE | HWSURFACE)

    def processMouseMotion(self, event):
        print(event)

    def processMouseButtonDown(self, event):
        print(event)

    def processMouseButtonUp(self, event):
        print(event)

    def processMouseWheel(self, event):
        print(event)
