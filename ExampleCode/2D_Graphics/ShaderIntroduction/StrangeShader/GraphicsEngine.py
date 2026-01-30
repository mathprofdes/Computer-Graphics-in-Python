#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
#
# Don Spickler
# 12/17/2021

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm
import random
import time

from Box import *
from Axes2D import *
from Polygon import *


class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL

    ScreenBounds = [-1, 1, -1, 1]

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("AspectRatioVert.glsl", "StrangeFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        self.setProjectionMatrices(pygame.display.get_surface().get_size())

        glUseProgram(self.shaderProgram)
        self.shadernumLoc = glGetUniformLocation(self.shaderProgram, "shadernum")
        self.timeLoc = glGetUniformLocation(self.shaderProgram, "time")

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)

        # Create and load the objects.
        self.circle = Polygon(-0.5, -0.5, 50, 0.25)
        self.box = Box()
        self.starttime = time.time()

    # Turn on shader, clear screen, draw axes and boxes, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        now = time.time()
        runtime = now - self.starttime
        glUniform1f(self.timeLoc, runtime)

        self.box.draw()
        self.circle.draw()

        self.printOpenGLErrors()


    def setShaderNum(self, num):
        glUseProgram(self.shaderProgram)
        glUniform1i(self.shadernumLoc, num)

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    def setProjectionMatrices(self, size):
        self.setProjectionMatrix(size, self.shaderProgram, "Projection")

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size, prog, name):
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
        glUseProgram(prog)
        projLoc = glGetUniformLocation(prog, name)
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(ProjectionMatrix))

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
