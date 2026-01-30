#! /usr/bin/env python3
#
# User interface event processing.
#
# Don Spickler
# 11/26/2021

import pygame
from pygame.locals import *
import datetime
from GraphicsEngine import *

class UI():
    # Constructor, links the graphics engine to the user interface for easy
    # one-way communication from the UI to the GE.
    def __init__(self, GE):
        self.ge = GE

        pygame.mixer.music.load('Bach.wav')
        pygame.mixer.music.play(-1)  # Loop indefinitely.

        # Load other sounds.
        self.ding_sound = pygame.mixer.Sound("Ding.wav")

        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

    def processKeydown(self, event):
        # Play Ding.wav
        if event.key == pygame.K_p:
            self.ding_sound.play()

        # Pause playback.
        if event.key == K_F5:
            pygame.mixer.music.pause()

        # Resume playback.
        if event.key == K_F6:
            pygame.mixer.music.unpause()

        # Stop playback.
        if event.key == K_F7:
            pygame.mixer.music.stop()

        # Start playback.
        if event.key == K_F8:
            pygame.mixer.music.play(-1)

        # Load and play Bach
        if event.key == K_F9:
            pygame.mixer.music.load('Bach.wav')
            pygame.mixer.music.play(-1)  # Loop indefinitely.

        # Load and play REM
        if event.key == K_F10:
            pygame.mixer.music.load('REM.wav')
            pygame.mixer.music.play(-1)  # Loop indefinitely.

        # Move box up.
        if event.key == pygame.K_UP:
            cx, cy = self.ge.box.getCenter()
            cy = cy + 0.01
            self.ge.box.setCenter(cx, cy)

        # Move box down.
        if event.key == pygame.K_DOWN:
            cx, cy = self.ge.box.getCenter()
            cy = cy - 0.01
            self.ge.box.setCenter(cx, cy)

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
            path = datetime.datetime.now().strftime('ScreenShot_%Y-%m-%d_%H-%M-%S.%f.png')
            image = self.ge.getScreenImage()
            image.save(path)

        # Reset the box to original position and size.
        if event.key == K_r:
            self.ge.box.setCenter(0, 0)
            self.ge.box.setSize(1, 1)



