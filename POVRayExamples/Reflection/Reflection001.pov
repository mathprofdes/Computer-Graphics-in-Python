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
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

sphere {
  <0, 1, -5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { reflection {1.0} ambient 0.1 diffuse 0.4 specular 0.5 roughness 0.001 }
  }
}

sphere {
  <-5, 1, 0>, 2
  texture {
    pigment { color <0,0,1> }
    finish {  reflection {1.0} ambient 0.1  diffuse 0.4  specular 0.5 roughness 0.02 }
  } 
}

sphere {
  <-5, 1, -5>, 2
  texture {
    pigment { color <0,0,1> }
    finish {  reflection {1.0} ambient 0.1  diffuse 0.4  specular 0.5 roughness 0.05 }
  }
}

