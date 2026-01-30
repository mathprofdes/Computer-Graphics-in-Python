#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for mode changes and screen shots.
#
# Don Spickler
# 12/2/2021

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import numpy as np
import ctypes
from PIL import Image
from Box import *
from PointSet import *


class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1

    # Engine settings.
    mode = GL_FILL
    shaderProgram = -1
    plotstyle = 1
    drawset = 1

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("PassThroughVert.glsl", "PassThroughFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)

        # Create set 1 of two parallel lines of 10 points
        self.set1 = PointSet()

        for i in range(1, 11):
            self.set1.add([-1.1 + i / 5, 0.9, 0, 1], [1 - i / 10, i / 10, 0, 1])
            self.set1.add([-1.1 + i / 5, -0.9, 0, 1], [1 - i / 10, i / 10, 0, 1])

        # Create set 2 of points in a circle.
        self.set2 = PointSet()
        vertexCount = 25
        for i in range(1, vertexCount + 1):
            self.set2.add([0.9 * np.cos(2 * np.pi * i / vertexCount), 0.9 * np.sin(2 * np.pi * i / vertexCount), 0, 1],
                          [1 - i / vertexCount, i / vertexCount, 0, 1])

        self.set1.LoadDataToGraphicsCard()
        self.set2.LoadDataToGraphicsCard()

    # Turn on shader, clear screen, set modes, draw.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)

        plotmode = GL_POINTS
        if self.plotstyle == 1:
            plotmode = GL_POINTS
        elif self.plotstyle == 2:
            plotmode = GL_LINES
        elif self.plotstyle == 3:
            plotmode = GL_LINE_STRIP
        elif self.plotstyle == 4:
            plotmode = GL_LINE_LOOP
        elif self.plotstyle == 5:
            plotmode = GL_TRIANGLES
        elif self.plotstyle == 6:
            plotmode = GL_TRIANGLE_STRIP
        elif self.plotstyle == 7:
            plotmode = GL_TRIANGLE_FAN

        if self.drawset == 1:
            self.set1.draw(plotmode)
        else:
            self.set2.draw(plotmode)

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

    # Get and print out lne and point data.
    def printInfo(self):
        info = glGetFloat(GL_POINT_SIZE)
        print("GL_POINT_SIZE = ", info)

        info = glGetFloatv(GL_POINT_SIZE_RANGE)
        print("GL_POINT_SIZE_RANGE = ", info[0], " to ", info[1])

        info = glGetFloat(GL_POINT_SIZE_GRANULARITY)
        print("GL_POINT_SIZE_GRANULARITY = ", info)

        info = glGetFloat(GL_LINE_WIDTH)
        print("GL_LINE_WIDTH = ", info)

        info = glGetFloatv(GL_LINE_WIDTH_RANGE)
        print("GL_LINE_WIDTH_RANGE = ", info[0], " to ", info[1])

        info = glGetFloat(GL_LINE_WIDTH_GRANULARITY)
        print("GL_LINE_WIDTH_GRANULARITY = ", info)
        print()

    # Adjust the point size by ps times the point granularity.
    def adjustPointSize(self, ps):
        ptsize = glGetFloat(GL_POINT_SIZE)
        ptgran = glGetFloat(GL_POINT_SIZE_GRANULARITY)
        range = glGetFloatv(GL_POINT_SIZE_RANGE)

        newsize = ptsize + ps * ptgran

        if (newsize < range[0]):
            newsize = range[0]

        if (newsize > range[1]):
            newsize = range[1]

        glPointSize(newsize)

    # Adjust the line width by lw times the line width granularity.
    def adjustLineWidth(self, lw):
        linewd = glGetFloat(GL_LINE_WIDTH)
        linegran = glGetFloat(GL_LINE_WIDTH_GRANULARITY)
        range = glGetFloatv(GL_LINE_WIDTH_RANGE)

        newsize = linewd + lw * linegran

        if (newsize < range[0]):
            newsize = range[0]

        if (newsize > range[1]):
            newsize = range[1]

        glLineWidth(newsize)
