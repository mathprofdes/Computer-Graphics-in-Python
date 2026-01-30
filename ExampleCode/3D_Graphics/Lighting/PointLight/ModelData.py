#! /usr/bin/env python3
#
# Model Data object
#
# This object will load in raw (text) data for an object. The data file is to be
# a text file containing one line each for each vertex.  Each vertex line must contain
# 8 numbers, 3 for the vertex, 3 for the normal, and 2 for a texture coordinate.
# The order of these can be in whichever order you wish and is specified by the
# formattype parameter string which can be any of VNT, VTN, TVN, TNV, NTV, or NVT.
# Order of the components must be (x, y, z), (nx, ny, nz), and (tx, ty).
# The values on each vertex line must be separated by spaces.
#
# Don Spickler
# 1/7/2022

from OpenGL.GL import *
import ctypes
import numpy as np
import glm
from PIL import Image


class ModelData():
    # Constructor, img is assumed to be a PIL Image.
    def __init__(self, datafile=None, formattype="VNT"):
        # Setup VAO and buffers.
        self.datafilename = datafile
        self.type = formattype.upper()
        self.vertexcount = 0

        self.VAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)

        self.LoadDataToGraphicsCard()

    # Reset the properties of the object, img is assumed to be a PIL Image.
    def set(self, datafile=None, formattype="VNT"):
        self.datafilename = datafile
        self.type = formattype.upper()
        self.vertexcount = 0

        self.LoadDataToGraphicsCard()

    # Convert space separated numeric strings into lists of numeric data, floats.
    def makeDataList(self, datastring):
        # Note that the following could be done in this single line, but not very readable.
        # return [float(n) for n in " ".join(datastring.split()).rstrip().lstrip().split(" ")]

        # Change multiple spaces to a single space.
        datastring = " ".join(datastring.split())
        # Trim
        datastring = datastring.rstrip().lstrip()
        # Split to list of numbers as strings.
        datastringlist = datastring.split(" ")
        # Convert number strings to numeric values. Store in list structure and return.
        return [float(n) for n in datastringlist]

    # Load vertex, normal, and index data to the graphics card.
    def LoadDataToGraphicsCard(self):
        vPosition = 0
        # vColor = 1 # Unused here but in some shaders.
        vNormal = 2
        vTex = 3

        if self.datafilename is None:
            return

        data = open(self.datafilename, 'r').read()
        data = data.split("\n")

        vertices = []
        normals = []
        texcoords = []

        for i in range(len(data)):
            dataline = data[i].rstrip().lstrip()
            if len(dataline) > 0:
                line = self.makeDataList(dataline)
                if self.type == "VNT":
                    vertices.extend(line[0:3])
                    normals.extend(line[3:6])
                    texcoords.extend(line[6:])
                elif self.type == "VTN":
                    vertices.extend(line[0:3])
                    texcoords.extend(line[3:5])
                    normals.extend(line[5:])
                elif self.type == "TVN":
                    texcoords.extend(line[0:2])
                    vertices.extend(line[2:5])
                    normals.extend(line[5:])
                elif self.type == "TNV":
                    texcoords.extend(line[0:2])
                    normals.extend(line[2:5])
                    vertices.extend(line[5:])
                elif self.type == "NVT":
                    normals.extend(line[0:3])
                    vertices.extend(line[3:6])
                    texcoords.extend(line[6:])
                elif self.type == "NTV":
                    normals.extend(line[0:3])
                    texcoords.extend(line[3:5])
                    vertices.extend(line[5:])

        # Convert data to GLSL form and get machine sizes of data types.
        vertexdata = np.array(vertices).astype(ctypes.c_float)
        normaldata = np.array(normals).astype(ctypes.c_float)
        texcoorddata = np.array(texcoords).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.VAO)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate space for the vertex, normal, and texture coordinate data. Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(normals) + len(texcoords)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning, then normals, then texture coordinates.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vertices), vertexdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vertices), floatsz * len(normals), normaldata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * (len(vertices) + len(normals)), floatsz * len(texcoords),
                        texcoorddata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vNormal, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vertices)))
        glVertexAttribPointer(vTex, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * (len(vertices) + len(normals))))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vNormal)
        glEnableVertexAttribArray(vTex)

        self.vertexcount = len(vertices) // 3

    # Draw the Object.
    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertexcount)
