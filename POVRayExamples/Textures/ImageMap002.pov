#include "colors.inc" 
#include "stones.inc"

camera {         
  location <10, 7, 5>
  look_at <0, 0, 0>                
  angle 50
}

light_source { <2, 10, 5> color White }
light_source { <-5, 7, -3> color White area_light <1,0,0> <0,0,1> 5, 5}
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

torus {
  2, 0.7              // major and minor radius
  translate <0,1,0>
  pigment{ image_map {"Image3.bmp" map_type 5 } }
  finish { ambient 0.1 diffuse 0.4 phong 0.5}
}
