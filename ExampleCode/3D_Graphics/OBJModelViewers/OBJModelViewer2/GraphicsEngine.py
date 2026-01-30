#! /usr/bin/env python3

"""
Graphics Engine

This version uses only one shader for the model, loaded in the graphics engine.
Material and texture uniform locations are sent to the model class.
Matrix loading and lighting are controlled by the graphics engine.
Material and texture loading is controlled by the model class.

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
            self.ModelShader = self.shader.loadShadersFromFile("Shaders/OBJModelVert.glsl",
                                                               "Shaders/OBJModelFrag.glsl")
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

        glUseProgram(self.ModelShader)
        self.projviewLocModel = glGetUniformLocation(self.ModelShader, "PV")
        self.modelLocModel = glGetUniformLocation(self.ModelShader, "Model")
        self.normalLocModel = glGetUniformLocation(self.ModelShader, "NormalMatrix")

        # Locations for uniforms that the model will need.
        self.mataLocModel = glGetUniformLocation(self.ModelShader, "Mat.ambient")
        self.matdLocModel = glGetUniformLocation(self.ModelShader, "Mat.diffuse")
        self.matsLocModel = glGetUniformLocation(self.ModelShader, "Mat.specular")
        self.mateLocModel = glGetUniformLocation(self.ModelShader, "Mat.emission")
        self.matfLocModel = glGetUniformLocation(self.ModelShader, "Mat.shininess")
        self.atexLocModel = glGetUniformLocation(self.ModelShader, "atex")
        self.dtexLocModel = glGetUniformLocation(self.ModelShader, "dtex")
        self.stexLocModel = glGetUniformLocation(self.ModelShader, "stex")
        self.useatexLocModel = glGetUniformLocation(self.ModelShader, "useATex")
        self.usedtexLocModel = glGetUniformLocation(self.ModelShader, "useDTex")
        self.usestexLocModel = glGetUniformLocation(self.ModelShader, "useSTex")

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

        # self.CubeMapTexId = self.generateCubemapFromSkybox(SkyboxImageFile)

        # Make sure that other texture units do not overlap with these.
        glActiveTexture(GL_TEXTURE1)  # Material Ambient Texture
        glActiveTexture(GL_TEXTURE2)  # Material Diffuse Texture
        glActiveTexture(GL_TEXTURE3)  # Material Specular Texture

        glUseProgram(self.ModelShader)
        glUniform1i(glGetUniformLocation(self.ModelShader, "atex"), 1)
        glUniform1i(glGetUniformLocation(self.ModelShader, "dtex"), 2)
        glUniform1i(glGetUniformLocation(self.ModelShader, "stex"), 3)

        self.LoadMatrices(glm.scale(glm.vec3(3)))

        self.wfmodel = OBJModel(self.ModelShader, self.mataLocModel, self.matdLocModel, self.matsLocModel,
                                self.mateLocModel, self.matfLocModel, 1, 2, 3, self.useatexLocModel,
                                self.usedtexLocModel, self.usestexLocModel)

    # Load a texture object, assign it to an active texture and set its attributes.
    def loadTexture(self, path, filename):
        texturefilename = path + filename
        img = Image.open(texturefilename).convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.asarray(img)
        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        return texID

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
        glUseProgram(self.ModelShader)
        if self.wfmodel:
            self.wfmodel.draw()

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

        glUseProgram(self.ModelShader)
        glUniform3fv(glGetUniformLocation(self.ModelShader, "eye"), 1, glm.value_ptr(eye))

    # Load the light object information to all obj shaders, for lighting calculations.
    def LoadLights(self):
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        glUseProgram(self.ModelShader)
        glUniform1i(glGetUniformLocation(self.ModelShader, "numLights"), len(self.lights))
        for i in range(len(self.lights)):
            self.lights[i].LoadLight(self.ModelShader, "Lt[" + str(i) + "]")

    # Load the position of the movable light.
    def LoadMovingLight(self):
        glUseProgram(self.ModelShader)
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        t = glGetUniformLocation(self.ModelShader, "Lt[0].position")
        glUniform4fv(t, 1, glm.value_ptr(self.lights[0].position))

    # Loads the model matrix, calculates the normal matrix, (M^(-1))^T, and loads
    # it to the shader.  Function assumes that the lighting shader program is active.
    def LoadMatrices(self, model):
        NM = glm.inverse(glm.transpose(glm.mat3(model)))
        glUseProgram(self.ModelShader)
        glUniformMatrix4fv(self.modelLocModel, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix3fv(self.normalLocModel, 1, GL_FALSE, glm.value_ptr(NM))

    # Reset the projection matrix using the stored projection matrix.
    def resetProjectionMatrix(self):
        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.CubemapShader)
        glUniformMatrix4fv(self.projviewLocCM, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ModelShader)
        glUniformMatrix4fv(self.projviewLocModel, 1, GL_FALSE, glm.value_ptr(PV))

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
        glUseProgram(self.ModelShader)
        glUniformMatrix4fv(self.projviewLocModel, 1, GL_FALSE, glm.value_ptr(PV))

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
