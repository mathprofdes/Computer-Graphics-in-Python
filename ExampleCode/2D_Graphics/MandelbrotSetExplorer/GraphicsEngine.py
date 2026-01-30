#! /usr/bin/env python3
#
# Graphics engine object sets up graphics card programs and data.
# Updates the display and has methods for setting the fractal attributes
# in the fragmant shader.
#
# Don Spickler
# 12/19/2021

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from Shader import *
import pygame
import numpy as np
import ctypes
from PIL import Image
import glm
import random

from Box import *
from Axes2D import *
from Polygon import *


class GraphicsEngine():
    # "Addresses" for OpenGL constructs.
    VAO = 0
    Buffer = 0
    vPosition = 0
    vColor = 1
    mode = GL_FILL
    ScreenBounds = [-1, 1, -1, 1]

    # Scaling limitation on some fractal attributes.
    minScale = 0.00000000001
    maxMaxiter = 10000
    maxBailoutRadius = 1000000
    TitleBarNote = None

    # Constructor
    def __init__(self):
        # Load shaders and compile shader programs.
        try:
            shader = Shader()
            self.shaderProgram = shader.loadShadersFromFile("AspectRatioVert.glsl", "MandelbrotFrag.glsl")
        except Exception as err:
            for i in range(len(err.args)):
                print(err.args[i])
            raise Exception(err)

        glUseProgram(self.shaderProgram)

        self.box = Box()
        self.setProjectionMatrices(pygame.display.get_surface().get_size())

        # Set clear/background color to black.
        glClearColor(0, 0, 0, 1)
        self.setDefaultValues()
        self.loadDefaults()

    # Set the default attribute values for the fractal.
    def setDefaultValues(self):
        self.maxIter = 100
        self.boarderPer = 0.25
        self.center = glm.vec2(0, 0)
        self.scale = 2
        self.smooth = True
        self.doublePre = False
        self.BailoutRad = 10
        self.solidColor = glm.vec4(1, 0, 0, 1)
        self.colorScheme = 1
        self.iterationScale = 2.5
        self.iterationOffset = 0
        self.exponent = 2

    # Load the default attribute values for the fractal to the shader.
    def loadDefaults(self):
        self.setDoublePrecision(self.doublePre)
        self.setSmoothRendering(self.smooth)
        self.setMaxIter(self.maxIter)
        self.setBailoutRadius(self.BailoutRad)
        self.setScaleFactor(self.scale)
        self.loadColorScheme(self.colorScheme)
        self.setBorderFactor(self.boarderPer)
        self.setIterationScale(self.iterationScale)
        self.setIterationOffset(self.iterationOffset)
        self.setCenter()
        self.setExponent(self.exponent)

    # Reset the default attribute values for the fractal and load to the shader.
    def resetFractal(self):
        self.setDefaultValues()
        self.loadDefaults()

    # Set the mode to either single or double precision.
    def setDoublePrecision(self, doublepre):
        glUniform1i(glGetUniformLocation(self.shaderProgram, "doublePrec"), doublepre)
        if doublepre:
            self.TitleBarNote = "Double Precision is on."
        else:
            self.TitleBarNote = "Double Precision is off."

    # Set the mode to either smooth or not smooth rendering.
    def setSmoothRendering(self, smooth):
        glUniform1i(glGetUniformLocation(self.shaderProgram, "smoothRender"), smooth)
        if smooth:
            self.TitleBarNote = "Smooth rendering is on."
        else:
            self.TitleBarNote = "Smooth rendering is off."

    # Toggle smooth rendering.
    def toggleSmooth(self):
        self.smooth = not self.smooth
        self.setSmoothRendering(self.smooth)

    # Toggle double precision.
    def toggleDoublePre(self):
        self.doublePre = not self.doublePre
        self.setDoublePrecision(self.doublePre)

    # Set the maximum iteration used for graphing the fractal.
    def setMaxIter(self, iter):
        if iter > self.maxMaxiter:
            iter = self.maxMaxiter
        elif iter < 10:
            iter = 10

        self.maxIter = iter
        glUniform1i(glGetUniformLocation(self.shaderProgram, "maxiter"), self.maxIter)
        self.TitleBarNote = "Maximum iteration: " + str(self.maxIter)

    # Add to the maximum iteration used for graphing the fractal.
    def addToMaxIter(self, inc):
        self.setMaxIter(self.maxIter + inc)

    # Set the percentage of iterations used for the boarder color.
    def setBorderFactor(self, factor):
        if factor < 0:
            factor = 0
        elif factor > 1:
            factor = 1

        self.boarderPer = factor
        glUniform1f(glGetUniformLocation(self.shaderProgram, "boarderPer"), self.boarderPer)
        self.TitleBarNote = "Boarder Percentage: {:0.2%}".format(1-self.boarderPer)

    # Add to the percentage of iterations used for the boarder color.
    def addToBorderFactor(self, a):
        self.setBorderFactor(self.boarderPer + a)

    # Set the exponent on z for the family to be graphed.
    def setExponent(self, exp):
        self.exponent = exp
        glUniform1i(glGetUniformLocation(self.shaderProgram, "exponent"), exp)
        self.TitleBarNote = "Equation: z^" + str(self.exponent) + " + c"

    # Set the bailout radius used to end the iterations.
    def setBailoutRadius(self, rad):
        if rad < 2:
            rad = 2
        elif rad > self.maxBailoutRadius:
            rad = self.maxBailoutRadius

        self.BailoutRad = rad
        glUniform1f(glGetUniformLocation(self.shaderProgram, "bailoutRad"), rad)
        self.TitleBarNote = "Bailout Radius: {:.2f}".format(self.BailoutRad)

    # Add to the bailout radius used to end the iterations.
    def addToBailoutRadius(self, rad):
        self.setBailoutRadius(self.BailoutRad + rad)

    # Multiply the bailout radius, by the given factor, used to end the iterations.
    def multBailoutRadius(self, rad):
        self.setBailoutRadius(self.BailoutRad * rad)

    # Set the scale factor used for zooming in and out of the image.
    def setScaleFactor(self, scale):
        if scale < self.minScale:
            scale = self.minScale

        self.scale = scale
        glUniform1d(glGetUniformLocation(self.shaderProgram, "scaleD"), scale)
        glUniform1f(glGetUniformLocation(self.shaderProgram, "scale"), scale)
        self.TitleBarNote = "Scale: {:.15f}".format(self.scale)

    # Return the solid color used for some of the color schemes.
    def getSolidColor(self):
        return self.solidColor

    # Set the solid color used for some of the color schemes.
    def setSolidColor(self, col):
        self.solidColor = col
        self.loadColorScheme(self.colorScheme)

    # Set the solid scheme number and load the respective color scheme.
    def setColorScheme(self, num):
        if 1 <= num <= 10:
            self.colorScheme = num
        else:
            self.colorScheme = 1

        self.loadColorScheme(self.colorScheme)

    # Load the color scheme.
    # - 1: Sets the palette to a single color fade in and fade out.  The color can be altered
    #         by the user using the keyboard interface.
    # - 2: Sets the palette to alternating color to black and the color is faded in and out
    #         in the sequence.  The color can be altered by the user using the keyboard interface.
    # - 3: Sets the palette to a repeating ROYGBIV scheme.
    # - 4: Sets the palette to a repeating RGB scheme.
    # - 5: Sets the palette to a repeating KROYGBIV scheme with K = black.
    # - 6: Sets the palette to a repeating RGB scheme with K = black.
    # - 7: Sets the palette to a repeating KRKGKBKW scheme with K = black and W = white.
    # - 8: Sets the palette to a repeating KRYGCBPW scheme.
    # - 9: Sets the palette to a repeating 10 random color scheme.
    # - 10: Sets the palette to a repeating random color scheme with between 5 and 25 colors.

    def loadColorScheme(self, num):
        colorset = []
        if num == 1:
            for i in range(50):
                colorset.append(self.solidColor * (0.02 * i))

            for i in range(50, 100):
                colorset.append(self.solidColor * (0.02 * (100-i)))

            colordata = np.array(colorset).astype(ctypes.c_float)
            glUniform4fv(glGetUniformLocation(self.shaderProgram, "colorSet"), 100, colordata)
        elif num == 2:
            for i in range(50):
                if i % 2 == 1:
                    colorset.append(glm.vec4(0,0,0,1))
                else:
                    colorset.append(self.solidColor * (0.02 * i))

            for i in range(50, 100):
                if i % 2 == 1:
                    colorset.append(glm.vec4(0,0,0,1))
                else:
                    colorset.append(self.solidColor * (0.02 * (100-i)))

            colordata = np.array(colorset).astype(ctypes.c_float)
            glUniform4fv(glGetUniformLocation(self.shaderProgram, "colorSet"), 100, colordata)
        elif 3 <= num <= 10:
            if num == 3:
                colorset.append(glm.vec4(1, 0, 0, 1))
                colorset.append(glm.vec4(1, 0.6, 0, 1))
                colorset.append(glm.vec4(1, 1, 0, 1))
                colorset.append(glm.vec4(0, 1, 0, 1))
                colorset.append(glm.vec4(0, 0, 1, 1))
                colorset.append(glm.vec4(0.75, 0.5, 0.75, 1))
                colorset.append(glm.vec4(0.5, 0.25, .75, 1))
            elif num == 4:
                colorset.append(glm.vec4(1, 0, 0, 1))
                colorset.append(glm.vec4(0, 1, 0, 1))
                colorset.append(glm.vec4(0, 0, 1, 1))
            elif num == 5:
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(1, 0, 0, 1))
                colorset.append(glm.vec4(1, 0.6, 0, 1))
                colorset.append(glm.vec4(1, 1, 0, 1))
                colorset.append(glm.vec4(0, 1, 0, 1))
                colorset.append(glm.vec4(0, 0, 1, 1))
                colorset.append(glm.vec4(0.75, 0.5, 0.75, 1))
                colorset.append(glm.vec4(0.5, 0.25, .75, 1))
            elif num == 6:
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(1, 0, 0, 1))
                colorset.append(glm.vec4(0, 1, 0, 1))
                colorset.append(glm.vec4(0, 0, 1, 1))
            elif num == 7:
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(1, 0, 0, 1))
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(0, 1, 0, 1))
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(0, 0, 1, 1))
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(1, 1, 1, 1))
            elif num == 8:
                colorset.append(glm.vec4(0, 0, 0, 1))
                colorset.append(glm.vec4(1, 0, 0, 1))
                colorset.append(glm.vec4(1, 1, 0, 1))
                colorset.append(glm.vec4(0, 1, 0, 1))
                colorset.append(glm.vec4(0, 1, 1, 1))
                colorset.append(glm.vec4(0, 0, 1, 1))
                colorset.append(glm.vec4(1, 0, 1, 1))
                colorset.append(glm.vec4(1, 1, 1, 1))
            elif num == 9:
                for i in range(10):
                    colorset.append(glm.vec4(random.random(), random.random(), random.random(), 1))
            elif num == 10:
                numcolors = random.randint(5, 25)
                for i in range(numcolors):
                    colorset.append(glm.vec4(random.random(), random.random(), random.random(), 1))

            length = len(colorset)
            colspan = 100.0 / length
            expandedColorSet = []
            for i in range(100):
                col1pos = int(i / colspan)
                col1 = colorset[col1pos % length]
                col2 = colorset[(col1pos+1) % length]
                s = i / colspan - i // colspan
                thiscolor = (1 - s) * col1 + s * col2
                expandedColorSet.append(thiscolor)

            colordata = np.array(expandedColorSet).astype(ctypes.c_float)
            glUniform4fv(glGetUniformLocation(self.shaderProgram, "colorSet"), 100, colordata)

    # Displays the center to the titlebar.
    def displayCenter(self):
        self.TitleBarNote = "Center: ({:.15f}, {:.15f})".format(-self.center.x, -self.center.y)

    # Add to the center of the image.
    def addToCenter(self, x, y):
        self.center.x += x * self.scale
        self.center.y += y * self.scale
        dcenter = glm.dvec2(self.center.x, self.center.y)

        glUniform2dv(glGetUniformLocation(self.shaderProgram, "centerD"), 1, glm.value_ptr(dcenter))
        glUniform2fv(glGetUniformLocation(self.shaderProgram, "center"), 1, glm.value_ptr(self.center))
        self.displayCenter()

    # Set the center of the image using screen coordinates.
    def setCenterBySC(self, x, y):
        self.center.x -= x * self.scale
        self.center.y -= y * self.scale
        dcenter = glm.dvec2(self.center.x, self.center.y)

        glUniform2dv(glGetUniformLocation(self.shaderProgram, "centerD"), 1, glm.value_ptr(dcenter))
        glUniform2fv(glGetUniformLocation(self.shaderProgram, "center"), 1, glm.value_ptr(self.center))
        self.displayCenter()

    # Reset the center by the values of self.center.x and self.center.y
    def setCenter(self):
        dcenter = glm.dvec2(self.center.x, self.center.y)
        glUniform2dv(glGetUniformLocation(self.shaderProgram, "centerD"), 1, glm.value_ptr(dcenter))
        glUniform2fv(glGetUniformLocation(self.shaderProgram, "center"), 1, glm.value_ptr(self.center))
        self.displayCenter()

    # Multiply the scale factor used for zooming.
    def multScaleFactor(self, f):
        self.scale *= f

        if self.scale < self.minScale:
            self.scale = self.minScale

        glUniform1d(glGetUniformLocation(self.shaderProgram, "scaleD"), self.scale)
        glUniform1f(glGetUniformLocation(self.shaderProgram, "scale"), self.scale)
        self.TitleBarNote = "Scale: {:.15f}".format(self.scale)

    # Set the iteration scaling to lengthen or shorten the color cycle.
    def setIterationScale(self, iterscale):
        if iterscale < 0.01:
            iterscale = 0.01
        elif (iterscale > 100):
            iterscale = 100

        self.iterationScale = iterscale
        glUniform1f(glGetUniformLocation(self.shaderProgram, "iterationScale"), self.iterationScale)
        self.TitleBarNote = "Iteration Scale: {:.2f}".format(self.iterationScale)

    # Multiplies the iteration scaling to lengthen or shorten the color cycle.
    def multIterationScale(self, mult):
        newiterscale = self.iterationScale * mult
        self.setIterationScale(newiterscale)

    # Set the iteration offset used for the color cycle.
    def setIterationOffset(self, offset):
        if offset < 0:
            offset = 0

        if offset > 100:
            offset = 100

        self.iterationOffset = offset
        glUniform1f(glGetUniformLocation(self.shaderProgram, "colorsOffset"), self.iterationOffset)
        self.TitleBarNote = "Iteration Offset: {:.1f}".format(self.iterationOffset)

    # Add to the iteration offset used for the color cycle.
    def addIterationOffset(self, addOffset):
        self.setIterationOffset(self.iterationOffset + addOffset)

    # Turn on shader, clear screen, draw axes and boxes, swap display buffers.
    def update(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        self.box.draw()
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

    # Sets the projection matrix.
    def setProjectionMatrices(self, size):
        self.setProjectionMatrix(size, self.shaderProgram, "Projection")

    # Set and load the projection matrix to the graphics card.
    def setProjectionMatrix(self, size, prog, name):
        w, h = size

        # if width > height create a matrix to map scene to [-a, a] X [-1, 1]
        # if height > width create a matrix to map scene to [-1, 1] X [-a, a]
        # glm.ortho creates the scaling matrix.
        if w > h:
            aspratio = w / h
            ProjectionMatrix = glm.ortho(-aspratio, aspratio, -1, 1)
            self.ScreenBounds = [-aspratio, aspratio, -1, 1]
        else:
            aspratio = h / w
            ProjectionMatrix = glm.ortho(-1, 1, -aspratio, aspratio)
            self.ScreenBounds = [-1, 1, -aspratio, aspratio]

        # Load Projection Matrix to the projection matrix in the shader.
        glUseProgram(prog)
        projLoc = glGetUniformLocation(prog, name)
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(ProjectionMatrix))

        self.box.setHeight(2*self.ScreenBounds[3])
        self.box.setWidth(2 * self.ScreenBounds[1])

    # Get the real world screen bounds.
    def getScreenBounds(self):
        return self.ScreenBounds

    # Get the current viewport dimensions.
    def getViewport(self):
        return glGetIntegerv(GL_VIEWPORT)

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

    # Return the fractal information of the current image as a string.
    def getFractalInformation(self):
        infostring = ""
        infostring += "Equation: z^" + str(self.exponent) + " + c \n"
        infostring += "Center: ({:.15f}, {:.15f}) \n".format(-self.center.x, -self.center.y)

        Width = self.scale * (self.ScreenBounds[1] - self.ScreenBounds[0])
        Height = self.scale * (self.ScreenBounds[3] - self.ScreenBounds[2])

        realLeft = -self.center.x - Width / 2
        realRight = -self.center.x + Width / 2
        realTop = -self.center.y + Height / 2
        realBottom = -self.center.y - Height / 2

        infostring += "Horizontal Range: [{:.15f}, {:.15f}] \n".format(realLeft, realRight)
        infostring += "Vertical Range: [{:.15f}, {:.15f}] \n".format(realBottom, realTop)
        infostring += "Maximum Iteration: {} \n".format(self.maxIter)

        return infostring
