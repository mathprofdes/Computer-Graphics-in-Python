#! /usr/bin/env python3
#
# Material object
#
# The material object holds the data for a material on the CPU side.
# Data stored are glm.vec4 vectors for ambient, diffuse, specular, and
# emission and a single float shininess for the shininess exponent.
# The class also has a function for loading the data to the shaders
# assuming the shader uses the following struct.
#
# struct Material
# {
#     vec4 ambient;     ///< Ambient color of the material.
#     vec4 diffuse;     ///< Diffuse color of the material.
#     vec4 specular;    ///< Specular color of the material.
#     vec4 emission;    ///< Emission color of the material.
#     float shininess;  ///< Shininess exponent of the material.
# };
#
# The class also has several standard material presets for loading
# some standard materials.
#
# Don Spickler
# 1/6/2022

import glm
from OpenGL.GL import *


class Material():
    # Constructor
    def __init__(self):
        self.ambient = glm.vec4(0.3, 0, 0, 1)
        self.diffuse = glm.vec4(0.6, 0, 0, 1)
        self.specular = glm.vec4(0.8, 0.6, 0.6, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 32

    # Loads the material information to the shader material struct.  The shader parameter is
    # the shader address and the name is the variable name of the material structure variable
    # in the shader.
    def LoadMaterial(self, shader, name):
        glUseProgram(shader)
        glUniform4fv(glGetUniformLocation(shader, name + ".ambient"), 1, glm.value_ptr(self.ambient))
        glUniform4fv(glGetUniformLocation(shader, name + ".diffuse"), 1, glm.value_ptr(self.diffuse))
        glUniform4fv(glGetUniformLocation(shader, name + ".specular"), 1, glm.value_ptr(self.specular))
        glUniform4fv(glGetUniformLocation(shader, name + ".emission"), 1, glm.value_ptr(self.emission))
        glUniform1f(glGetUniformLocation(shader, name + ".shininess"), self.shininess)

    ##############################################
    #  Material Preset Functions
    ##############################################

    def RedPlastic(self):
        self.ambient = glm.vec4(0.3, 0, 0, 1)
        self.diffuse = glm.vec4(0.6, 0, 0, 1)
        self.specular = glm.vec4(0.8, 0.6, 0.6, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 32

    def GreenPlastic(self):
        self.ambient = glm.vec4(0, 0.3, 0, 1)
        self.diffuse = glm.vec4(0, 0.6, 0, 1)
        self.specular = glm.vec4(0.6, 0.8, 0.6, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 32

    def BluePlastic(self):
        self.ambient = glm.vec4(0, 0, 0.3, 1)
        self.diffuse = glm.vec4(0, 0, 0.6, 1)
        self.specular = glm.vec4(0.6, 0.6, 0.8, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 32

    def WhitePlastic(self):
        self.ambient = glm.vec4(0.3, 0.3, 0.3, 1)
        self.diffuse = glm.vec4(0.6, 0.6, 0.6, 1)
        self.specular = glm.vec4(0.8, 0.8, 0.8, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 32

    def Brass(self):
        self.ambient = glm.vec4(0.329412, 0.223529, 0.027451, 1)
        self.diffuse = glm.vec4(0.780392, 0.568627, 0.113725, 1)
        self.specular = glm.vec4(0.992157, 0.941176, 0.807843, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 27.8974

    def Bronze(self):
        self.ambient = glm.vec4(0.2125, 0.1275, 0.054, 1)
        self.diffuse = glm.vec4(0.714, 0.4284, 0.18144, 1)
        self.specular = glm.vec4(0.393548, 0.271906, 0.166721, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 25.6

    def PolishedBronze(self):
        self.ambient = glm.vec4(0.25, 0.148, 0.06475, 1)
        self.diffuse = glm.vec4(0.4, 0.2368, 0.1036, 1)
        self.specular = glm.vec4(0.774597, 0.458561, 0.200621, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 76.8

    def Chrome(self):
        self.ambient = glm.vec4(0.25, 0.25, 0.25, 1)
        self.diffuse = glm.vec4(0.4, 0.4, 0.4, 1)
        self.specular = glm.vec4(0.774597, 0.774597, 0.774597, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 76.8

    def Copper(self):
        self.ambient = glm.vec4(0.19125, 0.0735, 0.0225, 1)
        self.diffuse = glm.vec4(0.7038, 0.27048, 0.0828, 1)
        self.specular = glm.vec4(0.256777, 0.137622, 0.086014, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 12.8

    def PolishedCopper(self):
        self.ambient = glm.vec4(0.2295, 0.08825, 0.0275, 1)
        self.diffuse = glm.vec4(0.5508, 0.2118, 0.066, 1)
        self.specular = glm.vec4(0.580594, 0.223257, 0.0695701, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 51.2

    def Gold(self):
        self.ambient = glm.vec4(0.24725, 0.1995, 0.0745, 1)
        self.diffuse = glm.vec4(0.75164, 0.60648, 0.22648, 1)
        self.specular = glm.vec4(0.628281, 0.555802, 0.366065, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 51.2

    def PolishedGold(self):
        self.ambient = glm.vec4(0.24725, 0.2245, 0.0645, 1)
        self.diffuse = glm.vec4(0.34615, 0.3143, 0.0903, 1)
        self.specular = glm.vec4(0.797357, 0.723991, 0.208006, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 83.2

    def Pewter(self):
        self.ambient = glm.vec4(0.105882, 0.058824, 0.113725, 1)
        self.diffuse = glm.vec4(0.427451, 0.470588, 0.541176, 1)
        self.specular = glm.vec4(0.333333, 0.333333, 0.521569, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 9.84615

    def Silver(self):
        self.ambient = glm.vec4(0.19225, 0.19225, 0.19225, 1)
        self.diffuse = glm.vec4(0.50754, 0.50754, 0.50754, 1)
        self.specular = glm.vec4(0.508273, 0.508273, 0.508273, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 51.2

    def PolishedSilver(self):
        self.ambient = glm.vec4(0.23125, 0.23125, 0.23125, 1)
        self.diffuse = glm.vec4(0.2775, 0.2775, 0.2775, 1)
        self.specular = glm.vec4(0.773911, 0.773911, 0.773911, 1)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 89.6

    def Emerald(self):
        self.ambient = glm.vec4(0.0215, 0.1745, 0.0215, 0.55)
        self.diffuse = glm.vec4(0.07568, 0.61424, 0.07568, 0.55)
        self.specular = glm.vec4(0.633, 0.727811, 0.633, 0.55)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 76.8

    def Jade(self):
        self.ambient = glm.vec4(0.135, 0.2225, 0.1575, 0.95)
        self.diffuse = glm.vec4(0.54, 0.89, 0.63, 0.95)
        self.specular = glm.vec4(0.316228, 0.316228, 0.316228, 0.95)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 12.8

    def Obsidian(self):
        self.ambient = glm.vec4(0.05375, 0.05, 0.06625, 0.82)
        self.diffuse = glm.vec4(0.18275, 0.17, 0.22525, 0.82)
        self.specular = glm.vec4(0.332741, 0.328634, 0.346435, 0.82)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 38.4

    def Pearl(self):
        self.ambient = glm.vec4(0.25, 0.20725, 0.20725, 0.922)
        self.diffuse = glm.vec4(1, 0.829, 0.829, 0.922)
        self.specular = glm.vec4(0.296648, 0.296648, 0.296648, 0.922)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 11.264

    def Ruby(self):
        self.ambient = glm.vec4(0.1745, 0.01175, 0.01175, 0.55)
        self.diffuse = glm.vec4(0.61424, 0.04136, 0.04136, 0.55)
        self.specular = glm.vec4(0.727811, 0.626959, 0.626959, 0.55)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 76.8

    def Turquoise(self):
        self.ambient = glm.vec4(0.1, 0.18725, 0.1745, 0.8)
        self.diffuse = glm.vec4(0.396, 0.74151, 0.69102, 0.8)
        self.specular = glm.vec4(0.297254, 0.30829, 0.306678, 0.8)
        self.emission = glm.vec4(0, 0, 0, 1)
        self.shininess = 12.8
