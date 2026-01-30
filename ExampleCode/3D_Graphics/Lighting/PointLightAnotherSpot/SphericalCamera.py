#! /usr/bin/env python3
#
# Spherical Camera object
#
# Creates a spherical camera, that is, one that sits on a sphere of radius r and always
# points to the origin.
#
# Don Spickler
# 12/30/2021

import glm


class SphericalCamera():
    # Constructor
    def __init__(self, R=1, Theta=0, Psi=0):
        self.r = R  # Radius of camera to origin.
        self.theta = Theta  # Theta rotation on the xz plane counter clockwise from positive x axis.
        self.psi = Psi  # Psi rotation from the xz plane to radial.

    # Set the position of the camera.
    def setPosition(self, R=1, Theta=0, Psi=0):
        self.r = R
        self.theta = Theta
        self.psi = Psi

    # Return the lookat matrix for the current camera position, always assuming the view is
    # to the origin and up is <0, 1, 0>.
    def lookAt(self):
        eye = glm.vec3(self.r * glm.cos(glm.radians(self.psi)) * glm.cos(glm.radians(self.theta)),
                       self.r * glm.sin(glm.radians(self.psi)),
                       self.r * glm.cos(glm.radians(self.psi)) * glm.sin(glm.radians(self.theta)))
        center = glm.vec3(0, 0, 0)
        up = glm.vec3(0, 1, 0)

        return glm.lookAt(eye, center, up)

    # Return the current (x, y, z) position of the camera.
    def getPosition(self):
        return glm.vec3(self.r * glm.cos(glm.radians(self.psi)) * glm.cos(glm.radians(self.theta)),
                        self.r * glm.sin(glm.radians(self.psi)),
                        self.r * glm.cos(glm.radians(self.psi)) * glm.sin(glm.radians(self.theta)))

    # Add to the radius.
    def addR(self, num):
        self.r += num
        if self.r < 0.000001:
            self.r = 0.000001

    # Add to the theta angle.
    def addTheta(self, num):
        self.theta += num
        if self.theta > 360:
            self.theta -= 360
        if self.theta < 0:
            self.theta += 360

    # Add to the psi angle.
    def addPsi(self, num):
        self.psi += num
        if self.psi > 90:
            self.psi = 90
        if self.psi < -90:
            self.psi = -90

    # Set the radius of the camera.
    def setR(self, num):
        self.r = num
        if self.r < 0.000001:
            self.r = 0.000001

    # Set the theta angle.
    def setTheta(self, num):
        self.theta = num
        if self.theta > 360:
            self.theta -= 360
        if self.theta < 0:
            self.theta += 360

    # Set the psi angle.
    def setPsi(self, num):
        self.psi = num
        if self.psi > 90:
            self.psi = 90
        if self.psi < -90:
            self.psi = -90

    # Return the current radius.
    def getR(self, num):
        return self.r

    # Return the current theta.
    def getTheta(self, num):
        return self.theta

    # Return the current psi.
    def getPsi(self, num):
        return self.psi
