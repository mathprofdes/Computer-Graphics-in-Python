#! /usr/bin/env python3
#
# Box object
#
# Simple rectangle object with OpenGL data loading and drawing interfaces.  The data that
# is being stored is created in two separate arrays, one for vertices and the other for
# color.  These blocks of data are transferred to a single array buffer on the graphics
# card in two separate locations (that is the data is not intermixed) and hence we can
# set up the reading pointers as having tightly packed data. There is also an index array
# of 6 values {0, 3, 2, 0, 2, 1} that represent the vertices that will be drawn in two
# triangles.  So one triangle will use vertices (0, 3, 2) and the other will use vertices
# (0, 2, 1).  This one includes another indexing array {0, 1, 2, 3} that is used to draw
# an outline of the box.  All we need to do is bind the correct indexing array on the
# draw.
#
# This version also uses the glBufferSubData function to alter small portions of the
# data that is alread on the graphics card.
#
# Don Spickler
# 12/30/2021

from OpenGL.GL import *
import ctypes
import numpy as np


class Box():
    floatsz = ctypes.sizeof(ctypes.c_float)
    uintsz = ctypes.sizeof(ctypes.c_uint)

    # Constructor
    def __init__(self, x=0, y=0, wd=1, ht=1):
        self.cx = x
        self.cy = y
        self.w = wd
        self.h = ht
        self.drawStyle = 0
        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1

        # Vertex and index data for the box, using two triangles.
        self.vertices = [self.cx - self.w / 2, self.cy + self.h / 2,
                         self.cx + self.w / 2, self.cy + self.h / 2,
                         self.cx + self.w / 2, self.cy - self.h / 2,
                         self.cx - self.w / 2, self.cy - self.h / 2
                         ]

        colors = [1, 0, 0,
                  0, 1, 0,
                  0, 0, 1,
                  1, 1, 1]

        indicesFill = [0, 3, 2, 0, 2, 1]
        indicesOutline = [0, 1, 2, 3]

        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(indicesFill).astype(ctypes.c_uint)
        indexoutlinedata = np.array(indicesOutline).astype(ctypes.c_uint)
        vertexdata = np.array(self.vertices).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)

        self.BoxVAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)
        self.BoxEBO = glGenBuffers(2)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Load the indexing arrays on the graphics card. Load the fill index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[0])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.uintsz * len(indicesFill), indexdata, GL_STATIC_DRAW)

        # Load the outline index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.uintsz * len(indicesOutline), indexoutlinedata, GL_STATIC_DRAW)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, self.floatsz * (len(self.vertices) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.floatsz * len(self.vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, self.floatsz * len(self.vertices), self.floatsz * len(colors), colordata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(self.floatsz * len(self.vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Alter data on card for vertex position.
    def changeVertex(self, i, x, y):
        glBindVertexArray(self.BoxVAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)
        vertex = [x, y]
        vertexdata = np.array(vertex).astype(ctypes.c_float)
        glBufferSubData(GL_ARRAY_BUFFER, 2 * self.floatsz * i,
                        self.floatsz * len(vertex), vertexdata)

    # Alter data on card for vertex color.
    def changeColor(self, i, r, g, b):
        glBindVertexArray(self.BoxVAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)
        color = [r, g, b]
        colordata = np.array(color).astype(ctypes.c_float)
        glBufferSubData(GL_ARRAY_BUFFER, self.floatsz * len(self.vertices) + 3 * self.floatsz * i,
                        self.floatsz * len(color), colordata)

    # Draw the box.
    def draw(self):
        glBindVertexArray(self.BoxVAO)
        if self.drawStyle == 0:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[0])
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        elif self.drawStyle == 1:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
            glDrawElements(GL_LINE_LOOP, 4, GL_UNSIGNED_INT, None)
        elif self.drawStyle == 2:
            glDrawArrays(GL_LINE_LOOP, 0, 4)
