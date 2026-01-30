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

        # Set the draw style of the box to fill.
        if event.key == K_1:
            self.ge.box.drawStyle = 0

        # Set the draw style of the box to outline indexed.
        if event.key == K_2:
            self.ge.box.drawStyle = 1

        # Set the draw style of the box to outline not indexed.
        if event.key == K_3:
            self.ge.box.drawStyle = 2

        # Make changes to vertex and color data for subdata example.
        if event.key == K_a:
            self.ge.box.changeVertex(2, 1, -1)

        if event.key == K_s:
            self.ge.box.changeVertex(2, 0.5, -0.5)

        if event.key == K_d:
            self.ge.box.changeVertex(1, 1, 0.75)

        if event.key == K_f:
            self.ge.box.changeVertex(1, 0.5, 0.5)

        if event.key == K_q:
            self.ge.box.changeColor(2, 1, 1, 0)

        if event.key == K_w:
            self.ge.box.changeColor(2, 0, 0, 1)

        if event.key == K_e:
            self.ge.box.changeColor(3, 0, 0, 0)

        if event.key == K_r:
            self.ge.box.changeColor(3, 1, 1, 1)

        # Get a screen shot and save to png file.
        if event.key == K_F12:
            path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H-%M-%S.%f.png')
            image = self.ge.getScreenImage()
            image.save(path)
