#! /usr/bin/env python3
#
# Light object
#
# The light object holds the data for a point light on the CPU side.
# Data stored are glm.vec4 vectors for position, ambient, diffuse, and
# specular. glm.vec3 vectors for the spot direction and attenuation.
# Single floats for shininess for the spot cutoff and spot exponent
# and a boolean that determines if the light is on or not.
# The class also has a function for loading the data to the shaders
# assuming the shader uses the following struct.
#
# struct Light
# {
#     bool on;             ///< Light on or off.
#     vec4 position;       ///< Position of the light.
#     vec3 spotDirection;  ///< Direction of the spot light.
#     vec4 ambient;        ///< Ambient color of the light.
#     vec4 diffuse;        ///< Diffuse color of the light.
#     vec4 specular;       ///< Specular color of the light.
#     float spotCutoff;    ///< Spot cutoff angle.
#     float spotExponent;  ///< Spot falloff exponent.
#     vec3 attenuation;    ///< Attenuation vector, x = constant, y = linear, z = quadratic.
# };
#
# Don Spickler
# 1/6/2022

import glm
from OpenGL.GL import *


class Light():
    # Constructor
    def __init__(self):
        self.on = True
        self.position = glm.vec4(30, 30, 30, 1)
        self.spotDirection = glm.vec3(-1, -1, -1)
        self.ambient = glm.vec4(0, 0, 0, 1)
        self.diffuse = glm.vec4(1, 1, 1, 1)
        self.specular = glm.vec4(1, 1, 1, 1)
        self.spotCutoff = 180
        self.spotExponent = 0
        self.attenuation = glm.vec3(1, 0, 0)

    # Resets the light data to the original settings.
    def Reset(self):
        self.on = True
        self.position = glm.vec4(30, 30, 30, 1)
        self.spotDirection = glm.vec3(-1, -1, -1)
        self.ambient = glm.vec4(0, 0, 0, 1)
        self.diffuse = glm.vec4(1, 1, 1, 1)
        self.specular = glm.vec4(1, 1, 1, 1)
        self.spotCutoff = 180
        self.spotExponent = 0
        self.attenuation = glm.vec3(1, 0, 0)

    # Loads the light information to the shader light struct.  The shader parameter is
    # the shader address and the name is the variable name of the light structure variable
    # in the shader.
    def LoadLight(self, shader, name):
        glUseProgram(shader)
        glUniform1i(glGetUniformLocation(shader, name + ".on"), self.on)
        glUniform4fv(glGetUniformLocation(shader, name + ".position"), 1, glm.value_ptr(self.position))
        glUniform3fv(glGetUniformLocation(shader, name + ".spotDirection"), 1, glm.value_ptr(self.spotDirection))
        glUniform4fv(glGetUniformLocation(shader, name + ".ambient"), 1, glm.value_ptr(self.ambient))
        glUniform4fv(glGetUniformLocation(shader, name + ".diffuse"), 1, glm.value_ptr(self.diffuse))
        glUniform4fv(glGetUniformLocation(shader, name + ".specular"), 1, glm.value_ptr(self.specular))
        glUniform1f(glGetUniformLocation(shader, name + ".spotCutoff"), self.spotCutoff)
        glUniform1f(glGetUniformLocation(shader, name + ".spotExponent"), self.spotExponent)
        glUniform3fv(glGetUniformLocation(shader, name + ".attenuation"), 1, glm.value_ptr(self.attenuation))
