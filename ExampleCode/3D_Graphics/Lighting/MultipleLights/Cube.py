#! /usr/bin/env python3
#
# Cube object
#
# Simple cube object with OpenGL data loading and drawing interfaces.  The data that
# is being stored is created in three separate arrays, one each for vertices, colors,
# and normals.  These blocks of data are transferred to a single array buffer on the graphics
# card in three separate locations (that is the data is not intermixed) and hence we can
# set up the reading pointers as having tightly packed data. There are also index arrays
# for drawing faces and for outlines.
#
# The cube is centered at the origin and is unit length in all three directions.
#
# Don Spickler
# 1/6/2022

from OpenGL.GL import *
import ctypes
import numpy as np


class Cube():
    # Constructor
    def __init__(self):
        self.drawStyle = 0
        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        vColor = 1
        vNormal = 2

        # Vertex data for the cube.
        vertices = [-0.5, 0.5, 0.5, 1,
                    -0.5, -0.5, 0.5, 1,
                    0.5, -0.5, 0.5, 1,
                    0.5, 0.5, 0.5, 1,

                    -0.5, 0.5, -0.5, 1,
                    -0.5, -0.5, -0.5, 1,
                    0.5, -0.5, -0.5, 1,
                    0.5, 0.5, -0.5, 1,

                    -0.5, 0.5, 0.5, 1,
                    -0.5, 0.5, -0.5, 1,
                    0.5, 0.5, -0.5, 1,
                    0.5, 0.5, 0.5, 1,

                    -0.5, -0.5, 0.5, 1,
                    -0.5, -0.5, -0.5, 1,
                    0.5, -0.5, -0.5, 1,
                    0.5, -0.5, 0.5, 1,

                    0.5, -0.5, 0.5, 1,
                    0.5, -0.5, -0.5, 1,
                    0.5, 0.5, -0.5, 1,
                    0.5, 0.5, 0.5, 1,

                    -0.5, -0.5, 0.5, 1,
                    -0.5, -0.5, -0.5, 1,
                    -0.5, 0.5, -0.5, 1,
                    -0.5, 0.5, 0.5, 1]

        # Color data for the cube.
        colors = [1, 0, 0,
                  1, 0, 0,
                  1, 0, 0,
                  1, 0, 0,
                  0, 1, 0,
                  0, 1, 0,
                  0, 1, 0,
                  0, 1, 0,
                  0, 0, 1,
                  0, 0, 1,
                  0, 0, 1,
                  0, 0, 1,
                  1, 1, 0,
                  1, 1, 0,
                  1, 1, 0,
                  1, 1, 0,
                  0, 1, 1,
                  0, 1, 1,
                  0, 1, 1,
                  0, 1, 1,
                  1, 0, 1,
                  1, 0, 1,
                  1, 0, 1,
                  1, 0, 1]

        normals = [0, 0, 1,
                   0, 0, 1,
                   0, 0, 1,
                   0, 0, 1,

                   0, 0, -1,
                   0, 0, -1,
                   0, 0, -1,
                   0, 0, -1,

                   0, 1, 0,
                   0, 1, 0,
                   0, 1, 0,
                   0, 1, 0,

                   0, -1, 0,
                   0, -1, 0,
                   0, -1, 0,
                   0, -1, 0,

                   1, 0, 0,
                   1, 0, 0,
                   1, 0, 0,
                   1, 0, 0,

                   -1, 0, 0,
                   -1, 0, 0,
                   -1, 0, 0,
                   -1, 0, 0]

        # Face index data for a filled in cube using two triangles per face.
        indicesFill = [0, 1, 2,
                       2, 3, 0,
                       6, 5, 4,
                       4, 7, 6,
                       10, 9, 8,
                       8, 11, 10,
                       12, 13, 14,
                       14, 15, 12,
                       16, 17, 18,
                       18, 19, 16,
                       22, 21, 20,
                       20, 23, 22]

        # Outline index data for the cube using two vertices per line.
        indicesOutline = [0, 1, 1, 2, 2, 3, 3, 0,
                          4, 5, 5, 6, 6, 7, 7, 4,
                          8, 9, 9, 10, 10, 11, 11, 8,
                          12, 13, 13, 14, 14, 15, 15, 12,
                          16, 17, 17, 18, 18, 19, 19, 16,
                          20, 21, 21, 22, 22, 23, 23, 20]

        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(indicesFill).astype(ctypes.c_uint)
        indexoutlinedata = np.array(indicesOutline).astype(ctypes.c_uint)
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        colordata = np.array(colors).astype(ctypes.c_float)
        normaldata = np.array(normals).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)

        self.BoxVAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)
        self.BoxEBO = glGenBuffers(2)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.BoxVAO)

        # Load the indexing arrays on the graphics card. Load the fill index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[0])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(indicesFill), indexdata, GL_STATIC_DRAW)

        # Load the outline index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(indicesOutline), indexoutlinedata, GL_STATIC_DRAW)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate space for the vertex and color data.Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(colors) + len(normals)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(colors), colordata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(colors)), floatsz * len(normals), normaldata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))
        glVertexAttribPointer(vNormal, 3, GL_FLOAT, GL_FALSE, 0,
                              ctypes.c_void_p(floatsz * (len(vertices) + len(colors))))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vColor)
        glEnableVertexAttribArray(vNormal)

    # Draw the Cube.
    def draw(self):
        glBindVertexArray(self.BoxVAO)
        if self.drawStyle == 0:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[0])
            glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        elif self.drawStyle == 1:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.BoxEBO[1])
            glDrawElements(GL_LINES, 48, GL_UNSIGNED_INT, None)
