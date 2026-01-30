// Persistence Of Vision Ray Tracer Scene Description File
// File: splinefunction.pov
// Vers: 3.5
// Desc: A demonstration of using splines in functions.
// This scene uses a spline to make a customized gradient pattern.
// Date: 2001/08/18
// Auth: Ingo Janssen
//
// -w320 -h240
// -w800 -h600 +a0.3
//

#include "colors.inc"

#version 3.5;
global_settings {assumed_gamma 1.0}
camera {location <14.0, 8.0, -12.5> look_at <0,2,0> angle 40 }

light_source {<4,5,-30> White*2}
light_source {<4,55,30> White*2}

 lathe {
  cubic_spline 
  6,
  <1, 0>, <3, 0>,<1,2.5>,<3, 5>, <1, 5>, <1, 0>
  pigment {Red}
  finish { phong 0.7}
 }

