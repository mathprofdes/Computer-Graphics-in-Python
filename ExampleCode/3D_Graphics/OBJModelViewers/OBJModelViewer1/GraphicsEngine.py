#! /usr/bin/env python3

"""
Graphics Engine

This version has the graphics engine taking control of all shader activity.
The model loads the data and materials, the graphics engine loads the textures.
The graphics engine extracts the material information from the model, sets the
shader attributes, and invokes the model to draw the segment.
The model stores the material information as well as parses and laods the
vertex data to the graphics card.

Don Spickler
4/16/2022
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm

from Sphere import *
from Axes3D import *
from SphericalCamera import *
from YPRCamera import *
from Light import *
from Material import *
from OBJModel import *


class GraphicsEngine():
    mode = GL_FILL
    shaderProgram = -1
    backgroundnum = 0
    cameranum = 0
    showaxes = True
    showlight = True
    projectionMatrix = glm.mat4(1)
    viewMatrix = glm.mat4(1)
    objshaderprograms = []  # List of program IDs
    texturelist = []  # List of texture names and IDs so that textures can be used in multiple programs.

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            self.shader = Shader()
            self.AxesShader = self.shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                              "Shaders/PassThroughFrag.glsl")
            self.ConstColorShader = self.shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                                    "Shaders/ConstantColorFrag.glsl")
            self.CubemapShader = self.shader.loadShadersFromFile("Shaders/VertexShaderCubeMap.glsl",
                                                                 "Shaders/FragmentCubeMap.glsl")

        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the locations of some of the uniform variables.
        glUseProgram(self.AxesShader)
        self.projviewLocAxes = glGetUniformLocation(self.AxesShader, "ProjView")
        self.modelLocAxes = glGetUniformLocation(self.AxesShader, "Model")

        glUseProgram(self.ConstColorShader)
        self.projviewLocConst = glGetUniformLocation(self.ConstColorShader, "ProjView")
        self.modelLocConst = glGetUniformLocation(self.ConstColorShader, "Model")
        lightcol = glm.vec4(1, 1, 0, 1)
        glUniform4fv(glGetUniformLocation(self.ConstColorShader, "ConstantColor"),
                     1, glm.value_ptr(lightcol))

        glUseProgram(self.CubemapShader)
        self.projviewLocCM = glGetUniformLocation(self.CubemapShader, "PV")

        # Read the chader code for the OBJ model programs.  There will be one program per segment.
        self.objvert = open("Shaders/OBJModelVert.glsl", 'r').read()
        self.objfrag = open("Shaders/OBJModelFrag.glsl", 'r').read()

        # Start with no model in memory.
        self.model = None
        self.activeTextureID = 1

        # Set the projection matrices to all shaders.
        self.setProjectionMatrix(pygame.display.get_surface().get_size())

        # Set clear/background color to black and turn on depth testing.
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)

        # Create the cameras.
        self.sphericalcamera = SphericalCamera(30, 60, 45)
        self.yprcamera = YPRCamera()
        self.setViewMatrix()

        # Create and load the objects.
        self.axes = Axes3D()
        self.cmsphere = Sphere(200)
        self.lightsphere = Sphere(0.25, 10, 10)

        # Create and load the lights.
        self.lights = []
        for i in range(3):
            self.lights.append(Light())
        self.lightcamera = SphericalCamera(20, 45, 45)

        # Set light positions.  Light 0 will ne locked to the lightcamera object.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        self.lights[1].position = glm.vec4(-10, 20, -10, 1)
        self.lights[2].position = glm.vec4(10, -20, -10, 1)

        # Tone down the intensity of the lights.
        # lightFactor = 1
        lightFactor = 0.75
        for i in range(3):
            self.lights[i].diffuse = lightFactor * self.lights[i].diffuse
            self.lights[i].specular = lightFactor * self.lights[i].specular

        self.LoadLights()

        # Load the cubemap.
        glUseProgram(self.CubemapShader)
        glActiveTexture(GL_TEXTURE0)  # Make sure that other texture units do not overlap with this.
        glUniform1i(glGetUniformLocation(self.CubemapShader, "cmtex"), 0)

        self.CubeMapTexId = self.generateCubemapFromOneImage("SkyboxImages/Starfield.jpg")

        # If you wish to replace the star field with a skybox the code to do that is below.

        # SkyboxImageFile = "SkyboxImages/Skybox001.jpg"
        # SkyboxImageFile = "SkyboxImages/Skybox002.jpg"
        # SkyboxImageFile = "SkyboxImages/Skybox003.jpg"
        # SkyboxImageFile = "SkyboxImages/Skybox004.jpg"
        # SkyboxImageFile = "SkyboxImages/Skybox005.jpg"
        # SkyboxImageFile = "SkyboxImages/Skybox006.png"
        # SkyboxImageFile = "SkyboxImages/Skybox007.png"
        # SkyboxImageFile = "SkyboxImages/Skybox008.png"
        # SkyboxImageFile = "SkyboxImages/SkyboxLayout.png"

        # self.CubeMapTexId = self.generateCubemapFromSkybox(SkyboxImageFile)

    def loadModel(self, path, filename):
        # If there is a model already loaded, remove the data from GPU memory.
        if self.model:
            self.model.clearData()

        # Remove program and texture data.
        for prog in self.objshaderprograms:
            glDeleteProgram(prog)

        for texinfo in self.texturelist:
            glDeleteTextures(1, texinfo[1])

        self.objshaderprograms.clear()
        self.texturelist.clear()
        self.activeTextureID = 1

        # Create and load new model.
        self.model = OBJModel()
        self.model.load(path, filename)

        # Create and load programs with material and texture data.
        for i in range(len(self.model.renderLayout)):
            prog = self.shader.loadShaders(self.objvert, self.objfrag)
            glUseProgram(prog)
            materialName = self.model.renderLayout[i][0]

            for j in range(len(self.model.materialsList)):
                if materialName == self.model.materialsList[j].name:
                    self.model.materialsList[j].material.LoadMaterial(prog, "Mat")
                    if self.model.materialsList[j].ambientTexture != "":
                        texid = self.addNewTexture(path, self.model.materialsList[j].ambientTexture)
                        glUniform1i(glGetUniformLocation(prog, "atex"), texid)
                        glUniform1i(glGetUniformLocation(prog, "useATex"), True)

                    if self.model.materialsList[j].diffuseTexture != "":
                        texid = self.addNewTexture(path, self.model.materialsList[j].diffuseTexture)
                        glUniform1i(glGetUniformLocation(prog, "dtex"), texid)
                        glUniform1i(glGetUniformLocation(prog, "useDTex"), True)

                    if self.model.materialsList[j].specularTexture != "":
                        texid = self.addNewTexture(path, self.model.materialsList[j].specularTexture)
                        glUniform1i(glGetUniformLocation(prog, "stex"), texid)
                        glUniform1i(glGetUniformLocation(prog, "useSTex"), True)

            self.objshaderprograms.append(prog)

        # Set matrices and lights for the OBJ shaders.
        self.resetProjectionMatrix()
        self.setViewMatrix()
        self.LoadMatrices(glm.mat4(1))
        self.LoadLights()

    # Add in a new texture.  If the texture is already loaded the ID of that texture is returned.
    # If it is a new texture then load the texture image and assign it a new id.
    def addNewTexture(self, path, filename):
        texid = -1
        for texinfo in self.texturelist:
            if texinfo[0] == filename:
                texid = texinfo[1]

        if texid == -1:
            texid = self.loadTexture(path, filename)
            self.texturelist.append([filename, texid])

        return texid

    # LOad a texture object, assign it to an active texture and set its attributes.
    def loadTexture(self, path, filename):
        texturefilename = path + filename
        texID = -1
        self.activeTextureID += 1

        img = Image.open(texturefilename).convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.asarray(img)
        texID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + self.activeTextureID)
        glBindTexture(GL_TEXTURE_2D, texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        # return texID
        return self.activeTextureID

    # Create a texture cubemap from a skybox image. Load but not assign to an
    # active texture.
    def generateCubemapFromSkybox(self, filemane):
        teximg = Image.open(filemane).convert('RGBA')

        CMID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, CMID)

        # Setup some parameters for texture filters and mipmapping
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        # Get width and height of the subimages.
        imgw = teximg.width // 4
        imgh = teximg.height // 3

        # Extract the subimages and load to texture positions.
        teximgcrop = teximg.crop((2 * imgw, imgh, 3 * imgw, 2 * imgh))
        img_data = np.asarray(teximgcrop)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGBA, teximgcrop.width, teximgcrop.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        teximgcrop = teximg.crop((0, imgh, imgw, 2 * imgh))
        img_data = np.asarray(teximgcrop)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_X, 0, GL_RGBA, teximgcrop.width, teximgcrop.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        teximgcrop = teximg.crop((imgw, 0, 2 * imgw, imgh))
        img_data = np.asarray(teximgcrop)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 0, GL_RGBA, teximgcrop.width, teximgcrop.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        teximgcrop = teximg.crop((imgw, 2 * imgh, 2 * imgw, 3 * imgh))
        img_data = np.asarray(teximgcrop)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, GL_RGBA, teximgcrop.width, teximgcrop.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        teximgcrop = teximg.crop((imgw, imgh, 2 * imgw, 2 * imgh))
        img_data = np.asarray(teximgcrop)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 0, GL_RGBA, teximgcrop.width, teximgcrop.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        teximgcrop = teximg.crop((3 * imgw, imgh, 4 * imgw, 2 * imgh))
        img_data = np.asarray(teximgcrop)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, GL_RGBA, teximgcrop.width, teximgcrop.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        glGenerateMipmap(GL_TEXTURE_CUBE_MAP)

        return CMID

    # Create a texture cubemap from a single image to be repeated on all 6 sides..
    # Load but not assign to an active texture.
    def generateCubemapFromOneImage(self, filemane):
        teximg = Image.open(filemane).convert('RGBA')

        CMID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, CMID)

        # Setup some parameters for texture filters and mipmapping
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        img_data = np.asarray(teximg)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_X, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img_data)

        glGenerateMipmap(GL_TEXTURE_CUBE_MAP)

        return CMID

    # Turn on shader, clear screen, draw axes, cubes, or box.
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        # Draw cubemap.
        if self.backgroundnum == 0:
            glUseProgram(self.CubemapShader)
            self.cmsphere.draw()

        # Draw axes if selected.
        if self.showaxes:
            glUseProgram(self.AxesShader)
            axestrans = glm.scale(glm.vec3(10))
            glUniformMatrix4fv(self.modelLocAxes, 1, GL_FALSE, glm.value_ptr(axestrans))
            self.axes.draw()

        # Draw position of the light if selected.
        if self.showlight:
            glUseProgram(self.ConstColorShader)
            self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
            for i in range(3):
                lightobjmodel = glm.translate(glm.vec3(self.lights[i].position))
                glUniformMatrix4fv(self.modelLocConst, 1, GL_FALSE, glm.value_ptr(lightobjmodel))
                self.lightsphere.draw()

        # Draw remainder of scene.
        if self.model:
            glBindVertexArray(self.model.ModelVAO)
            for i in range(len(self.model.renderLayout)):
                glUseProgram(self.objshaderprograms[i])
                self.model.drawSegment(i)

        self.printOpenGLErrors()

    # Set mode to fill.
    def setFill(self):
        self.mode = GL_FILL

    # Set mode to line.
    def setLine(self):
        self.mode = GL_LINE

    # Set mode to point.
    def setPoint(self):
        self.mode = GL_POINT

    # Load the eye position to all obj shaders, for lighting calculations.
    def LoadEyePosition(self):
        eye = glm.vec3(0, 0, 0)
        if self.cameranum == 0:
            eye = self.sphericalcamera.getPosition()
        elif self.cameranum == 1:
            eye = self.yprcamera.getPosition()

        if len(self.objshaderprograms) > 0:
            t = glGetUniformLocation(self.objshaderprograms[0], "eye")
            for prog in self.objshaderprograms:
                glUseProgram(prog)
                glUniform3fv(t, 1, glm.value_ptr(eye))

    # Load the light object information to all obj shaders, for lighting calculations.
    def LoadLights(self):
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        for prog in self.objshaderprograms:
            glUseProgram(prog)
            glUniform1i(glGetUniformLocation(prog, "numLights"), len(self.lights))
            for i in range(len(self.lights)):
                self.lights[i].LoadLight(prog, "Lt[" + str(i) + "]")

    # Load the position of the movable light.
    def LoadMovingLight(self):
        if len(self.objshaderprograms) > 0:
            self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
            t = glGetUniformLocation(self.objshaderprograms[0], "Lt[0].position")
            for prog in self.objshaderprograms:
                glUseProgram(prog)
                glUniform4fv(t, 1, glm.value_ptr(self.lights[0].position))

    # Loads the model matrix, calculates the normal matrix, (M^(-1))^T, and loads
    # it to the shader.  Function assumes that the lighting shader program is active.
    def LoadMatrices(self, model):
        if len(self.objshaderprograms) > 0:
            NM = glm.inverse(glm.transpose(glm.mat3(model)))
            mloc = glGetUniformLocation(self.objshaderprograms[0], "Model")
            nloc = glGetUniformLocation(self.objshaderprograms[0], "NormalMatrix")
            for prog in self.objshaderprograms:
                glUseProgram(prog)
                glUniformMatrix4fv(mloc, 1, GL_FALSE, glm.value_ptr(model))
                glUniformMatrix3fv(nloc, 1, GL_FALSE, glm.value_ptr(NM))

    # Reset the projection matrix using the stored projection matrix.
    def resetProjectionMatrix(self):
        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.CubemapShader)
        glUniformMatrix4fv(self.projviewLocCM, 1, GL_FALSE, glm.value_ptr(PV))

        if len(self.objshaderprograms) > 0:
            t = glGetUniformLocation(self.objshaderprograms[0], "PV")
            for prog in self.objshaderprograms:
                glUseProgram(prog)
                glUniformMatrix4fv(t, 1, GL_FALSE, glm.value_ptr(PV))

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size):
        w, h = size
        self.projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        self.resetProjectionMatrix()

    # Set and load the view matrix to the graphics card.
    def setViewMatrix(self):
        if self.cameranum == 0:
            self.viewMatrix = self.sphericalcamera.lookAt()
        else:
            self.viewMatrix = self.yprcamera.lookAt()

        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.CubemapShader)
        glUniformMatrix4fv(self.projviewLocCM, 1, GL_FALSE, glm.value_ptr(PV))

        if len(self.objshaderprograms) > 0:
            t = glGetUniformLocation(self.objshaderprograms[0], "PV")
            for prog in self.objshaderprograms:
                glUseProgram(prog)
                glUniformMatrix4fv(t, 1, GL_FALSE, glm.value_ptr(PV))

        self.LoadEyePosition()

    # Toggle between the two cameras.
    def toggleCamera(self):
        if self.cameranum == 0:
            self.cameranum = 1
        else:
            self.cameranum = 0

    # Toggle the drawing of the axes.
    def toggleAxes(self):
        self.showaxes = not self.showaxes

    # Toggle the drawing of the axes.
    def toggleLight(self):
        self.showlight = not self.showlight

    # Dump screen buffer data to raw pixels and convert to PIL Image object.
    def getScreenImage(self):
        viewport = glGetIntegerv(GL_VIEWPORT)
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(viewport[0], viewport[1], viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (viewport[2], viewport[3]), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image

    # Print out any errors in the OpenGL error queue.
    def printOpenGLErrors(self):
        errCode = glGetError()
        while errCode != GL_NO_ERROR:
            errString = gluErrorString(errCode)
            print("OpenGL Error: ", errString, "\n")
            errCode = glGetError()
