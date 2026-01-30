#! /usr/bin/env python3
#
# Graphics engine object.
#
# Don Spickler
# 3/25/2022

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm

from Cube import *
from Sphere import *
from Torus import *
from Trefoil import *
from Plane import *
from SimplePlane import *
from HeightMap import *
from ModelData import *
from Axes3D import *
from SphericalCamera import *
from YPRCamera import *
from Light import *
from Material import *


class GraphicsEngine():
    mode = GL_FILL
    shaderProgram = -1
    cameranum = 0
    displayobjmode = 1
    showaxes = True
    showlight = True
    projectionMatrix = glm.mat4(1)
    viewMatrix = glm.mat4(1)

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.AxesShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                         "Shaders/PassThroughFrag.glsl")
            self.TextureShader = shader.loadShadersFromFile("Shaders/VertexShaderLightingTexture.glsl",
                                                            "Shaders/PhongMultipleLightsAndTexture.glsl")
            self.ConstColorShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3D.glsl",
                                                               "Shaders/ConstantColorFrag.glsl")

        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the locations of some of the uniform variables.
        glUseProgram(self.AxesShader)
        self.projviewLocAxes = glGetUniformLocation(self.AxesShader, "ProjView")
        self.modelLocAxes = glGetUniformLocation(self.AxesShader, "Model")

        glUseProgram(self.TextureShader)
        self.projviewLocPhong = glGetUniformLocation(self.TextureShader, "PV")
        self.modelLocPhong = glGetUniformLocation(self.TextureShader, "Model")
        self.normalMatrixLocPhong = glGetUniformLocation(self.TextureShader, "NormalMatrix")
        GlobalAmbient = glm.vec4(0.2, 0.2, 0.2, 1)
        glUniform4fv(glGetUniformLocation(self.TextureShader, "GlobalAmbient"),
                     1, glm.value_ptr(GlobalAmbient))
        glUniform1i(glGetUniformLocation(self.TextureShader, "numLights"), 3)
        self.texLocRender = glGetUniformLocation(self.TextureShader, "tex1")
        self.texYNLocRender = glGetUniformLocation(self.TextureShader, "useTexture")
        self.texTransform = glGetUniformLocation(self.TextureShader, "textrans")

        glUseProgram(self.ConstColorShader)
        self.projviewLocConst = glGetUniformLocation(self.ConstColorShader, "ProjView")
        self.modelLocConst = glGetUniformLocation(self.ConstColorShader, "Model")
        lightcol = glm.vec4(1, 1, 0, 1)
        glUniform4fv(glGetUniformLocation(self.ConstColorShader, "ConstantColor"),
                     1, glm.value_ptr(lightcol))

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
        self.cube = Cube()
        self.lightsphere = Sphere(0.25, 10, 10)
        self.torus = Torus()
        self.trefiol = Trefoil()
        self.teapot = ModelData("Data/teapotDataTNV.txt", "TNV")
        self.simpleplane = SimplePlane()

        # Load Lights and Materials
        self.mat = Material()
        self.mat.WhitePlastic()
        self.mat.LoadMaterial(self.TextureShader, "Mat")

        self.lights = []
        self.lights.append(Light())
        self.lightcamera = SphericalCamera(50, 45, 45)

        # Set light positions.  Light 0 will ne locked to the lightcamera object.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)

        # Load in textures.
        self.texID1 = self.loadTexture("Images/cat003.png")
        self.texID2 = self.loadTexture("Images/metal024.bmp")
        self.texID3 = self.loadTexture("Images/oakH.jpg")
        self.texID4 = self.loadTexture("Images/amazaque.bmp")
        self.texID5 = self.loadTexture("Images/stucco001.jpg")
        self.texID6 = self.loadTexture("Images/knotted.jpg")
        self.texID7 = self.loadTexture("Images/ash.jpg")

        # Link the texture ID to different texture units.
        glActiveTexture(GL_TEXTURE0 + self.texID1)
        glBindTexture(GL_TEXTURE_2D, self.texID1)

        glActiveTexture(GL_TEXTURE0 + self.texID2)
        glBindTexture(GL_TEXTURE_2D, self.texID2)

        glActiveTexture(GL_TEXTURE0 + self.texID3)
        glBindTexture(GL_TEXTURE_2D, self.texID3)

        glActiveTexture(GL_TEXTURE0 + self.texID4)
        glBindTexture(GL_TEXTURE_2D, self.texID4)

        glActiveTexture(GL_TEXTURE0 + self.texID5)
        glBindTexture(GL_TEXTURE_2D, self.texID5)

        glActiveTexture(GL_TEXTURE0 + self.texID6)
        glBindTexture(GL_TEXTURE_2D, self.texID6)

        glActiveTexture(GL_TEXTURE0 + self.texID7)
        glBindTexture(GL_TEXTURE_2D, self.texID7)

        glUniform1i(self.texLocRender, self.texID3)
        glUniform1i(self.texYNLocRender, True)

        textureMat = glm.mat4(3)
        glUniformMatrix4fv(self.texTransform, 1, GL_FALSE, glm.value_ptr(textureMat))

    def loadTexture(self, filename):
        teximg = Image.open(filename)
        teximg = teximg.convert('RGBA')
        teximg = teximg.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(teximg.getdata()), np.int8)

        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        return texID

    def renderScene(self):
        textureMat = glm.mat4(1)
        glUniformMatrix4fv(self.texTransform, 1, GL_FALSE, glm.value_ptr(textureMat))
        glUniform1i(self.texLocRender, self.texID1)
        model = glm.translate(glm.vec3(15, 2.5, 10))
        model = glm.scale(model, glm.vec3(5))
        self.LoadMatrices(model)
        self.cube.draw()

        model = glm.translate(glm.vec3(-10, 5, 3))
        model = glm.rotate(model, glm.radians(30), glm.vec3(1, 1, 1))
        model = glm.scale(model, glm.vec3(5))
        self.LoadMatrices(model)
        self.cube.draw()

        model = glm.translate(glm.vec3(7, 6, -10))
        model = glm.scale(model, glm.vec3(3))
        self.LoadMatrices(model)
        glUniform1i(self.texLocRender, self.texID4)
        self.torus.draw()


        model = glm.translate(glm.vec3(-10, 5, -15))
        model = glm.scale(model, glm.vec3(5))
        self.LoadMatrices(model)
        glUniform1i(self.texLocRender, self.texID2)
        self.teapot.draw()


        textureMat = glm.scale(glm.vec3(50, 3, 1))
        glUniformMatrix4fv(self.texTransform, 1, GL_FALSE, glm.value_ptr(textureMat))
        model = glm.translate(glm.vec3(0, 6, 15))
        model = glm.scale(model, glm.vec3(3))
        self.LoadMatrices(model)
        glUniform1i(self.texLocRender, self.texID7)
        self.trefiol.draw()

        # Room
        # Floor
        textureMat = glm.mat4(10)
        glUniformMatrix4fv(self.texTransform, 1, GL_FALSE, glm.value_ptr(textureMat))
        glUniform1i(self.texLocRender, self.texID3)
        model = glm.scale(glm.vec3(50))
        model = glm.rotate(model, -np.pi / 2, glm.vec3(1, 0, 0))
        self.LoadMatrices(model)
        self.simpleplane.draw()

        # Ceiling
        glUniform1i(self.texLocRender, self.texID6)
        model = glm.translate(glm.vec3(0, 50, 0))
        model = glm.scale(model, glm.vec3(50))
        model = glm.rotate(model, np.pi / 2, glm.vec3(1, 0, 0))
        self.LoadMatrices(model)
        self.simpleplane.draw()

        # Walls
        glUniform1i(self.texLocRender, self.texID5)
        model = glm.translate(glm.vec3(0, 50, -50))
        model = glm.scale(model, glm.vec3(50))
        self.LoadMatrices(model)
        self.simpleplane.draw()

        glUniform1i(self.texLocRender, self.texID5)
        model = glm.translate(glm.vec3(0, 50, 50))
        model = glm.rotate(model, glm.radians(180), glm.vec3(0, 1, 0))
        model = glm.scale(model, glm.vec3(50))
        self.LoadMatrices(model)
        self.simpleplane.draw()

        glUniform1i(self.texLocRender, self.texID5)
        model = glm.translate(glm.vec3(50, 50, 0))
        model = glm.rotate(model, glm.radians(-90), glm.vec3(0, 1, 0))
        model = glm.scale(model, glm.vec3(50))
        self.LoadMatrices(model)
        self.simpleplane.draw()

        glUniform1i(self.texLocRender, self.texID5)
        model = glm.translate(glm.vec3(-50, 50, 0))
        model = glm.rotate(model, glm.radians(90), glm.vec3(0, 1, 0))
        model = glm.scale(model, glm.vec3(50))
        self.LoadMatrices(model)
        self.simpleplane.draw()

    # Turn on shader, clear screen, draw axes, cubes, or box.
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

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
            lightobjmodel = glm.translate(glm.vec3(self.lights[0].position))
            glUniformMatrix4fv(self.modelLocConst, 1, GL_FALSE, glm.value_ptr(lightobjmodel))
            self.lightsphere.draw()

        # Draw remainder of scene.
        glUseProgram(self.TextureShader)

        # Set the light position from the light "camera". Load to shader.
        self.lights[0].position = glm.vec4(self.lightcamera.getPosition(), 1)
        self.lights[0].LoadLight(self.TextureShader, "Lt[0]")

        # Get the position of the camera and load to the shader.
        eye = glm.vec3(0, 0, 0)
        if self.cameranum == 0:
            eye = self.sphericalcamera.getPosition()
        elif self.cameranum == 1:
            eye = self.yprcamera.getPosition()

        glUniform3fv(glGetUniformLocation(self.TextureShader, "eye"), 1, glm.value_ptr(eye))

        self.renderScene()

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

    # Loads the model matrix, calculates the normal matrix, (M^(-1))^T, and loads
    # it to the shader.  Function assumes that the lighting shader program is active.
    def LoadMatrices(self, model):
        glUniformMatrix4fv(self.modelLocPhong, 1, GL_FALSE, glm.value_ptr(model))
        NM = glm.inverse(glm.transpose(glm.mat3(model)))
        glUniformMatrix3fv(self.normalMatrixLocPhong, 1, GL_FALSE, glm.value_ptr(NM))

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size):
        w, h = size
        self.projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.TextureShader)
        glUniformMatrix4fv(self.projviewLocPhong, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))

    # Set and load the view matrix to the graphics card.
    def setViewMatrix(self):
        if self.cameranum == 0:
            self.viewMatrix = self.sphericalcamera.lookAt()
        else:
            self.viewMatrix = self.yprcamera.lookAt()

        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.TextureShader)
        glUniformMatrix4fv(self.projviewLocPhong, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.ConstColorShader)
        glUniformMatrix4fv(self.projviewLocConst, 1, GL_FALSE, glm.value_ptr(PV))

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
