#! /usr/bin/env python3
#
# Point Set object
#
# The PointSet class holds a set of points and colors. It also has
# facilities for loading the data to the graphics card and invoking draw
# commands on the data.
#
# Creates vertex and color arrays, both of size 4*sz to hold packed data of the
# form [x1, y1, z1, w1, x2, y2, z2, w2, ...] for the vertices and
# [r1, g1, b1, a1, r2, g2, b2, a2, ...] for the colors.  Generates the needed
# buffers and call the function to load the data to the graphics card.
#
# Don Spickler
# 12/2/2021

from OpenGL.GL import *
import ctypes
import numpy as np


class PointSet():
    # Constructor
    def __init__(self):
        self.vertices = []
        self.colors = []

        self.VAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)

    def __str__(self):
        return "PointSet: Vertices = {}  Colors = {}".format(self.vertices, self.colors)

    def __repr__(self):
        return "PointSet: {}".format(hex(id(self)))

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1

        # Format data for GLSL
        data = self.vertices + self.colors
        glsldata = np.array(data).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)

        # Remove the current data from the card memory
        glBindVertexArray(self.VAO)

        # Reserve new space and load data.
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, floatsz * len(data), glsldata, GL_DYNAMIC_DRAW)

        # Set the attributes.
        glVertexAttribPointer(vPosition, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(self.vertices)))

        # Enable
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Add in a new vertex (and color).
    def add(self, vertex, color):
        self.vertices = self.vertices + vertex
        self.colors = self.colors + color

    # Reset the vertex and color of the index vertex.
    def set(self, index, vertex, color):
        for i in range(4):
            self.vertices[4 * index + i] = vertex[i]
            self.colors[4 * index + i] = color[i]

    # Clear the vertex and color data.
    def clear(self):
        self.vertices = []
        self.colors = []

    # Draw the vertices.
    def draw(self, mode = GL_TRIANGLES):
        glBindVertexArray(self.VAO)
        glDrawArrays(mode, 0, len(self.vertices) // 4)
