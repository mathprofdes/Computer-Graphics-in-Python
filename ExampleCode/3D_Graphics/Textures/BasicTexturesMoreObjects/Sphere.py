#! /usr/bin/env python3
#
# Sphere object
#
# Creates the vertex and normal vector data for a sphere object and
# loads the data to the grphics card.
#
# Don Spickler
# 1/7/2022

from OpenGL.GL import *
import ctypes
import numpy as np
import glm


class Sphere():
    # Constructor
    def __init__(self, r=1, lon=20, lat=20,
                 begintheta=0, endtheta=2 * np.pi,
                 beginpsi=-np.pi / 2, endpsi=np.pi / 2):
        self.r = r
        self.lon = lon
        self.lat = lat
        self.bt = begintheta
        self.et = endtheta
        self.bp = beginpsi
        self.ep = endpsi

        # Setup VAO and buffers.
        self.VAO = glGenVertexArrays(1)
        self.EBO = glGenBuffers(1)
        self.ArrayBuffer = glGenBuffers(1)

        self.LoadDataToGraphicsCard()

    # Reset the properties of the object.
    def set(self, r=1, lon=20, lat=20,
              begintheta=0, endtheta=2 * np.pi,
              beginpsi=-np.pi / 2, endpsi=np.pi / 2):
        self.r = r
        self.lon = lon
        self.lat = lat
        self.bt = begintheta
        self.et = endtheta
        self.bp = beginpsi
        self.ep = endpsi
        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        # vColor = 1 # Unused here but in some shaders.
        vNormal = 2
        vTex = 3

        vertices = []
        normals = []
        tex = []

        # Load data into lists.
        for i in range(self.lon + 1):
            for j in range(self.lat + 1):
                theta = self.bt + (self.et - self.bt) * (i / self.lon)
                psi = self.bp + (self.ep - self.bp) * (j / self.lat)

                # Calculate the vertices.
                x = self.r * glm.cos(psi) * glm.cos(theta)
                y = self.r * glm.cos(psi) * glm.sin(theta)
                z = self.r * glm.sin(psi)

                # Calculate the normals.
                nx = x / self.r
                ny = y / self.r
                nz = z / self.r

                vertices.extend([x, y, z])
                normals.extend([nx, ny, nz])
                tex.extend([i / self.lon, j / self.lat])

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
        texdata = np.array(tex).astype(ctypes.c_float)
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
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(normals) + len(tex)), None, GL_DYNAMIC_DRAW)

        # Load the data.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(normals), normaldata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(normals)), floatsz * len(tex), texdata)

        # Setup attribute information.
        glVertexAttribPointer(vPosition, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vNormal, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))
        glVertexAttribPointer(vTex, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * (len(vertices) + len(normals))))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vNormal)
        glEnableVertexAttribArray(vTex)

    # Draw the Object.
    def draw(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glDrawElements(GL_TRIANGLES, 6 * self.lon * self.lat, GL_UNSIGNED_INT, None)
