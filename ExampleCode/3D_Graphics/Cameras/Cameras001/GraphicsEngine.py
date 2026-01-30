#! /usr/bin/env python3
#
# Graphics engine object.
#
# Don Spickler
# 12/30/2021

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm

from Box import *
from Cube import *
from Axes3D import *
from SphericalCamera import *
from YPRCamera import *


class GraphicsEngine():
    mode = GL_FILL
    shaderProgram = -1
    cameranum = 0
    displayobjmode = 1
    showaxes = True

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("VertexShaderBasic3D.glsl", "PassThroughFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the location of the projection matrix in the shader.
        glUseProgram(self.shaderProgram)
        self.projLoc = glGetUniformLocation(self.shaderProgram, "Proj")
        self.viewLoc = glGetUniformLocation(self.shaderProgram, "View")
        self.modelLoc = glGetUniformLocation(self.shaderProgram, "Model")
        self.setProjectionMatrix(pygame.display.get_surface().get_size())

        # Set clear/background color to black and turn on depth testing.
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # Create the cameras.
        self.sphericalcamera = SphericalCamera(30, 60, 45)
        self.yprcamera = YPRCamera()
        self.setViewMatrix()

        # Create and load the objects.
        self.axes = Axes3D()
        self.box = Box()
        self.cube = Cube()

    # Turn on shader, clear screen, draw axes, cubes, or box.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        if self.showaxes:
            axestrans = glm.scale(glm.vec3(10, 10, 10))
            glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(axestrans))
            self.axes.draw()

        model = glm.mat4(1)
        if self.displayobjmode == 1:
            for i in range(-10, 11, 4):
                for j in range(-10, 11, 4):
                    for k in range(-10, 11, 4):
                        model = glm.translate(glm.vec3(i, j, k))
                        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(model))
                        self.cube.draw()
        elif self.displayobjmode == 2:
            glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(model))
            self.cube.draw()
        elif self.displayobjmode == 3:
            glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(model))
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
        projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        glUniformMatrix4fv(self.projLoc, 1, GL_FALSE, glm.value_ptr(projectionMatrix))

    # Set and load the view matrix to the graphics card.
    def setViewMatrix(self):
        if self.cameranum == 0:
            view = self.sphericalcamera.lookAt()
        else:
            view = self.yprcamera.lookAt()

        glUniformMatrix4fv(self.viewLoc, 1, GL_FALSE, glm.value_ptr(view))

    # Toggle between the two cameras.
    def toggleCamera(self):
        if self.cameranum == 0:
            self.cameranum = 1
        else:
            self.cameranum = 0

    # Toggle the drawing of the axes.
    def toggleAxes(self):
        self.showaxes = not self.showaxes

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
