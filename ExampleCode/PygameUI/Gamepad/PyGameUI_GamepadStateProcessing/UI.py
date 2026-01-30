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

    #####################################
    # Gamepad Event Processing
    #####################################

    # In state processing for the gamepads, use the added and removed events to track and store
    # the joysticks in a list of connected devices.  Then in the processing loop go through this list
    # for each gamepad.  This makes processing much faster than reinitializing the joysticks each time.
    def processJoyAdded(self, event):
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        # Initialize joysticks, can be called repeatedly, but must be done for a joystick to
        # create events.
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()

    def processJoyRemoved(self, event):
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    def processGamepadStates(self):
        if pygame.joystick.get_count() == 0:
            return

        for joystick in self.joysticks:
            jid = joystick.get_instance_id()

            axes = joystick.get_numaxes()
            for i in range(axes):
                if i in [0, 1, 3, 4]:
                    axis = joystick.get_axis(i)
                    if abs(axis) > 0.05:
                        print("Joystick ID: ", jid, "   Axis: ", i, "   Value: ", axis)

                        c = self.ge.box.getCenter()

                        if i == 0:
                            self.ge.box.setCenter(axis, c[1])
                        elif i == 1:
                            self.ge.box.setCenter(c[0], -axis)
                        elif i == 3:
                            w = self.ge.box.getWidth()
                            if (axis > 0):
                                self.ge.box.setWidth(w + 0.01)
                            else:
                                self.ge.box.setWidth(w - 0.01)
                        elif i == 4:
                            h = self.ge.box.getHeight()
                            if (axis > 0):
                                self.ge.box.setHeight(h + 0.01)
                            else:
                                self.ge.box.setHeight(h - 0.01)
                else:
                    axis = joystick.get_axis(i)
                    if axis > -0.99:
                        print("Joystick ID: ", jid, "   Axis: ", i, "   Value: ", axis)

            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                if button:
                    print("Joystick ID: ", jid, "   Button Pressed: ", i)

            hats = joystick.get_numhats()
            for i in range(hats):
                hat = joystick.get_hat(i)
                if abs(hat[0]) > 0.01 or abs(hat[1]) > 0.01:
                    print("Joystick ID: ", jid, "   Hat: ", i, "   Value: ", hat)

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
