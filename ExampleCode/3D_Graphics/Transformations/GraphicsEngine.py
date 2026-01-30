#! /usr/bin/env python3
#
# Graphics engine object.
#
# Don Spickler
# 1/3/2022

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
    projectionMatrix = glm.mat4(1)
    viewMatrix = glm.mat4(1)

    # For rotation animation if used in update function.
    a = 0

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
        self.projviewLoc = glGetUniformLocation(self.shaderProgram, "ProjView")
        self.modelLoc = glGetUniformLocation(self.shaderProgram, "Model")
        self.setProjectionMatrix(pygame.display.get_surface().get_size())

        # Set clear/background color to black and turn on depth testing.
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # Create the cameras.
        self.sphericalcamera = SphericalCamera(10, 60, 25)
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

        # Draw object with no model transformation.
        model = glm.mat4(1.0)
        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(model))

        if self.displayobjmode == 1:
            self.cube.draw()
        elif self.displayobjmode == 2:
            self.box.draw()

        # Create transformation matrix.
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(3, 0, 0))
        model = glm.rotate(model, glm.radians(20), glm.vec3(0, 1, 0))
        model = glm.scale(model, glm.vec3(3, 1, 1))

        # modelTranslate = glm.translate(glm.vec3(3, 0, 0))
        # modelRotate = glm.rotate(glm.radians(20), glm.vec3(0, 1, 0))
        # modelScale = glm.scale(glm.vec3(3, 1, 1))
        # model = modelTranslate * modelRotate * modelScale

        # self.a += 1
        # modelTranslate = glm.translate(glm.vec3(3, 0, 0))
        # modelRotate = glm.rotate(glm.radians(self.a), glm.vec3(0, 1, 0))
        # modelScale = glm.scale(glm.vec3(3, 1, 1))
        # model = modelTranslate * modelRotate * modelScale

        # Load transformation matrix to shader.
        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(model))

        # Draw object with model transformation.
        if self.displayobjmode == 1:
            self.cube.draw()
        elif self.displayobjmode == 2:
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
        self.projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        PV = self.projectionMatrix * self.viewMatrix
        glUniformMatrix4fv(self.projviewLoc, 1, GL_FALSE, glm.value_ptr(PV))

    # Set and load the view matrix to the graphics card.
    def setViewMatrix(self):
        if self.cameranum == 0:
            self.viewMatrix = self.sphericalcamera.lookAt()
        else:
            self.viewMatrix = self.yprcamera.lookAt()

        PV = self.projectionMatrix * self.viewMatrix
        glUniformMatrix4fv(self.projviewLoc, 1, GL_FALSE, glm.value_ptr(PV))

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
