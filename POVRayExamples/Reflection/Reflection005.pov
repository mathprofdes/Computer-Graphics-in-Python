#include "colors.inc" 
#include "stones.inc"

camera {         
  location <10, 10, 7>
  look_at <0, 2, 0>                
  angle 50
}

light_source { <2, 10, 5> color White }
light_source { <-5, 7, -3> color White area_light <1,0,0> <0,0,1> 5, 5}
         
plane { <0, 1, 0>, -1
  pigment { color rgb <0.1,0.1,0.1> }
  finish { phong 0.25 reflection {1.0}}
} 

sphere {
  <0, 1, -5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { phong 0.5 reflection {0.3} }
  }
}

sphere {
  <-5, 1, 0>, 2
  texture {
    pigment { color <0,0,1> }
    finish { phong 0.5 reflection {0.3} }
  } 
}

sphere {
  <-5, 1, -5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { phong 0.5 reflection {0.3} }
  }
}

