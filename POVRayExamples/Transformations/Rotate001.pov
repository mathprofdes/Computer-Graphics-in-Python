#include "colors.inc" 
#include "stones.inc"

camera {         
  location <6, 10, 15>
  look_at <0, 0, 0>                
  angle 50
}

light_source { <2, 10, 5> color White }
light_source { <-5, 7, -3> color White area_light <1,0,0> <0,0,1> 5, 5}
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

sphere {
  <0, 0, 0>, 1
  texture {
    pigment { rgb <0,1,0> }
    finish { phong 0.5 }
  }
  scale <2,3,4>
  rotate 90*x
  rotate 90*z
  translate <0,2,0>
}
