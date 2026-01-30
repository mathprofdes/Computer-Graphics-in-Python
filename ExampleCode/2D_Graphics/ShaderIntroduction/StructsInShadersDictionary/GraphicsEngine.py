#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
#
# Don Spickler
# 12/16/2021

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
            self.AxisProgram = shader.loadShadersFromFile("AspectRatioVert.glsl",
                                                          "PassThroughFrag.glsl")
            self.StructProgram = shader.loadShadersFromFile("AspectRatioAndMoreVert.glsl",
                                                            "PassThroughOrConstantFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Get uniform locations.
        self.Uniforms = {}
        glUseProgram(self.StructProgram)
        self.Uniforms["ConstantColor"] = glGetUniformLocation(self.StructProgram, "info.constantColor")
        self.Uniforms["PassThroughMode"] = glGetUniformLocation(self.StructProgram, "info.pass")
        self.Uniforms["ProjectionMatrix"] = glGetUniformLocation(self.StructProgram, "Mats.Projection")
        self.Uniforms["RotationMatrix"] = glGetUniformLocation(self.StructProgram, "Mats.Rotation")
        self.Uniforms["ScaleMatrix"] = glGetUniformLocation(self.StructProgram, "Mats.Scale")
        self.Uniforms["TranslationMatrix"] = glGetUniformLocation(self.StructProgram, "Mats.Translate")

        glUseProgram(self.AxisProgram)
        self.projAxesLoc = glGetUniformLocation(self.AxisProgram, "Projection")

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)

        # Create and load the objects.
        self.axes = Axes2D()
        self.circle = Polygon(0, 0, 6, 1)
        self.box = Box()

        # Set uniform variables.
        RotationMatrix = glm.rotate(30 * np.pi / 180, glm.vec3(0, 0, 1))
        ScaleMatrix = glm.scale(glm.vec3(0.5, 0.25, 1))
        self.TranslateMatrix = glm.translate(glm.vec3(0.3, -0.15, 0))
        self.TranslateMatrix2 = glm.translate(glm.vec3(-0.1, 0.4, 0))

        glUseProgram(self.StructProgram)
        glUniformMatrix4fv(self.Uniforms["RotationMatrix"], 1, GL_FALSE, glm.value_ptr(RotationMatrix))
        glUniformMatrix4fv(self.Uniforms["ScaleMatrix"], 1, GL_FALSE, glm.value_ptr(ScaleMatrix))
        glUniformMatrix4fv(self.Uniforms["TranslationMatrix"], 1, GL_FALSE, glm.value_ptr(self.TranslateMatrix))

        glUniform4fv(self.Uniforms["ConstantColor"], 1, [0, 1, 0, 1])
        glUniform1i(self.Uniforms["PassThroughMode"], 1)

        self.setProjectionMatrices(pygame.display.get_surface().get_size())

    # Turn on shader, clear screen, draw axes and boxes, swap display buffers.
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        glUseProgram(self.AxisProgram)
        self.axes.draw()

        glUseProgram(self.StructProgram)

        glUniform1i(self.Uniforms["PassThroughMode"], 0)
        glUniformMatrix4fv(self.Uniforms["TranslationMatrix"], 1, GL_FALSE, glm.value_ptr(self.TranslateMatrix))
        self.circle.draw()

        glUniform1i(self.Uniforms["PassThroughMode"], 1)
        glUniformMatrix4fv(self.Uniforms["TranslationMatrix"], 1, GL_FALSE, glm.value_ptr(self.TranslateMatrix2))
        self.box.draw()

        self.printOpenGLErrors()

    def setOutlineMode(self):
        self.circle.setOutline()
        self.box.setOutline()

    def setFillMode(self):
        self.circle.setFill()
        self.box.setFill()

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
        self.setProjectionMatrix(size, self.AxisProgram, self.projAxesLoc)
        self.setProjectionMatrix(size, self.StructProgram, self.Uniforms["ProjectionMatrix"])

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size, prog, location):
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
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(ProjectionMatrix))

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
