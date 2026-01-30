#include "colors.inc" 
#include "stones.inc"

camera {         
  location <7, 5, 3>
  look_at <0, 0, 0>                
  angle 70
}

light_source { <2, 10, 5> color White }
light_source { <-10, 15, -7> color White spotlight radius 20 falloff 40}

plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

torus {
  2, 0.3 
  pigment { Green }
  finish { ambient 0.1 diffuse 0.4 phong 0.5}
}


