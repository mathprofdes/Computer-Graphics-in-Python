#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 12/2/2021

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

    def processKeydown(self, event):
        # Draw mode selection
        if event.key == K_1:
            self.ge.plotstyle = 1

        if event.key == K_2:
            self.ge.plotstyle = 2

        if event.key == K_3:
            self.ge.plotstyle = 3

        if event.key == K_4:
            self.ge.plotstyle = 4

        if event.key == K_5:
            self.ge.plotstyle = 5

        if event.key == K_6:
            self.ge.plotstyle = 6

        if event.key == K_7:
            self.ge.plotstyle = 7

        # Point set selection
        if event.key == K_F7:
            self.ge.drawset = 1

        if event.key == K_F8:
            self.ge.drawset = 2

        # Print information on point and line sizes.
        if event.key == K_p:
            self.ge.printInfo()

        # Change point size.
        if event.key == K_RIGHT:
            self.ge.adjustPointSize(1)

        if event.key == K_LEFT:
            self.ge.adjustPointSize(-1)

        # Change line width.
        if event.key == K_UP:
            self.ge.adjustLineWidth(1)

        if event.key == K_DOWN:
            self.ge.adjustLineWidth(-1)

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
