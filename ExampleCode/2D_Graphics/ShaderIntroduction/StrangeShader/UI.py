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
            self.ge.setProjectionMatrices(event.size)

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

        # Set the shader mode number.
        if event.key == K_0:
            self.ge.setShaderNum(0)

        if K_1 <= event.key <= K_9:
            self.ge.setShaderNum(event.key - K_1 + 1)

        # Get a screen shot and save to png file.
        if event.key == K_F12:
            path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H-%M-%S.%f.png')
            image = self.ge.getScreenImage()
            image.save(path)

    def processKeyStates(self):
        key = pygame.key.get_pressed()
        if key[K_LCTRL] or key[K_RCTRL]:  # Either control key down.
            # Increase the box width.
            if key[K_LEFT]:
                w = self.ge.box.getWidth()
                w = w + 0.01
                self.ge.box.setWidth(w)

            # Decrease the box width.
            if key[K_RIGHT]:
                w = self.ge.box.getWidth()
                w = w - 0.01
                self.ge.box.setWidth(w)

            # Increase the box height.
            if key[K_UP]:
                h = self.ge.box.getHeight()
                h = h + 0.01
                self.ge.box.setHeight(h)

            # Decrease the box height.
            if key[K_DOWN]:
                h = self.ge.box.getHeight()
                h = h - 0.01
                self.ge.box.setHeight(h)
        else:  # No modifiers
            # Move box up.
            if key[K_UP]:
                cx, cy = self.ge.box.getCenter()
                cy = cy + 0.01
                self.ge.box.setCenter(cx, cy)

            # Move box down.
            if key[K_DOWN]:
                cx, cy = self.ge.box.getCenter()
                cy = cy - 0.01
                self.ge.box.setCenter(cx, cy)

            # Move box left.
            if key[K_LEFT]:
                cx, cy = self.ge.box.getCenter()
                cx = cx - 0.01
                self.ge.box.setCenter(cx, cy)

            # Move box right.
            if key[K_RIGHT]:
                cx, cy = self.ge.box.getCenter()
                cx = cx + 0.01
                self.ge.box.setCenter(cx, cy)