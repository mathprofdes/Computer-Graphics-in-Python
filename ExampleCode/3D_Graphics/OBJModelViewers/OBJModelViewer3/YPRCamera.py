#! /usr/bin/env python3
#
# YPR Camera object
#
# Creates a Yaw-Pitch-Roll camera.
#
# Don Spickler
# 12/30/2021

import glm


class YPRCamera():
    # Constructor
    def __init__(self, P=glm.vec3(0, 0, 0), V=glm.vec3(0, 0, -1), U=glm.vec3(0, 1, 0)):
        self.position = P  # Position of the camera.
        self.view = V  # Viewing Vector direction.
        self.up = U  # Up vector.

    # Sets the camera position.
    def setPosition(self, P=glm.vec3(0, 0, 0)):
        self.position = P

    # Sets the view vector.
    def setView(self, V=glm.vec3(0, 0, -1)):
        self.view = V

    # Sets the up vector.
    def setUp(self, U=glm.vec3(0, 1, 0)):
        self.up = U

    # Sets all three vectors of the camera.
    def setCamera(self, P=glm.vec3(0, 0, 0), V=glm.vec3(0, 0, -1), U=glm.vec3(0, 1, 0)):
        self.position = P
        self.view = V
        self.up = U

    # Return the lookat matrix for the current camera attributes.
    def lookAt(self):
        return glm.lookAt(self.position, self.position + self.view, self.up)

    # Gets the current camera position.
    def getPosition(self):
        return self.position

    # Gets the current view vector.
    def getView(self):
        return self.view

    # Gets the current up vector.
    def getUp(self):
        return self.up

    # Adds to the pitch angle.
    def addPitch(self, num):
        rightvec = glm.cross(self.view, self.up)
        rot = glm.rotate(glm.radians(num), rightvec)
        View4 = glm.vec4(self.view, 1)
        Up4 = glm.vec4(self.up, 1)
        View4 = rot * View4
        Up4 = rot * Up4
        self.up = glm.normalize(glm.vec3(Up4))
        self.view = glm.normalize(glm.vec3(View4))

    # Adds to the yaw angle.
    def addYaw(self, num):
        rot = glm.rotate(glm.radians(num), self.up)
        View4 = glm.vec4(self.view, 1)
        View4 = rot * View4
        self.view = glm.normalize(glm.vec3(View4))

    # Adds to the roll angle.
    def addRoll(self, num):
        rot = glm.rotate(glm.radians(num), self.view)
        Up4 = glm.vec4(self.up, 1)
        Up4 = rot * Up4
        self.up = glm.normalize(glm.vec3(Up4))

    # Moves the camera position forward, and backward.
    def moveForward(self, num):
        mod = glm.length(self.view)
        if mod < 0.000001:
            return
        self.position += self.view / mod * num

    # Moves the camera position right, and left.
    def moveRight(self, num):
        rightvec = glm.cross(self.view, self.up)
        mod = glm.length(rightvec)
        if mod < 0.000001:
            return
        self.position += rightvec / mod * num

    # Moves the camera position up, and down.
    def moveUp(self, num):
        mod = glm.length(self.up)
        if mod < 0.000001:
            return
        self.position += self.up / mod * num
