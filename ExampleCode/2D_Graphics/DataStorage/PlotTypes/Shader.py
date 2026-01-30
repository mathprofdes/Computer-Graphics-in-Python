#! /usr/bin/env python3
#
# Shader object that will load and compile vertex and fragment shaders
# either from files or from strings.
#
# Don Spickler
# 11/20/2021

from OpenGL.GL import *
from OpenGL.GL.shaders import *

class Shader():
    lasterror = ""

    # Constructor
    def __init__(self):
        """No need to do anything here."""

    # Loads shaders as strings, compiles and links the program and returns
    # the shader program address.
    def loadShaders(self, vert, frag):
        vertexShader = compileShader(vert, GL_VERTEX_SHADER)
        compileSuccess = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
        if not compileSuccess:
            # retrieve error message
            self.lasterror = glGetShaderInfoLog(vertexShader)
            # free memory used to store shader program
            glDeleteShader(vertexShader)
            # raise exception
            raise Exception(self.lasterror)

        fragmentShader = compileShader(frag, GL_FRAGMENT_SHADER)
        compileSuccess = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
        if not compileSuccess:
            self.lasterror = glGetShaderInfoLog(fragmentShader)
            glDeleteShader(fragmentShader)
            raise Exception(self.lasterror)

        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glLinkProgram(shaderProgram)

        linkSuccess = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
        if not linkSuccess:
            self.lasterror = glGetProgramInfoLog(shaderProgram)
            glDeleteProgram(shaderProgram)
            raise Exception(self.lasterror)

        return shaderProgram

    # Loads shaders from files and calls the compiler method to compile and link the
    # program. Returns the shader program address.
    def loadShadersFromFile(self, vert, frag):
        return self.loadShaders(open(vert, 'r').read(), open(frag, 'r').read())

    # Gets last error in the compilation.
    def getLastError(self):
        return self.lasterror

    # Clears the last error.
    def clearLastError(self):
        self.lasterror = ""

    # Prints out the last error list.
    def printLastError(self):
        for i in range(len(self.lasterror.args)):
            print(self.lasterror.args[i])
