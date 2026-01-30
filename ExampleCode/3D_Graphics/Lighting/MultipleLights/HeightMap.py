#! /usr/bin/env python3
#
# Height Map object
#
# Creates the vertex and normal vector data for a height map object and
# loads the data to the grphics card. The image used for the map is
# assumed to be a PIL Image object in RGB (0-255) format.
#
# Don Spickler
# 1/7/2022

from OpenGL.GL import *
import ctypes
import numpy as np
import glm
from PIL import Image


class HeightMap():
    # Constructor, img is assumed to be a PIL Image.
    def __init__(self, img, w=1, h=1, bump=1, lon=20, lat=20):
        self.img = img
        self.w = w
        self.h = h
        self.lon = lon
        self.lat = lat
        self.bump = bump

        # Setup VAO and buffers.
        self.VAO = glGenVertexArrays(1)
        self.EBO = glGenBuffers(1)
        self.ArrayBuffer = glGenBuffers(1)

        self.LoadDataToGraphicsCard()

    # Reset the properties of the object, img is assumed to be a PIL Image.
    def set(self, img, w=1, h=1, bump=1, lon=20, lat=20):
        self.img = img
        self.w = w
        self.h = h
        self.lon = lon
        self.lat = lat
        self.bump = bump
        self.LoadDataToGraphicsCard()

    def pos(self, i, j):
        return 3 * ((self.lat + 1) * i + j)

    # Load vertex, normal, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        # vColor = 1 # Unused here but in some shaders.
        vNormal = 2

        # Load vertex data into list.
        vertices = []
        for i in range(self.lon + 1):
            for j in range(self.lat + 1):
                x = -self.w / 2 + self.w * (i / self.lon)
                y = -self.h / 2 + self.h * (j / self.lat)

                # Get z coordinate by image pixel value, assumed that the image is RGB (0-255).
                posx = int((self.img.width - 1) * (i / self.lon))
                posy = int((self.img.height - 1) * (j / self.lat))
                pix = self.img.getpixel((posx, posy))
                inten = (pix[0] + pix[1] + pix[2]) / (3 * 255)
                z = self.bump * inten

                vertices.extend([x, y, z])

        # Load noraml data into list.
        normals = []
        for i in range(self.lon + 1):
            for j in range(self.lat + 1):
                vecpos = [0, 0, 0, 0]
                sumvec = glm.vec3(0)
                # Get endpoint positions to the vectors to be crossed.
                for k in range(8):
                    if k == 0:
                        vecpos = [i + 1, j, i + 1, j + 1]
                    if k == 1:
                        vecpos = [i + 1, j + 1, i, j + 1]
                    if k == 2:
                        vecpos = [i, j + 1, i - 1, j + 1]
                    if k == 3:
                        vecpos = [i - 1, j + 1, i - 1, j]
                    if k == 4:
                        vecpos = [i - 1, j, i - 1, j - 1]
                    if k == 5:
                        vecpos = [i - 1, j - 1, i, j - 1]
                    if k == 6:
                        vecpos = [i, j - 1, i + 1, j - 1]
                    if k == 7:
                        vecpos = [i + 1, j - 1, i + 1, j]

                    # If the point is inside the grid.
                    if 0 <= vecpos[0] <= self.lon and 0 <= vecpos[1] <= self.lat:
                        if 0 <= vecpos[2] <= self.lon and 0 <= vecpos[3] <= self.lat:
                            # Get positions of endpoint positions in the vertex list to vectors.
                            p = self.pos(i, j)
                            p1 = self.pos(vecpos[0], vecpos[1])
                            p2 = self.pos(vecpos[2], vecpos[3])
                            # Create vec3 objects of (x, y, z) points.
                            v = glm.vec3(vertices[p], vertices[p + 1], vertices[p + 2])
                            v1 = glm.vec3(vertices[p1], vertices[p1 + 1], vertices[p1 + 2])
                            v2 = glm.vec3(vertices[p2], vertices[p2 + 1], vertices[p2 + 2])
                            # Subtract endpoints to get vecotrs.
                            tv1 = glm.normalize(v1 - v)
                            tv2 = glm.normalize(v2 - v)
                            # Take cross product for normal vector and add it to the vector accumulator.
                            cp = glm.cross(tv1, tv2)
                            sumvec += cp

                # Normalize the accumulation vector and append to the normal vector list.
                if glm.length(sumvec) > 0.000001:
                    normals.extend(glm.normalize(sumvec))
                else:
                    normals.extend(glm.vec3(0))

        # Setup indexing array for triangles.
        indices = []
        for i in range(self.lon):
            for j in range(self.lat):
                indices.append(i * (self.lat + 1) + j)
                indices.append((i + 1) * (self.lat + 1) + j)
                indices.append((i + 1) * (self.lat + 1) + j + 1)
                indices.append(i * (self.lat + 1) + j)
                indices.append((i + 1) * (self.lat + 1) + j + 1)
                indices.append(i * (self.lat + 1) + j + 1)

        # Convert data to GLSL form and get machine sizes of data types.
        indexdata = np.array(indices).astype(ctypes.c_uint)
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        normaldata = np.array(normals).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)
        uintsz = ctypes.sizeof(ctypes.c_uint)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.VAO)

        # Load the indexing arrays on the graphics card. Load the fill index array.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, uintsz * len(indices), indexdata, GL_STATIC_DRAW)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate space but not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(normals)), None, GL_DYNAMIC_DRAW)

        # Load the data.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(normals), normaldata)

        # Setup attribute information.
        glVertexAttribPointer(vPosition, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vNormal, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vNormal)

    # Draw the Object.
    def draw(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glDrawElements(GL_TRIANGLES, 6 * self.lon * self.lat, GL_UNSIGNED_INT, None)
