#include "colors.inc" 
#include "stones.inc"

camera {         
  location <7, 5, 3>
  look_at <0, 0, 0>                
  angle 50
}

light_source { <2, 10, 5> color White }
light_source { <-5, 7, -3> color White area_light <1,0,0> <0,0,1> 5, 5}
                  
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

box {
  <0, -1,   0>,  // Near lower left corner
  < 2, 1,  -2>   // Far upper right corner
  texture {
    T_Stone10 
    scale 5
    finish { phong 0.75 }
  }
  translate <-1,1,1>
}
