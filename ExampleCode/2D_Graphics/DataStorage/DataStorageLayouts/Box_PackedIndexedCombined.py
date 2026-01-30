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
# (0, 2, 1).
#
# Don Spickler
# 12/06/2021

from OpenGL.GL import *
import ctypes
import numpy as np

class Box_PackedIndexedCombined():
    # Constructor
    def __init__(self, x = 0, y = 0, wd = 1, ht = 1):
        self.cx = x
        self.cy = y
        self.w = wd
        self.h = ht
        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1

        # Vertex and index data for the box, using two triangles.
        vertices = [self.cx - self.w/2, self.cy + self.h/2,
                    self.cx + self.w / 2, self.cy + self.h / 2,
                    self.cx + self.w / 2, self.cy - self.h / 2,
                    self.cx - self.w / 2, self.cy - self.h / 2
                    ]

        colors = [1, 0, 0,
                  0, 1, 0,
                  0, 0, 1,
                  1, 1, 1]

        indices = [0, 3, 2, 0, 2, 1]

        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(indices).astype(ctypes.c_uint)
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)

        self.BoxVAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)
        self.BoxEBO = glGenBuffers(1)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Load the indexing array on the graphics card.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(indices), indexdata, GL_STATIC_DRAW)

        # Bindm(turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate  space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(colors)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(colors), colordata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Draw the box.
    def draw(self):
        glBindVertexArray(self.BoxVAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
