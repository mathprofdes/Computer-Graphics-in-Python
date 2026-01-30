#! /usr/bin/env python3

"""
OBJ Model object

This version lets the model take care of all the shader information.
Matrix, lights, materials and textures are loaded from the model class.
The graphics engine still communicates directly with the UI and loads
the needed information to the model class to load into the shaders.

Don Spickler
4/16/2022
"""

import glm
from OpenGL.GL import *
import ctypes
import numpy as np
import os
from PIL import Image
from Shader import *


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
    # Constructor
    def __init__(self):
        self.PVMatrix = glm.mat4(1.0)
        self.Model = glm.mat4(1.0)
        self.eye = glm.vec3(0, 0, 0)
        self.lights = []

        self.objvert = open("Shaders/OBJModelVert.glsl", 'r').read()
        self.objfrag = open("Shaders/OBJModelFrag.glsl", 'r').read()
        self.shaderList = []
        self.numvertices = 0

        # The renderLayout list contains a list of list pairs.  Each pair is the name of a
        # material to be used, that matches a material from the materialsList, and the
        # vertex position on where that material is to start being used.  This allows an
        # external class, such as a graphics engine, to extract all needed data for rendering.
        self.renderLayout = []

        # Keeps a list of the textures so that they can be cleared.
        self.textureList = []

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
        materialsList = []

        # Process line by line, beginning of the line designates that type of data to be loaded
        # into the material attribute structure.
        for i in range(len(materialdata)):
            lastmat = len(materialsList) - 1
            line = materialdata[i]
            if line.startswith("newmtl "):
                newmaterial = OBJMaterial()
                newmaterial.name = line[7:].rstrip().lstrip()
                materialsList.append(newmaterial)
            elif line.startswith("Ns "):
                materialsList[lastmat].shininess = float(line[3:])
            elif line.startswith("Ka "):
                materialsList[lastmat].ambient = self.makeColorGLMVector(line[3:])
            elif line.startswith("Kd "):
                materialsList[lastmat].diffuse = self.makeColorGLMVector(line[3:])
            elif line.startswith("Ks "):
                materialsList[lastmat].specular = self.makeColorGLMVector(line[3:])
            elif line.startswith("Ke "):
                materialsList[lastmat].emission = self.makeColorGLMVector(line[3:])
            elif line.startswith("map_Ka "):
                filename = os.path.basename(line[7:])
                tex = self.loadTexture(path, filename)
                materialsList[lastmat].ambientTexture = tex
                self.textureList.append(tex)
            elif line.startswith("map_Kd "):
                filename = os.path.basename(line[7:])
                tex = self.loadTexture(path, filename)
                materialsList[lastmat].diffuseTexture = tex
                self.textureList.append(tex)
            elif line.startswith("map_Ks "):
                filename = os.path.basename(line[7:])
                tex = self.loadTexture(path, filename)
                materialsList[lastmat].specularTexture = tex
                self.textureList.append(tex)

        if len(materialsList) == 0:
            return

        # Create dummy program to retrieve the locations of the uniform variables.
        # Since the shaders are all the same the uniforms will have the same positions
        # and hence can be used in multiple shaders.
        shader = Shader()
        prog = shader.loadShaders(self.objvert, self.objfrag)
        glUseProgram(prog)
        self.PVLoc = glGetUniformLocation(prog, "PV")
        self.ModelLoc = glGetUniformLocation(prog, "Model")
        self.NormalLoc = glGetUniformLocation(prog, "NormalMatrix")
        self.EyeLoc = glGetUniformLocation(prog, "eye")

        aloc = glGetUniformLocation(prog, "Mat.ambient")
        dloc = glGetUniformLocation(prog, "Mat.diffuse")
        sloc = glGetUniformLocation(prog, "Mat.specular")
        eloc = glGetUniformLocation(prog, "Mat.emission")
        shloc = glGetUniformLocation(prog, "Mat.shininess")

        atexloc = glGetUniformLocation(prog, "atex")
        dtexloc = glGetUniformLocation(prog, "dtex")
        stexloc = glGetUniformLocation(prog, "stex")
        ausetexloc = glGetUniformLocation(prog, "useATex")
        dusetexloc = glGetUniformLocation(prog, "useDTex")
        susetexloc = glGetUniformLocation(prog, "useSTex")

        # Remove dummy program from memory.
        try:
            glDeleteProgram(prog)
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])

        # Convert marterials to shaders. So each material in the model will have
        # its own separate shader.
        for mat in materialsList:
            prog = shader.loadShaders(self.objvert, self.objfrag)
            glUseProgram(prog)
            glUniform4fv(aloc, 1, glm.value_ptr(mat.ambient))
            glUniform4fv(dloc, 1, glm.value_ptr(mat.diffuse))
            glUniform4fv(sloc, 1, glm.value_ptr(mat.specular))
            glUniform4fv(eloc, 1, glm.value_ptr(mat.emission))
            glUniform1f(shloc, mat.shininess)

            if mat.ambientTexture:
                glActiveTexture(GL_TEXTURE0 + mat.ambientTexture)
                glBindTexture(GL_TEXTURE_2D, mat.ambientTexture)
                glUniform1i(atexloc, mat.ambientTexture)
                glUniform1i(ausetexloc, True)
            else:
                glUniform1i(ausetexloc, False)

            if mat.diffuseTexture:
                glActiveTexture(GL_TEXTURE0 + mat.diffuseTexture)
                glBindTexture(GL_TEXTURE_2D, mat.diffuseTexture)
                glUniform1i(dtexloc, mat.diffuseTexture)
                glUniform1i(dusetexloc, True)
            else:
                glUniform1i(dusetexloc, False)

            if mat.specularTexture:
                glActiveTexture(GL_TEXTURE0 + mat.specularTexture)
                glBindTexture(GL_TEXTURE_2D, mat.specularTexture)
                glUniform1i(stexloc, mat.specularTexture)
                glUniform1i(susetexloc, True)
            else:
                glUniform1i(susetexloc, False)

            shaderentry = [mat.name, prog]
            self.shaderList.append(shaderentry)

        self.LoadMatrices(self.Model)
        self.LoadPV(self.PVMatrix)
        self.LoadLights(self.lights)
        self.LoadEye(self.eye)

    # Load the data from the file into vertex, normal, and texture coordinate structures.
    # This data is then loaded into a single VBO and VAO.  The renderLayout list keeps the
    # vertex numbers for each segment and this can be used in the glDrawArrays command either
    # in this class or in an external class.
    def load(self, path, filename):
        self.clearData()

        vPosition = 0
        vColor = 1  # Unused but in some shaders.
        vNormal = 2
        vTex = 3

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

    def LoadMatrices(self, model):
        NM = glm.inverse(glm.transpose(glm.mat3(model)))
        self.Model = model
        for sh in self.shaderList:
            glUseProgram(sh[1])
            glUniformMatrix4fv(self.ModelLoc, 1, GL_FALSE, glm.value_ptr(model))
            glUniformMatrix3fv(self.NormalLoc, 1, GL_FALSE, glm.value_ptr(NM))

    def LoadPV(self, PV):
        self.PVMatrix = PV
        for sh in self.shaderList:
            glUseProgram(sh[1])
            glUniformMatrix4fv(self.PVLoc, 1, GL_FALSE, glm.value_ptr(PV))

    def LoadLights(self, lights):
        self.lights = lights
        for sh in self.shaderList:
            glUseProgram(sh[1])
            i = 0
            glUniform1i(glGetUniformLocation(sh[1], "numLights"), len(lights))
            for light in lights:
                light.LoadLight(sh[1], "Lt[" + str(i) + "]")
                i += 1

    def LoadEye(self, eye):
        self.eye = eye
        for sh in self.shaderList:
            glUseProgram(sh[1])
            glUniform3fv(self.EyeLoc, 1, glm.value_ptr(eye))

    # Sends all the segments through the pipeline.
    def draw(self):
        glBindVertexArray(self.ModelVAO)
        for i in range(len(self.renderLayout)):
            matname = self.renderLayout[i][0]

            # Find the shader program to use, that matches the material of the segment.
            for sh in self.shaderList:
                if sh[0] == matname:
                    break

            # Use the shader program.
            glUseProgram(sh[1])

            # Draw the segment.
            start = self.renderLayout[i][1]
            if i == len(self.renderLayout) - 1:
                end = self.numvertices
            else:
                end = self.renderLayout[i + 1][1]
            glDrawArrays(GL_TRIANGLES, start, end - start)

    # Removes the data, VAO, VBO, and textures from the graphics card.
    def clearData(self):
        try:
            glBindVertexArray(self.ModelVAO)
            glBindBuffer(GL_ARRAY_BUFFER, self.ArrayBuffer)
            glBufferData(GL_ARRAY_BUFFER, 0, None, GL_STATIC_DRAW)

            for tex in self.textureList:
                glDeleteTextures(np.array(tex))

            for sh in self.shaderList:
                glDeleteProgram(sh[1])

            self.textureList = []
            self.shaderList = []
            self.renderLayout = []
        except Exception as err:
            self.textureList = []
            self.materialsList = []
            self.renderLayout = []
            for i in range(len(err.args)):
                print(err.args[i])
