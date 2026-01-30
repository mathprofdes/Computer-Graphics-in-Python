#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
# This will load in 5 box structures, each using a different data storage
# layout.
#
# Don Spickler
# 12/06/2021

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from Shader import *
import numpy as np
import ctypes
from PIL import Image

from Box_PackedIndexedCombined import *
from Box_PackedIndexed import *
from Box_Packed import *
from Box_Interlaced import *
from Box_InterlacedIndexed import *

class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL
    shaderProgram = -1

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

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)

        # Create and load the object.
        self.boxPIC = Box_PackedIndexedCombined(-0.5, 0.5, 0.25, 0.25)
        self.boxPI = Box_PackedIndexed(0.5, 0.5, 0.25, 0.35)
        self.boxP = Box_Packed(-0.5, -0.5, 0.3, 0.15)
        self.boxI = Box_Interlaced(0.5, -0.5, 0.1, 0.5)
        self.boxII = Box_InterlacedIndexed(0, 0, 0.3, 0.2)

    # Turn on shader, clear screen, draw triangles, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        self.boxPIC.draw()
        self.boxPI.draw()
        self.boxP.draw()
        self.boxI.draw()
        self.boxII.draw()

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    # Dump screen buffer data to raw pixels and convert to PIL Image object.
    def getScreenImage(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(viewport[0], viewport[1], viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (viewport[2], viewport[3]), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image
