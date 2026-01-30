#! /usr/bin/env python3
#
# Simple program to create an OpenGL Context through PyGame and extract
# the max version of OpenGL supported by the graphics card and drivers
# as well as the type of card and the vender of the card.
#
# Don Spickler
# 11/20/2021

import pygame
from pygame.locals import *
from OpenGL.GL import *

if __name__ == '__main__':
# Initialize pygame.
    pygame.init()
    pygame.display.set_mode([100, 100], OPENGL)

# Get card information and display in console.
    print()
    print("Version  = ", glGetString(GL_VERSION).decode('utf-8'))
    print("Vender   = ", glGetString(GL_VENDOR).decode('utf-8'))
    print("Renderer = ", glGetString(GL_RENDERER).decode('utf-8'))
