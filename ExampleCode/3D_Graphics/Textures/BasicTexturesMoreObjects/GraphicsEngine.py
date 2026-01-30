#! /usr/bin/env python3
#
# Graphics engine object.
#
# Don Spickler
# 1/8/2022

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
            self.TextureShader = shader.loadShadersFromFile("Shaders/VertexShaderBasic3DTexture.glsl",
                                                            "Shaders/SimpleTexture.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Turn on program, get the locations of some of the uniform variables.
        glUseProgram(self.AxesShader)
        self.projviewLocAxes = glGetUniformLocation(self.AxesShader, "ProjView")
        self.modelLocAxes = glGetUniformLocation(self.AxesShader, "Model")

        glUseProgram(self.TextureShader)
        self.projviewLocRender = glGetUniformLocation(self.TextureShader, "ProjView")
        self.modelLocRender = glGetUniformLocation(self.TextureShader, "Model")
        self.texLocRender = glGetUniformLocation(self.TextureShader, "tex1")
        self.texYNLocRender = glGetUniformLocation(self.TextureShader, "useTexture")

        self.setProjectionMatrix(pygame.display.get_surface().get_size())

        # Set clear/background color to black and turn on depth testing.
        glClearColor(0, 0, 0, 1)
        # glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)

        # Create the cameras.
        self.sphericalcamera = SphericalCamera(30, 60, 45)
        self.yprcamera = YPRCamera()
        self.setViewMatrix()

        # Create and load the objects.
        self.axes = Axes3D()
        self.cube = Cube()

        self.sphere = Sphere()
        # self.sphere = Sphere(1, 20, 20, glm.radians(45), glm.radians(200), glm.radians(-45), glm.radians(45))

        self.lightsphere = Sphere(0.25, 10, 10)

        self.torus = Torus()
        # self.torus.set(1.5, 2, 50, 20)

        self.trefiol = Trefoil()

        self.plane = Plane()
        # self.plane.set(1, 1, 1, 1)

        # img = Image.open("Images/map001.png")
        # img = Image.open("Images/map002.png")
        # img = Image.open("Images/cat001.png")
        # img = Image.open("Images/cat002.png")
        # img = Image.open("Images/hm001.png")
        img = Image.open("Images/hm002.png")
        # img = Image.open("Images/moon.jpg")
        # img = Image.open("Images/us.jpg")
        # img = Image.open("Images/volcano.png")

        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        self.heightmap = HeightMap(img, 10, 10, 2, 100, 100)

        self.teapot = ModelData("Data/teapotDataTNV.txt", "TNV")

        self.simpleplane = SimplePlane()

        # teximg = Image.open("Images/cat001.png")
        # teximg = Image.open("Images/cat002.png")
        teximg = Image.open("Images/cat003.png")
        # teximg = Image.open("Images/cat004.png")
        # teximg = Image.open("Images/amazaque.bmp")
        # teximg = Image.open("Images/lrock023.bmp")
        # teximg = Image.open("Images/misc026.bmp")
        # teximg = Image.open("Images/misc107.bmp")
        # teximg = Image.open("Images/misc151.bmp")
        # teximg = Image.open("Images/misc152.bmp")
        # teximg = Image.open("Images/Repeat-brick.jpg")

        teximg = teximg.convert('RGBA')
        teximg = teximg.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(teximg.getdata()), np.int8)

        self.texID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, teximg.width, teximg.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glUniform1i(self.texLocRender, 0)
        glUniform1i(self.texYNLocRender, True)

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

        # Draw remainder of scene.
        glUseProgram(self.TextureShader)

        # Draw selected objects with appropriate transformations.
        if self.displayobjmode == 1:
            for i in range(-10, 11, 4):
                for j in range(-10, 11, 4):
                    for k in range(-10, 11, 4):
                        model = glm.translate(glm.vec3(i, j, k))
                        self.loadModelMatrix(model)
                        self.cube.draw()
        elif self.displayobjmode == 2:
            model = glm.scale(glm.vec3(10))
            self.loadModelMatrix(model)
            self.cube.draw()
        elif self.displayobjmode == 3:
            model = glm.scale(glm.vec3(5))
            self.loadModelMatrix(model)
            self.sphere.draw()
        elif self.displayobjmode == 4:
            model = glm.scale(glm.vec3(5))
            model = glm.rotate(model, np.pi / 2, glm.vec3(1, 0, 0))
            self.loadModelMatrix(model)
            self.torus.draw()
        elif self.displayobjmode == 5:
            model = glm.scale(glm.vec3(3))
            self.loadModelMatrix(model)
            self.trefiol.draw()
        elif self.displayobjmode == 6:
            model = glm.scale(glm.vec3(10))
            self.loadModelMatrix(model)
            self.plane.draw()
        elif self.displayobjmode == 7:
            model = glm.scale(glm.vec3(3))
            model = glm.rotate(model, -np.pi / 2, glm.vec3(1, 0, 0))
            self.loadModelMatrix(model)
            self.heightmap.draw()
        elif self.displayobjmode == 8:
            model = glm.scale(glm.vec3(10))
            self.loadModelMatrix(model)
            self.teapot.draw()
        elif self.displayobjmode == 9:
            model = glm.scale(glm.vec3(10))
            self.loadModelMatrix(model)
            self.simpleplane.draw()

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

    # Load the model matrix to the texture shader.
    def loadModelMatrix(self, model):
        glUseProgram(self.TextureShader)
        glUniformMatrix4fv(self.modelLocRender, 1, GL_FALSE, glm.value_ptr(model))

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size):
        w, h = size
        self.projectionMatrix = glm.perspective(glm.radians(50.0), w / h, 0.01, 500.0)
        PV = self.projectionMatrix * self.viewMatrix
        glUseProgram(self.AxesShader)
        glUniformMatrix4fv(self.projviewLocAxes, 1, GL_FALSE, glm.value_ptr(PV))
        glUseProgram(self.TextureShader)
        glUniformMatrix4fv(self.projviewLocRender, 1, GL_FALSE, glm.value_ptr(PV))

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
        glUniformMatrix4fv(self.projviewLocRender, 1, GL_FALSE, glm.value_ptr(PV))

    # Toggle between the two cameras.
    def toggleCamera(self):
        if self.cameranum == 0:
            self.cameranum = 1
        else:
            self.cameranum = 0

    # Toggle the drawing of the axes.
    def toggleAxes(self):
        self.showaxes = not self.showaxes

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
