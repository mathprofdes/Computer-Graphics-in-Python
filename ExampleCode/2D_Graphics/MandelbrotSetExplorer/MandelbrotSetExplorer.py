#! /usr/bin/env python3
#
# This example is an extension of some of the 2-D shader examples for the course. It graphs the Mandelbrot Set
# and other sets in the same family, z^n+c for n = 2, 3, 4, ..., 10.  There are many user interface options
# that allow for color scheme changes and set parameter changes.
#
# User Options
#
# Keyboard Options
#
# - Escape + Alt:  Ends the program.
# - D: Toggles the precision between single and double.
# - S: Toggles the smooth graphing.
# - F8: Resets the fractal to the starting fractal.
# - F11: Prints the parameter settings for the image to the console.
# - F12: Saves a screen shot of the graphics window to a png file.
#         In addition it saves a text file containing the parameter settings for the image.

# - I Key is Down: Iteration mode
#     - 0: Sets bailout iteration to 50.
#     - 1: Sets bailout iteration to 100.
#     - 2: Sets bailout iteration to 250.
#     - 3: Sets bailout iteration to 500.
#     - 4: Sets bailout iteration to 1000.
#     - 5: Sets bailout iteration to 2500.
#     - 6: Sets bailout iteration to 5000.
#     - 7: Sets bailout iteration to 7500.
#     - 8: Sets bailout iteration to 10000.
#     - 9: Sets bailout iteration to 20000.
# - B Key is Down: Boarder mode
#     - 0: Sets border percentage to 0%.
#     - 1: Sets border percentage to 10%.
#     - 2: Sets border percentage to 20%.
#     - 3: Sets border percentage to 30%.
#     - 4: Sets border percentage to 40%.
#     - 5: Sets border percentage to 50%.
#     - 6: Sets border percentage to 60%.
#     - 7: Sets border percentage to 70%.
#     - 8: Sets border percentage to 80%.
#     - 9: Sets border percentage to 90%.
# - E Key is Down: Exponent mode, the exponent for z^n+c.
#     - 0: Sets exponent to 10.
#     - 1: Sets exponent to 2.
#     - 2: Sets exponent to 2.
#     - 3: Sets exponent to 3.
#     - 4: Sets exponent to 4.
#     - 5: Sets exponent to 5.
#     - 6: Sets exponent to 6.
#     - 7: Sets exponent to 7.
#     - 8: Sets exponent to 8.
#     - 9: Sets exponent to 9.
# - O Key is Down: Iteration Offset mode
#     - 0: Sets the offset to 0.
#     - 1: Sets the offset to 10.
#     - 2: Sets the offset to 20.
#     - 3: Sets the offset to 30.
#     - 4: Sets the offset to 40.
#     - 5: Sets the offset to 50.
#     - 6: Sets the offset to 60.
#     - 7: Sets the offset to 70.
#     - 8: Sets the offset to 80.
#     - 9: Sets the offset to 90.
# - W Key is Down: Color palette scaling mode
#     - 1: Sets the palette scale to 0.1.
#     - 2: Sets the palette scale to 0.25.
#     - 3: Sets the palette scale to 0.5.
#     - 4: Sets the palette scale to 0.75.
#     - 5: Sets the palette scale to 1.
#     - 6: Sets the palette scale to 2.5.
#     - 7: Sets the palette scale to 5.
#     - 8: Sets the palette scale to 10.
#     - 9: Sets the palette scale to 25.
# - T Key is Down: Color palette selection mode
#     - 1: Sets the palette to a single color fade in and fade out.  The color can be altered
#             by the user using the keyboard interface.
#     - 2: Sets the palette to alternating color to black and the color is faded in and out
#             in the sequence.  The color can be altered by the user using the keyboard interface.
#     - 3: Sets the palette to a repeating ROYGBIV scheme.
#     - 4: Sets the palette to a repeating RGB scheme.
#     - 5: Sets the palette to a repeating KROYGBIV scheme with K = black.
#     - 6: Sets the palette to a repeating RGB scheme with K = black.
#     - 7: Sets the palette to a repeating KRKGKBKW scheme with K = black and W = white.
#     - 8: Sets the palette to a repeating KRYGCBPW scheme.
#     - 9: Sets the palette to a repeating 10 random color scheme.
#     - 0: Sets the palette to a repeating random color scheme with between 5 and 25 colors.
#
# Keyboard + Arrow Key Options
#
# - Arrow keys alone
#     - Left: Moves the image to the left.
#     - Right: Moves the image to the right.
#     - Up: Moves the image up.
#     - Down: Moves the image down.
#
# - I Key is Down: Iteration mode
#     - Up: Increases the bailout iteration by 1.
#     - Down: Decreases the bailout iteration by 1.
#
# - U Key is Down: Fast iteration mode
#     - Up: Increases the bailout iteration by 10.
#     - Down: Decreases the bailout iteration by 10.
#
# - Y Key is Down: Very fast iteration mode
#     - Up: Increases the bailout iteration by 100.
#     - Down: Decreases the bailout iteration by 100.
#
# - B Key is Down: Boarder color mode
#     - Up: Increases the boarder color percentage.
#     - Down: Decreases the boarder color percentage.
#
# - W Key is Down: Palette scale mode.
#     - Up: Increases the palette scale.
#     - Down: Decreases the palette scale.
#
# - O Key is Down: Palette offset mode.
#     - Up: Increases the palette offset.
#     - Down: Decreases the palette offset.
#
# - N Key is Down: Bailout radius mode
#     - Up: Increases the bailout radius.
#     - Down: Decreases the bailout radius.
#
# - Z Key is Down: Zoom mode
#     - Up: Zooms In
#     - Down: Zooms Out
#
# - C and R Keys are Down: Color selection for Red
#     - Up: Increases component.
#     - Down: Decreases component.
# - C and G Keys are Down: Color selection for Green
#     - Up: Increases component.
#     - Down: Decreases component.
# - C and B Keys are Down: Color selection for Blue
#     - Up: Increases component.
#     - Down: Decreases component.
#
#
# Mouse Options
#
# - Wheel movement zooms the image in and out.
# - Ctrl + Wheel movement zooms the image in and out faster.
# - Right click alone with recenter the image to the click position.
# - Click and drag will reposition inage with cursor.
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
ProgramName = "Mandelbrot Set Explorer"
maxfps = 60
minMajor = 4
minMinor = 0
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
    noteready = True
    lastTitleBarNote = None

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
                if ge.TitleBarNote != None:
                    ge.TitleBarNote = None
                else:
                    pygame.display.set_caption(ProgramName + "    FPS: " + str("%.2f" % fps))
                frames = 0
                starttime = now
            # Process all other events in the UI object.
            else:
                ui.processEvents(event)

        if ge.TitleBarNote != None:
            pygame.display.set_caption(ge.TitleBarNote)

        # Process key states.
        ui.processKeyStates()

        # Have graphics engine update the image.
        ge.update()

        # Swap the display buffers.
        pygame.display.flip()
