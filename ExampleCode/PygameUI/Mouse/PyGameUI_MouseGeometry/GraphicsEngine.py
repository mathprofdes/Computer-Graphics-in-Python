#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
#
# Don Spickler
# 11/20/2021

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from Shader import *
import numpy as np
import ctypes
from PIL import Image
from Box import *

class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL
    shaderProgram = -1
    screenBounds = [-1, 1, -1, 1] # Set to the default here but could be a custom setting [lx, ux, ly, uy].

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("PassThroughVert.glsl", "PassThroughFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Set clear/background color ro black.
        glClearColor(0, 0, 0, 1)

        # Create and load the object.
        self.box = Box()

    # Turn on shader, clear screen, draw triangles, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        self.box.draw()

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    # Get the real world screen bounds.
    def getScreenBounds(self):
        return self.screenBounds

    # Get the current viewport dimensions.
    def getViewport(self):
        return glGetIntegerv(GL_VIEWPORT)

    # Dump screen buffer data to raw pixels and convert to PIL Image object.
    def getScreenImage(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(viewport[0], viewport[1], viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (viewport[2], viewport[3]), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image
