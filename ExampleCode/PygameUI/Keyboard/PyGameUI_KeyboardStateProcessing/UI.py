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
        if (event.mod & KMOD_CTRL) and (event.mod & KMOD_SHIFT):  # Control and shift down
            # Reset the box center.
            if event.key == K_f:
                self.ge.box.setCenter(0, 0)

        elif event.mod & KMOD_SHIFT:  # Shift down
            # Reset the box to original position and size.
            if event.key == K_r:
                self.ge.box.setCenter(0, 0)
                self.ge.box.setSize(1, 1)

        elif event.mod & KMOD_ALT:  # Alt down
            # Reset the box to original position and size.
            if event.key == K_r:
                self.ge.box.setCenter(0, 0)
                self.ge.box.setSize(1, 1)

        else:  # No modifiers
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
