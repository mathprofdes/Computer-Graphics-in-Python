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
  <0, 1, -2>, 2
  texture {   
    pigment {
      wood
      color_map {
        [0.0 color Black]
        [0.9 color DarkBrown]
        [1.0 color VeryDarkBrown]  
      } 
      turbulence 0.05
      scale <0.2, 0.3, 1>
    }
    finish { phong 0.5 }
  }
}
   
sphere {
  <0, 1, 4>, 2
  texture {
    pigment {
      wood
      color_map {
        [0.0 color Red]
        [0.5 color Blue]
        [1.0 color Green]
      }
      turbulence 1.0
      scale <0.2, 0.13, 0.1>
    }
    finish { phong 0.3 }
  }
}
