#! /usr/bin/env python3
#
# This program is the hello world of graphics.  Simply getting a couple
# triangles on the screen.
#
# Don Spickler
# 11/20/2021

from OpenGL.GL import *
from OpenGL.GL.shaders import *
import pygame
from pygame.locals import *
import numpy as np
import ctypes

# Program setup information
ProgramName = "Hello World of Graphics"
Width = 800
Height = 600

# "Addresses" for OpenGL constructs.
VAO = 0
Buffer = 0
vPosition = 0
vColor = 1
shaderProgram = -1

# Data for the two triangles to be displayed. Format is (r, g, b, x, y)
# for each vertex.
data = [[1.00, 0.00, 0.00, -0.90, -0.90], # Triangle 1
    [0.00, 1.00, 0.00, 0.85, -0.90],
    [0.00, 0.00, 1.00, -0.90, 0.85],
    [0.04, 0.04, 0.04, 0.90, -0.85],  # Triangle 2
    [0.40, 0.40, 0.40, 0.90, 0.90],
    [1.00, 1.00, 1.00, -0.85, 0.90]]

def exitProgram():
    pygame.quit()
    exit()

if __name__ == '__main__':
    # Initialize pygame.
    pygame.init()
    pygame.display.set_mode((Width, Height), DOUBLEBUF | OPENGL | RESIZABLE | HWSURFACE)
    pygame.display.set_caption(ProgramName)

    # Load and compile shaders.
    vertexShader = compileShader(open("PassThroughVert.glsl", 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = compileShader(open("PassThroughFrag.glsl", 'r').read(), GL_FRAGMENT_SHADER)

    # Attach and link shaders into a program.
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)
    glLinkProgram(shaderProgram)

    # Create the Vertex Array Object and bind.
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Create the Array Buffer and bind.
    Buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, Buffer)

    # Load the data to the graphics card using numpy to set the data type.
    gpudata = np.array(data).astype(ctypes.c_float)
    glBufferData(GL_ARRAY_BUFFER, gpudata.ravel(), GL_STATIC_DRAW)

    # Set the data attributes so the card knows how to interpret the data.
    floatsize = ctypes.sizeof(ctypes.c_float)
    glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_TRUE, 5 * floatsize, ctypes.c_void_p(0))
    glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 5 * floatsize, ctypes.c_void_p(3 * floatsize))

    # Enable the arrays and set the "positions" for the shaders.
    glEnableVertexAttribArray(vPosition)
    glEnableVertexAttribArray(vColor)

    # Start the pygame event loop.
    while True:
        # process events from pygame event queue. X or escape to close the program.
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                exitProgram()

        # Turn on shader, clear screen, draw triangles, swap display buffers.
        glUseProgram(shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, len(data))
        pygame.display.flip()
