#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 11/20/2021

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

    def processEvent(self, event):
        # Process key pressed events.
        if event.type == KEYDOWN:
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

            # Reset the display mode.
            if event.key == K_r:
                pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | RESIZABLE | HWSURFACE)
