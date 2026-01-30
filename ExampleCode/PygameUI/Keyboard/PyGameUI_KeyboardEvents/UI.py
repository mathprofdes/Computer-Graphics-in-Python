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

        if event.type == KEYUP:
            self.processKeyup(event)

    def processKeydown(self, event):
        # Move box up.
        if event.key == pygame.K_UP:
            self.ge.box.cy = self.ge.box.cy + 0.01
            self.ge.box.LoadDataToGraphicsCard()
            # You could also use a more encapsulated approach with gets and sets.
            # cx, cy = self.ge.box.getCenter()
            # cy = cy + 0.01
            # self.ge.box.setCenter(cx, cy)

        # Move box down.
        if event.key == pygame.K_DOWN:
            self.ge.box.cy = self.ge.box.cy - 0.01
            self.ge.box.LoadDataToGraphicsCard()
            # You could also use a more encapsulated approach with gets and sets.
            # cx, cy = self.ge.box.getCenter()
            # cy = cy - 0.01
            # self.ge.box.setCenter(cx, cy)

        # Move box left.
        if event.key == pygame.K_LEFT:
            cx, cy = self.ge.box.getCenter()
            cx = cx - 0.01
            self.ge.box.setCenter(cx, cy)

        # Move box right.
        if event.key == pygame.K_RIGHT:
            cx, cy = self.ge.box.getCenter()
            cx = cx + 0.01
            self.ge.box.setCenter(cx, cy)

        # Increase the box width.
        if event.key == pygame.K_a:
            w = self.ge.box.getWidth()
            w = w + 0.01
            self.ge.box.setWidth(w)

        # Decrease the box width.
        if event.key == pygame.K_d:
            w = self.ge.box.getWidth()
            w = w - 0.01
            self.ge.box.setWidth(w)

        # Increase the box height.
        if event.key == pygame.K_w:
            h = self.ge.box.getHeight()
            h = h + 0.01
            self.ge.box.setHeight(h)

        # Decrease the box height.
        if event.key == pygame.K_s:
            h = self.ge.box.getHeight()
            h = h - 0.01
            self.ge.box.setHeight(h)

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
        # Reset the box to original position and size.
        if event.key == K_r:
            self.ge.box.setCenter(0, 0)
            self.ge.box.setSize(1, 1)


