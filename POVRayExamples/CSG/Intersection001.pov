#include "colors.inc" 
#include "stones.inc"

camera {         
  location <7, 5, 0>
  look_at <0, 0, 0>                
  angle 70
}

light_source { <2, 10, 5> color White }
light_source { <-5, 7, -3> color White area_light <1,0,0> <0,0,1> 5, 5}
         
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

#declare sphere1 = sphere {
  <-1, 1,-1>, 2
  texture {
    pigment { color Yellow}
    finish { phong 0.5 }
  }
}

#declare sphere2 = sphere {
  <-1, 1,-3>, 2
  texture {
    pigment { color Green}
    finish { phong 0.5 }
  }
}

intersection  {
  object {sphere1}
  object {sphere2}
}
