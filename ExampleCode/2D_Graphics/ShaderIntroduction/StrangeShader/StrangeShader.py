#! /usr/bin/env python3
#
# This program shows the basic code to correct for the aspect ratio using
# shader uniform matrices. This program also uses a fragment shader that
# illustrates the use of shader side coloring methods.
#
# Don Spickler
# 12/06/2021

import pygame
from pygame.locals import *
import time
from OpenGL.GL import *
from GraphicsEngine import *
from UI import *

# Program setup information
ProgramName = "Shader Example on Fragment Colors"
maxfps = 60
minMajor = 3
minMinor = 3
Width = 800
Height = 600


# Shut down pygame and end the program.
def exitProgram():
    pygame.quit()
    exit()


# Print graphics card information.
def PrintCardInformation():
    print()
    print("Graphics Card Information")
    print("Version  = ", glGetString(GL_VERSION).decode('utf-8'))
    print("Vender   = ", glGetString(GL_VENDOR).decode('utf-8'))
    print("Renderer = ", glGetString(GL_RENDERER).decode('utf-8'))


if __name__ == '__main__':
    try:
        # Initialize PyGame and Setup OpenGL Context.
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, minMajor)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, minMinor)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                        pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.set_mode((Width, Height), DOUBLEBUF | OPENGL | RESIZABLE | HWSURFACE)
        pygame.display.set_caption(ProgramName)
        PrintCardInformation()
    except Exception as err:
        print("Cannot initialize PyGame or setup sufficient OpenGL context. Exiting...")
        exitProgram()

    # Add a user-defined event to update the PFS in the titlebar.
    UPDATE_FPS = USEREVENT + 1
    pygame.time.set_timer(UPDATE_FPS, 1000)

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
                try:
                    fps = frames / (now - starttime)
                except Exception as err:
                    fps = 0
                pygame.display.set_caption(ProgramName + "    FPS: " + str("%.2f" % fps))
                frames = 0
                starttime = now
            # Process all other events in the UI object.
            else:
                ui.processEvents(event)

        # Process key states.
        ui.processKeyStates()

        # Have graphics engine update the image.
        ge.update()

        # Swap the display buffers.
        pygame.display.flip()
