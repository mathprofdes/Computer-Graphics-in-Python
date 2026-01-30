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
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)
        elif event.type == pygame.VIDEORESIZE:
            self.ge.setProjectionMatrix(event.size)

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
            path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H-%M-%S.%f.png')
            image = self.ge.getScreenImage()
            image.save(path)
