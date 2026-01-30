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
        pygame.joystick.init()
        # Set the initial repeat rate time and repeat speed.
        pygame.key.set_repeat(500, 25)

    def processEvents(self, event):
        if event.type == KEYDOWN:
            self.processKeydown(event)

        if event.type == JOYDEVICEADDED:
            self.processJoyAdded(event)

        if event.type == JOYDEVICEREMOVED:
            self.processJoyRemoved(event)

        if event.type == JOYBUTTONDOWN:
            self.processJoyButtondown(event)

        if event.type == JOYBUTTONUP:
            self.processJoyButtonup(event)

        if event.type == JOYAXISMOTION:
            self.processJoyAxes(event)

        if event.type == JOYHATMOTION:
            self.processJoyHat(event)

    #####################################
    # Gamepad Event Processing
    #####################################

    def processJoyAdded(self, event):
        # Adding a gamepad to the system.
        print("Joy Added: ", end='')
        print(event)
        print('Number of joysticks: ', pygame.joystick.get_count())

        # Get list of joysticks.
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        print(self.joysticks)

        # Initialize joysticks, can be called repeatedly, but must be done for a joystick to
        # create events.
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()

        # If you need the id of the new joystick take the one at the end of the list.
        newID = self.joysticks[len(self.joysticks) - 1].get_instance_id()
        print('Number of joysticks: ', pygame.joystick.get_count(), "   New ID: ", newID)

    def processJoyRemoved(self, event):
        # Removing a gamepad from the system.
        print("Joy Removed: ", end='')
        print(event)
        print('Number of joysticks: ', pygame.joystick.get_count(), "   Removed ID: ", event.instance_id)

    def processJoyButtondown(self, event):
        # Button is pressed.
        print("Joy Button Down: ", end='')
        print(event)
        print("Joystick ID: ", event.instance_id, "  Button: ", event.button)

    def processJoyButtonup(self, event):
        # Button is released.
        print("Joy Button Up: ", end='')
        print(event)
        print("Joystick ID: ", event.instance_id, "  Button: ", event.button)

    def processJoyHat(self, event):
        # Hat changes.
        print("Joy Hat: ", end='')
        print(event)
        print("Joystick ID: ", event.instance_id, "  Hat: ", event.hat, "  Value: ", event.value)

    def processJoyAxes(self, event):
        # Joystick axes change.
        print("Joy Axes: ", end='')
        print(event)
        print("Joystick ID: ", event.instance_id, "  Axis: ", event.axis, "  Value: ", event.value)

    #####################################
    # Keyboard Event Processing
    #####################################

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
