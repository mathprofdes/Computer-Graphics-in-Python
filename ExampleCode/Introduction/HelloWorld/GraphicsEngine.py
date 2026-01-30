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

# Data for the two triangles to be displayed. Format is (r, g, b, x, y)
# for each vertex.
data = [[1.00, 0.00, 0.00, -0.90, -0.90],  # Triangle 1 (r, g, b, x, y)
     [0.00, 1.00, 0.00, 0.85, -0.90],
     [0.00, 0.00, 1.00, -0.90, 0.85],
     [0.04, 0.04, 0.04, 0.90, -0.85],  # Triangle 2
     [0.40, 0.40, 0.40, 0.90, 0.90],
     [1.00, 1.00, 1.00, -0.85, 0.90]]

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

        # Set clear/background color ro black.
        glClearColor(0, 0, 0, 1)

        # Create the Vertex Array Object and bind.
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Create the Array Buffer and bind.
        self.Buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

        # Load the data to the graphics card using numpy to set the data type.
        gpudata = np.array(data).astype(ctypes.c_float)
        glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

        # Set the data attributes so the card knows how to interpret the data.
        floatsize = ctypes.sizeof(ctypes.c_float)
        glVertexAttribPointer(self.vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
        glVertexAttribPointer(self.vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

        # Enable the arrays and set the "positions" for the shaders.
        glEnableVertexAttribArray(self.vPosition)
        glEnableVertexAttribArray(self.vColor)

    # Turn on shader, clear screen, draw triangles, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        glDrawArrays(GL_TRIANGLES, 0, len(data))

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
