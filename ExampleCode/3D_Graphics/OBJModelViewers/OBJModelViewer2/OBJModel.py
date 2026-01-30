#! /usr/bin/env python3

"""
OBJ Model object

This version uses only one shader for the model, loaded in the graphics engine.
Material and texture uniform locations are sent to the model class.
Matrix loading and lighting are controlled by the graphics engine.
Material and texture loading is controlled by the model class.

Don Spickler
4/16/2022
"""

import glm
from OpenGL.GL import *
import ctypes
import numpy as np
import os
from PIL import Image


class OBJMaterial():
    def __init__(self):
        self.name = ""
        self.ambient = glm.vec4(0, 0, 0, 1)
        self.diffuse = glm.vec4(0, 0, 0, 1)
        self.specular = glm.vec4(0, 0, 0, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 1
        # Textures are the texture IDs
        self.ambientTexture = None
        self.diffuseTexture = None
        self.specularTexture = None


class OBJModel():
    # Constructor bring in references to the shader and to the uniform locations.
    def __init__(self, sh, aloc, dloc, sloc, eloc, floc, texa, texd, texs, texab, texdb, texsb):
        self.shader = sh
        self.mataloc = aloc
        self.matdloc = dloc
        self.matsloc = sloc
        self.mateloc = eloc
        self.matfloc = floc
        self.texaloc = texa
        self.texdloc = texd
        self.texsloc = texs
        self.texabloc = texab
        self.texdbloc = texdb
        self.texsbloc = texsb

        self.numvertices = 0

        # The materialsList keeps a list of OBJMaterial objects that stores the material
        # attributes for that material and the names of any texture files that are to be
        # applied.  Textrues are not loaded in this class, it is the job of the graphics engine
        # to do that.
        self.materialsList = []

        # The renderLayout list contains a list of list pairs.  Each pair is the name of a
        # material to be used, that matches a material from the materialsList, and the
        # vertex position on where that material is to start being used.  This allows an
        # external class, such as a graphics engine, to extract all needed data for rendering.
        self.renderLayout = []

        self.ModelVAO = glGenVertexArrays(1)
        self.ArrayBuffer = glGenBuffers(1)

    def __del__(self):
        self.clearData()

    # Convert space separated strings into lists strings.
    def stringList(self, datastring):
        datastring = " ".join(datastring.split())
        datastring = datastring.rstrip().lstrip()
        datastringlist = datastring.split(" ")
        return datastringlist

    # This converts a text string of three numbers into a glm.vec4 of floats.
    def makeColorGLMVector(self, datastring):
        coor = [float(n) for n in self.stringList(datastring)]
        return glm.vec4(coor[0], coor[1], coor[2], 1)

    # Convert space separated numeric strings into lists of numeric data, floats.
    def makeDataList(self, datastring):
        return [float(n) for n in self.stringList(datastring)]

    # Convert space separated numeric strings into lists of numeric data, integers.
    def makeDataListInt(self, datastring):
        return [int(n) for n in self.stringList(datastring)]

    # Load a texture object, assign it to an active texture and set its attributes.
    def loadTexture(self, path, filename):
        texturefilename = path + filename
        teximg = Image.open(texturefilename).convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.asarray(teximg)
        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, teximg.size[0], teximg.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        return texID

    # This function loads the material from the material file that is referenced in the
    # Wavefront OBJ file.
    def loadMaterials(self, path, filename):
        materialdatatext = open(path + filename, 'r').read()
        materialdata = materialdatatext.split("\n")

        # Process line by line, beginning of the line designates that type of data to be loaded
        # into the material attribute structure.
        for i in range(len(materialdata)):
            lastmat = len(self.materialsList) - 1
            line = materialdata[i]
            if line.startswith("newmtl "):
                newmaterial = OBJMaterial()
                newmaterial.name = line[7:].rstrip().lstrip()
                self.materialsList.append(newmaterial)
            elif line.startswith("Ns "):
                self.materialsList[lastmat].shininess = float(line[3:])
            elif line.startswith("Ka "):
                self.materialsList[lastmat].ambient = self.makeColorGLMVector(line[3:])
            elif line.startswith("Kd "):
                self.materialsList[lastmat].diffuse = self.makeColorGLMVector(line[3:])
            elif line.startswith("Ks "):
                self.materialsList[lastmat].specular = self.makeColorGLMVector(line[3:])
            elif line.startswith("Ke "):
                self.materialsList[lastmat].emission = self.makeColorGLMVector(line[3:])
            elif line.startswith("map_Ka "):
                filename = os.path.basename(line[7:])
                self.materialsList[lastmat].ambientTexture = self.loadTexture(path, filename)
            elif line.startswith("map_Kd "):
                filename = os.path.basename(line[7:])
                self.materialsList[lastmat].diffuseTexture = self.loadTexture(path, filename)
            elif line.startswith("map_Ks "):
                filename = os.path.basename(line[7:])
                self.materialsList[lastmat].specularTexture = self.loadTexture(path, filename)

    # Load the data from the file into vertex, normal, and texture coordinate structures.
    # This data is then loaded into a single VBO and VAO.  The renderLayout list keeps the
    # vertex numbers for each segment and this can be used in the glDrawArrays command either
    # in this class or in an external class.
    def load(self, path, filename):
        vPosition = 0
        vColor = 1  # Unused but in some shaders.
        vNormal = 2
        vTex = 3

        self.clearData()

        modeldatatext = open(path + filename, 'r').read()
        modeldata = modeldatatext.split("\n")

        vertexdata = []
        normaldata = []
        texcoorddata = []

        # Extract vertex, normal, and texture corrdinate data and load into data lists.
        for i in range(len(modeldata)):
            line = modeldata[i]
            if line.startswith("v "):
                vertexdata.append(self.makeDataList(line[2:]))
            elif line.startswith("vn "):
                normaldata.append(self.makeDataList(line[3:]))
            elif line.startswith("vt "):
                texcoorddata.append(self.makeDataList(line[3:]))

        GC_vertexdata = []
        GC_normaldata = []
        GC_texcoorddata = []

        # Process face data.
        for i in range(len(modeldata)):
            line = modeldata[i]
            if line.startswith("f "):
                line = line[2:]
                numsep = line.count("/")

                if numsep == 6:
                    numdoublesep = line.count("//")
                    if numdoublesep == 0:
                        # Format: 12397/4407/17814 12396/4406/17814 12348/4357/17814  v/t/n
                        line = line.replace('/', ' ')
                        ilist = self.makeDataListInt(line)
                        # OBJ format starts indexing at 1 and not 0.
                        ilist = [n - 1 for n in ilist]

                        for j in range(3):
                            GC_vertexdata.extend(vertexdata[ilist[3 * j + 0]])
                            GC_texcoorddata.extend(texcoorddata[ilist[3 * j + 1]])
                            GC_normaldata.extend(normaldata[ilist[3 * j + 2]])

                    elif numdoublesep == 3:
                        # Format: 12397//17814 12396//17814 12348//17814  v//n
                        line = line.replace('//', ' ')
                        ilist = self.makeDataListInt(line)
                        # OBJ format starts indexing at 1 and not 0.
                        ilist = [n - 1 for n in ilist]

                        for j in range(3):
                            GC_vertexdata.extend(vertexdata[ilist[2 * j + 0]])
                            GC_texcoorddata.extend([0, 0])
                            GC_normaldata.extend(normaldata[ilist[2 * j + 1]])

                elif numsep == 3:
                    # Format: 12397/17814 12396/17814 12348/17814   v/t
                    line = line.replace('/', ' ')
                    ilist = self.makeDataListInt(line)
                    # OBJ format starts indexing at 1 and not 0.
                    ilist = [n - 1 for n in ilist]

                    for j in range(3):
                        GC_vertexdata.extend(vertexdata[ilist[2 * j + 0]])
                        GC_texcoorddata.extend(texcoorddata[ilist[2 * j + 1]])
                        GC_normaldata.extend([0, 0, 0])

                elif numsep == 0:
                    # Format: 12397 12396 12348   v
                    ilist = self.makeDataListInt(line)
                    # OBJ format starts indexing at 1 and not 0.
                    ilist = [n - 1 for n in ilist]

                    for j in range(3):
                        GC_vertexdata.extend(vertexdata[ilist[j]])
                        GC_texcoorddata.extend([0, 0])
                        GC_normaldata.extend([0, 0, 0])

            elif line.startswith("mtllib "):
                materialfile = line[7:].rstrip().lstrip()
                self.loadMaterials(path, materialfile)
            elif line.startswith("usemtl "):
                self.renderLayout.append([line[7:].rstrip().lstrip(), len(GC_vertexdata) // 3])

        # Load data up to the card and set attributes.
        vdata = np.array(GC_vertexdata).astype(ctypes.c_float)
        tdata = np.array(GC_texcoorddata).astype(ctypes.c_float)
        ndata = np.array(GC_normaldata).astype(ctypes.c_float)
        floatsz = ctypes.sizeof(ctypes.c_float)

        # Bind (turn on) a vertex array.
        glBindVertexArray(self.ModelVAO)

        # Bind (turn on) the vertex buffer (storage location).
        glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)

        # Allocate space for the vertex and color data. Do not load data at this point.
        glBufferData(GL_ARRAY_BUFFER, floatsz * (len(vdata) + len(ndata) + len(tdata)), None, GL_DYNAMIC_DRAW)

        # Load the data vertex at the beginning and then color at the end.
        glBufferSubData(GL_ARRAY_BUFFER, 0, floatsz * len(vdata), vdata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * len(vdata), floatsz * len(ndata), ndata)
        glBufferSubData(GL_ARRAY_BUFFER, floatsz * (len(vdata) + len(ndata)), floatsz * len(tdata), tdata)

        # Setup attribute information. Note that the 5th parameter is 0, indicating tightly packed.
        glVertexAttribPointer(vPosition, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribPointer(vNormal, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * len(vdata)))
        glVertexAttribPointer(vTex, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(floatsz * (len(vdata) + len(ndata))))

        # Set position indexes for shader streams.
        glEnableVertexAttribArray(vPosition)
        glEnableVertexAttribArray(vNormal)
        glEnableVertexAttribArray(vTex)

        self.numvertices = len(vdata) // 3

    # Sends all the segments through the pipeline.
    def draw(self):
        glUseProgram(self.shader)
        glBindVertexArray(self.ModelVAO)
        for i in range(len(self.renderLayout)):
            matname = self.renderLayout[i][0]

            # Find the material for the segment.
            for mat in self.materialsList:
                if mat.name == matname:
                    break

            # Load the material for the segment.
            glUniform4fv(self.mataloc, 1, glm.value_ptr(mat.ambient))
            glUniform4fv(self.matdloc, 1, glm.value_ptr(mat.diffuse))
            glUniform4fv(self.matsloc, 1, glm.value_ptr(mat.specular))
            glUniform4fv(self.mateloc, 1, glm.value_ptr(mat.emission))
            glUniform1f(self.matfloc, mat.shininess)

            # Load the ambient texture location to the shader.
            glActiveTexture(GL_TEXTURE0 + self.texaloc)
            if mat.ambientTexture is not None:
                glBindTexture(GL_TEXTURE_2D, mat.ambientTexture)
                glUniform1i(self.texabloc, True)
            else:
                glUniform1i(self.texabloc, False)

            # Load the diffuse texture location to the shader.
            glActiveTexture(GL_TEXTURE0 + self.texdloc)
            if mat.diffuseTexture is not None:
                glBindTexture(GL_TEXTURE_2D, mat.diffuseTexture)
                glUniform1i(self.texdbloc, True)
            else:
                glUniform1i(self.texdbloc, False)

            # Load the specular texture location to the shader.
            glActiveTexture(GL_TEXTURE0 + self.texsloc)
            if mat.specularTexture is not None:
                glBindTexture(GL_TEXTURE_2D, mat.specularTexture)
                glUniform1i(self.texsbloc, True)
            else:
                glUniform1i(self.texsbloc, False)

            # Draw segment.
            start = self.renderLayout[i][1]
            if i == len(self.renderLayout) - 1:
                end = self.numvertices
            else:
                end = self.renderLayout[i + 1][1]
            glDrawArrays(GL_TRIANGLES, start, end - start)

    # Removes the data from the graphics card.
    def clearData(self):
        try:
            glBindVertexArray(self.ModelVAO)
            glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)
            glBufferData(GL_ARRAY_BUFFER, 0, None, GL_STATIC_DRAW)

            for matinfo in self.materialsList:
                if matinfo.ambientTexture is not None:
                    glDeleteTextures(np.array(matinfo.ambientTexture))
                if matinfo.diffuseTexture is not None:
                    glDeleteTextures(np.array(matinfo.diffuseTexture))
                if matinfo.specularTexture is not None:
                    glDeleteTextures(np.array(matinfo.specularTexture))

            self.materialsList = []
            self.renderLayout = []
        except Exception as err:
            self.materialsList = []
            self.renderLayout = []
            for i in range(len(err.args)):
                print(err.args[i])
