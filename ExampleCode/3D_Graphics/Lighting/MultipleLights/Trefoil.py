#! /usr/bin/env python3
#
# Trefoil object
#
# Creates the vertex and normal vector data for a trefoil object and
# loads the data to the grphics card. 
#
# Don Spickler
# 1/7/2022

from OpenGL.GL import *
import ctypes
import numpy as np
import glm


class Trefoil():
    # Constructor
    def __init__(self, rmax=2, rmin=0.2, amp=0.5, lon=200, lat=20, numtwists=1.5, elongfact=1):
        self.rmax = rmax
        self.rmin = rmin
        self.lon = lon
        self.lat = lat
        self.amp = amp
        self.numtwists = numtwists
        self.elongfact = elongfact

        # Setup VAO and buffers.
        self.VAO = glGenVertexArrays(1)
        self.EBO = glGenBuffers(1)
        self.ArrayBuffer = glGenBuffers(1)

        self.LoadDataToGraphicsCard()

    # Reset the properties of the object.
    def set(self, rmax=2, rmin=0.2, amp=0.5, lon=200, lat=20, numtwists=1.5, elongfact=1):
        self.rmax = rmax
        self.rmin = rmin
        self.lon = lon
        self.lat = lat
        self.amp = amp
        self.numtwists = numtwists
        self.elongfact = elongfact
        self.LoadDataToGraphicsCard()

    # Load vertex, color, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        # vColor = 1 # Unused here but in some shaders.
        vNormal = 2

        vertices = []
        normals = []

        # Load data into lists.
        for i in range(self.lon + 1):
            for j in range(self.lat + 1):
                theta = 4 * np.pi - 4 * np.pi * (i / self.lon)
                psi = 2 * np.pi * (j / self.lat)

                # Create data points.
                x = self.rmin * glm.cos(psi) * glm.cos(theta) + self.rmax * glm.cos(theta) * (
                        1 + self.amp * glm.cos(self.numtwists * theta))
                y = self.elongfact * self.rmin * glm.sin(psi) + self.amp * glm.sin(self.numtwists * theta)
                z = self.rmin * glm.cos(psi) * glm.sin(theta) + self.rmax * glm.sin(theta) * (
                        1 + self.amp * glm.cos(self.numtwists * theta))

                # Create tangent vectors to cross for normals.
                nx1 = -self.rmin * glm.cos(psi) * glm.sin(theta) - self.rmax * glm.sin(theta) * (
                        1 + self.amp * glm.cos(self.numtwists * theta)) - self.rmax * glm.cos(theta) * (
                              self.numtwists * self.amp * glm.sin(self.numtwists * theta))
                ny1 = self.numtwists * self.amp * glm.cos(self.numtwists * theta)
                nz1 = self.rmin * glm.cos(psi) * glm.cos(theta) + self.rmax * glm.cos(theta) * (
                        1 + self.amp * glm.cos(self.numtwists * theta)) - self.rmax * glm.sin(
                    theta) * (self.numtwists * self.amp * glm.sin(self.numtwists * theta))

                nx2 = -self.rmin * glm.sin(psi) * glm.cos(theta)
                ny2 = self.elongfact * self.rmin * glm.cos(psi)
                nz2 = -self.rmin * glm.sin(psi) * glm.sin(theta)

                n1 = glm.vec3(nx1, ny1, nz1)
                n2 = glm.vec3(nx2, ny2, nz2)
                n = glm.normalize(glm.cross(n2, n1))

                vertices.extend([x, y, z])
                normals.extend(n)

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

        # Allocate space but do not load data at this point.
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
