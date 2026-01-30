#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
#
# This version includes a simple animation of a spinning square with
# its speed locked to the system clock.  The animation updates at 30
# degree per second.  In general, the rate variable determines the
# number of degrees per second for the animation.
#
# Don Spickler
# 12/9/2021

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm
import time

from Box import *
from Axes2D import *


class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL
    shaderProgram = -1

    # Data items.
    ScreenBounds = [-1, 1, -1, 1]
    rate = 30

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("AspectRatioAndTransformVert.glsl", "PassThroughFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the location of the projection and model matrices in the shader.
        glUseProgram(self.shaderProgram)
        self.projLoc = glGetUniformLocation(self.shaderProgram, "Projection")
        self.modelLoc = glGetUniformLocation(self.shaderProgram, "Model")
        self.setProjectionMatrix(pygame.display.get_surface().get_size())

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)

        # Create and load the objects.
        self.axes = Axes2D()
        self.box = Box()

        # Get the start time of the program.
        self.start_time = time.time()

    # Turn on shader, clear screen, draw axes and boxes, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        # Set the model matrix to the identity and load to graphics card.
        ModelMatrix = glm.mat4(1.0)
        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(ModelMatrix))

        # Draw the axes.
        self.axes.draw()

        # Get time change from the start of the program.
        timeNow = time.time()
        dt = timeNow - self.start_time

        # Animation locked to clock at 30 degrees per second.  If rate is set to 30 above.
        ModelMatrix = glm.rotate(dt * self.rate * np.pi / 180, glm.vec3(0, 0, 1))
        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(ModelMatrix))

        # Draw the box.
        self.box.draw()

        self.printOpenGLErrors()

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size):
        w, h = size

        # if width > height create a matrix to map scene to [-a, a] X [-1, 1]
        # if height > width create a matrix to map scene to [-1, 1] X [-a, a]
        # glm.ortho creates the scaling matrix.
        if w > h:
            aspratio = w / h
            ProjectionMatrix = glm.ortho(-aspratio, aspratio, -1, 1)
            self.ScreenBounds = [-aspratio, aspratio, -1, 1]
        else:
            aspratio = h / w
            ProjectionMatrix = glm.ortho(-1, 1, -aspratio, aspratio)
            self.ScreenBounds = [-1, 1, -aspratio, aspratio]

        # print(ProjectionMatrix)
        # print(self.ScreenBounds)

        # Load Projection Matrix to the projection matrix in the shader.
        glUniformMatrix4fv(self.projLoc, 1, GL_FALSE, glm.value_ptr(ProjectionMatrix))

    # Dump screen buffer data to raw pixels and convert to PIL Image object.
    def getScreenImage(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(viewport[0], viewport[1], viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (viewport[2], viewport[3]), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image

    # Print out any errors in the OpenGL error queue.
    def printOpenGLErrors(self):
        errCode = glGetError()
        while errCode != GL_NO_ERROR:
            errString = gluErrorString(errCode)
            print("OpenGL Error: ", errString, "\n")
            errCode = glGetError()
