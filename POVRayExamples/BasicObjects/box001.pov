#include "colors.inc" 
#include "stones.inc"

camera {         
  location <7, 5, 3>
  look_at <0, 0, 0>                
  angle 70
}

light_source { <2, 10, 5> color White }
light_source { <-10, 15, -7> color White }
         
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

sphere {
  <0, 1, 2>, 2
  texture {
  T_Stone10
    //pigment { color Yellow}
    finish { phong 0.5 }
  }
}

box {
 < 1, 1,  -3> ,    // Far upper right corner
  <-1, -1,   -1>  // Near lower left corner
 // < 1, 1,  -3>     // Far upper right corner
  texture {
    T_Stone10     // Pre-defined from stones.inc
    scale 5
    finish { phong 0.75 }
  }
}
