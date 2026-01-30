#! /usr/bin/env python3
#
# Axes3D object
#
# X, Y, and Z axes for development.  The x-axis is red, the y-axis is green,
# and the z-axis is blue.
# The positive axis is in bright color and the negative axis is dull. The
# length of each axis is 2 centered at the origin. That is, [-1, 1] in all
# three directions.
#
# Don Spickler
# 12/30/2021

from OpenGL.GL import *
import ctypes
import numpy as np


class Axes3D():
    # Constructor
    def __init__(self):
        self.LoadDataToGraphicsCard()

    # Load data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1

        # Vertex data for the axes.
        vertices = [0, 0, 0,
                    -1, 0, 0,
                    0, 0, 0,
                    1, 0, 0,
                    0, 0, 0,
                    0, -1, 0,
                    0, 0, 0,
                    0, 1, 0,
                    0, 0, 0,
                    0, 0, -1,
                    0, 0, 0,
                    0, 0, 1]

        # Color data for the axes.
        colors = [0.5, 0, 0,
                  0.5, 0, 0,
                  1, 0, 0,
                  1, 0, 0,
                  0, 0.5, 0,
                  0, 0.5, 0,
                  0, 1, 0,
                  0, 1, 0,
                  0, 0, 0.5,
                  0, 0, 0.5,
                  0, 0, 1,
                  0, 0, 1]

        # Convert data to GLSL form and get machine sizes of data types.
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)

        self.BoxVAO = glGenVertexArrays(1)
        ArrayBuffer = glGenBuffers(1)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, ArrayBuffer)

        # Allocate space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(colors), colordata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Draw the axes.
    def draw(self):
        glBindVertexArray(self.BoxVAO)
        glDrawArrays(GL_LINES, 0, 12)
