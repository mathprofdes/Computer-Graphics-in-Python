#include "colors.inc" 
#include "stones.inc"

camera {         
  location <10, 7, -7>
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
  <0, 0, 0>, .5
  texture {
    pigment { rgb <0,1,0> }
    finish { phong 0.5 }
  }
}

torus {
    2, 0.3
    translate <0,2.5,0>
    rotate -90*x
    pigment { checker color rgb <0,1,0> color rgb <0,0,1> }
    finish { phong 0.5}
  }

torus {
    2, 0.3 
    rotate -90*x 
    translate <0,2.5,0>    
    pigment { checker color rgb <0,0,0> color rgb <1,1,1> }
    finish { phong 0.5}
  }
