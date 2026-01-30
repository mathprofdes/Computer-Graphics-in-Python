#! /usr/bin/env python3
#
# This program is a demo program for the basic setup for 3-D OpenGL rendering.  It
# incorporates classes for axes, a 2D box, and a simple multi-colored cube.  It also has classes
# for a spherical camera and yaw-pitch-roll camera.
#
# The initial screen will render the coordinate axes and a grid of multi-colored cubes.  The
# options discussed below can be used to alter the position of the camera and scene objects.
# The projection, view, and model matrices are loaded to the shader and the matrix
# multiplication is done at the shader level.
#
# User Options - Keys
#
# - Escape:  Ends the program.
# - C: Toggles between the two cameras.
# - O: Toggles between outline and fill mode for the box and cube objects.
# - L: Toggles the drawing of the axes.
# - 1: Draws the grid of cubes.
# - 2: Draws a single cube.
# - 3: Draws the 2D box.
# - F1: Draws in fill mode.
# - F2: Draws in line mode.
# - F3: Draws in point mode.
# - F4: Toggles between 60 FPS and unlimited FPS.
# - F12: Saves a screen shot of the graphics window to a png file.
#
# If the spherical camera is currently selected,
#
# If no modifier keys are pressed:
#
# - Left: Increases the camera's theta value.
# - Right: Decreases the camera's theta value.
# - Up: Increases the camera's psi value.
# - Down: Decreases the camera's psi value.
#
# If the control or Z key is down:
#
# - Up: Decreases the camera's radius.
# - Down: Increases the camera's radius.
#
# If the yaw-pitch-roll camera is currently selected,
#
# If no modifier keys are pressed:
#
# - Left: Increases the yaw.
# - Right: Decreases the yaw.
# - Up: Increases the pitch.
# - Down: Decreases the pitch.
#
# If the control or Z key is down:
#
# - Left: Increases the roll.
# - Right: Decreases the roll.
# - Up: Moves the camera forward.
# - Down: Moves the camera backward.
#
# If the shift or S key is down:
#
# - Left: Moves the camera left.
# - Right: Moves the camera right.
# - Up: Moves the camera up.
# - Down: Moves the camera down.
#
# User Options - Mouse
#
# If the spherical camera is currently selected,
#
# If no modifier keys are pressed and the left mouse button is down a movement will
# alter the theta and psi angles of the spherical camera to give the impression
# of the mouse grabbing and moving the coordinate system.
#
# If the control key is down and the left mouse button is down then the camera will
# be moved in and out from the origin by the vertical movement of the mouse.
#
# If the wheel is moved then the camera will be moved in and out from the origin by
# the amount of the wheel movement.
#
# If the yaw-pitch-roll camera is currently selected,
#
# If no modifier keys are pressed and the left mouse button is down a movement will
# alter the yaw and pitch angles of the camera.
#
# If the control key is down and the left mouse button is down then the camera will
# be moved forward and backward by the vertical movement of the mouse.
#
# If the shift key is down and the left mouse button is down then the camera will
# be moved right and left as well as up and down.
#
# If the shift and control keys are down and the left mouse button is down then the
# camera will roll.
#
# If the wheel is moved then the camera will be moved foward and backward by
# the amount of the wheel movement.
#
# Don Spickler
# 12/30/2021

import pygame
from pygame.locals import *
import time
from OpenGL.GL import *
from GraphicsEngine import *
from UI import *

# Program setup information
ProgramName = "Cameras & Basic 3-D Setup Example #1"
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
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
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

        # Process Key states
        ui.processKeyStates()

        # Have graphics engine update the image.
        ge.update()

        # Swap the display buffers.
        pygame.display.flip()
