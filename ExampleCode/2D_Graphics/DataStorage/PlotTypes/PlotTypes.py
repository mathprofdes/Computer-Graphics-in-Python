#! /usr/bin/env python3
#
# This program is the hello world of graphics.  Simply getting a couple
# triangles on the screen.  This version adds in some standard user
# interface features and breaks up the program into a better structure.
#
# Don Spickler
# 12/1/2021

import pygame
from pygame.locals import *
import time
from OpenGL.GL import *
from GraphicsEngine import *
from UI import *

# Program setup information
ProgramName = "Plot Types"
maxfps = 60
minMajor = 3
minMinor = 3
Width = 800
Height = 600

# Shut down pygame and end the program.
def exitProgram():
    pygame.quit()
    exit()

# Test card supported version with desired version for the program.
def getOGLVersionAcceptable():
    versionok = True
    major = glGetIntegerv(GL_MAJOR_VERSION)
    minor = glGetIntegerv(GL_MINOR_VERSION)
    if (major < minMajor):
        versionok = False
    elif (major == minMajor and minor < minMinor):
        versionok = False
    return versionok

if __name__ == '__main__':
    pygame.init()

    # Add a user-defined event to update the PFS in the titlebar.
    UPDATE_FPS = USEREVENT + 1
    pygame.time.set_timer(UPDATE_FPS, 1000)

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                    pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

    pygame.display.set_mode((Width, Height), DOUBLEBUF | OPENGL | RESIZABLE | HWSURFACE)
    pygame.display.set_caption(ProgramName)

    # Check to see if hardware supports desired version of OpenGL.
    if not getOGLVersionAcceptable():
        print("Hardware does not support required OpenGL version ", str(minMajor) + "." + str(minMinor))
        print("Exiting")
        exitProgram()

    # Create the GraphicsEngine and the User Interface objects.
    try:
        ge = GraphicsEngine()
        ui = UI(ge)
    except Exception as err:
        exitProgram()

    # Set up clock and frame count for FPS calculation.
    clock = pygame.time.Clock()
    starttime = time.time()
    frames = 0

    # Start the pygame event loop.
    while True:
        clock.tick(maxfps)
        frames += 1

        for event in pygame.event.get():
            # X or escape to close the program.
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                exitProgram()
            # F4 to switch FPS cap between 60 and unlimited.
            elif event.type == KEYDOWN and event.key == K_F4:
                if maxfps == 0:
                    maxfps = 60
                else:
                    maxfps = 0
            # User defined event to update FPS.
            elif event.type == UPDATE_FPS:
                now = time.time()
                fps = frames / (now - starttime)
                pygame.display.set_caption(ProgramName + "    FPS: " + str("%.2f" % fps))
                frames = 0
                starttime = now
            # Process all other events in the UI object.
            else:
                ui.processEvents(event)

        # Have graphics engine update the image.
        ge.update()

        # Swap the display buffers.
        pygame.display.flip()
