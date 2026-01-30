#include "colors.inc" 
#include "stones.inc"

camera {         
  location <-7, 5, -3>
  look_at <0, 0, 0>                
  angle 70
}

light_source { <2, 10, 5> color White }
light_source { <-10, 15, -7> color White }
         
plane { <0, 1, 0>, -1
  pigment { checker color red 1 green 0 blue 0 color red 0 green 0 blue 0 }
  finish { ambient 0.1 diffuse 0.4 }
} 

sphere {
  <0, 0, 0>, 2
  texture {
    pigment { hexagon rgb <1,1,0> rgb <1,0,1> rgb <0,1,1>}
    finish { phong 0.3 }
  }
//  rotate <-75,-45,45>
}

/*
agate 
bozo 
brick 
checker 
mandel 
hexagon 
marble 
radial 
wood 
*/