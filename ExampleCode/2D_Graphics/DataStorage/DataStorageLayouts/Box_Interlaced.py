#! /usr/bin/env python3
#
# Box object
#
# This object loads the vertex and color data into a single array buffer.  The data
# is interlaced and hence not packed nor is the drawing is indexed.
#
# Don Spickler
# 12/06/2021

from OpenGL.GL import *
import ctypes
import numpy as np

class Box_Interlaced():
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
        vertex_color_data = [self.cx - self.w/2, self.cy + self.h/2, 1, 0, 0,
                    self.cx - self.w / 2, self.cy - self.h / 2, 1, 1, 1,
                    self.cx + self.w / 2, self.cy - self.h / 2, 0, 0, 1,

                    self.cx - self.w / 2, self.cy + self.h / 2, 1, 0, 0,
                    self.cx + self.w / 2, self.cy - self.h / 2, 0, 0, 1,
                    self.cx + self.w / 2, self.cy + self.h / 2, 0, 1, 0,
                    ]

        # Convert data to GLSL form and get machine sizes of data types.
        data = np.array(vertex_color_data).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)

        self.BoxVAO = glGenVertexArrays(1)
        self.VertexBuffer = glGenBuffers(1)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Bind (turn on) the vertex buffer, load data, set attributes.
        glBindBuffer(GL_ARRAY_BUFFER, self.VertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, floatsz * len(vertex_color_data), data, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 5*floatsz, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 5*floatsz, ctypes.c_void_p(2*floatsz))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)

    # Draw the box.
    def draw(self):
        glBindVertexArray(self.BoxVAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
