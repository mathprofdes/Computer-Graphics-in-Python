#! /usr/bin/env python3
#
# Box object
#
# Simple rectangle object with OpenGL data loading and drawing interfaces.  The data that
# is being stored is created in two separate arrays, one for vertices and the other for
# color.  These blocks of data are transferred to a single array buffer on the graphics
# card in two separate locations (that is the data is not intermixed) and hence we can
# set up the reading pointers as having tightly packed data. There are also two index arrays,
# # one for filled triangles and the other for an outline of the box.
#
# Don Spickler
# 12/16/2021

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
        self.fill = True
        self.colors = [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1]

        self.BoxVAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)
        self.BoxEBO = glGenBuffers(1)
        self.OutlineEBO = glGenBuffers(1)

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

        indices = [0, 3, 2, 0, 2, 1]
        outlineindices = [0, 1, 2, 3]

        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(indices).astype(ctypes.c_uint)
        outlineindexdata = np.array(outlineindices).astype(ctypes.c_uint)
        vertexdata = np.array(self.vertices).astype(ctypes.c_float)
        colordata = np.array(self.colors).astype(ctypes.c_float)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Load the indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.uintsz * len(indices), indexdata, GL_STATIC_DRAW)

        # Load the outline indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.OutlineEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.uintsz * len(outlineindices), outlineindexdata, GL_STATIC_DRAW)

        # Bindm(turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate  space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, self.floatsz * (len(self.vertices) + len(self.colors)), None, GL_DYNAMIC_DRAW)

        # Load the vertex data.
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.floatsz * len(self.vertices), vertexdata)

        # Load the color data.
        glBufferSubData(GL_ARRAY_BUFFER, self.floatsz * len(self.vertices), self.floatsz * len(self.colors), colordata)

        # Setup vertex data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        # Setup color data position information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(self.floatsz * len(self.vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Set the center of the box and reload the data.
    def setCenter(self, x, y):
        self.cx = x
        self.cy = y
        self.LoadDataToGraphicsCard()

    # Return the center of the box.
    def getCenter(self):
        return self.cx, self.cy

    # Set the width of the box and reload the data.
    def setWidth(self, wd):
        self.w = wd
        self.LoadDataToGraphicsCard()

    # Return the width of the box.
    def getWidth(self):
        return self.w

    # Set the height of the box and reload the data.
    def setHeight(self, ht):
        self.h = ht
        self.LoadDataToGraphicsCard()

    # Return the height of the box.
    def getHeight(self):
        return self.h

    # Return the size [width, height] of the box.
    def getSize(self):
        return self.w, self.h

    # Set the size (width x height) of the box and reload the data.
    def setSize(self, wd, ht):
        self.w = wd
        self.h = ht
        self.LoadDataToGraphicsCard()

    # Turn on fill mode.
    def setFill(self):
        self.fill = True

    # Turn on outline mode.
    def setOutline(self):
        self.fill = False

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
        if self.fill:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        else:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.OutlineEBO)
            glDrawElements(GL_LINE_LOOP, 4, GL_UNSIGNED_INT, None)
