#include "colors.inc" 
#include "stones.inc"
#include "textures.inc"
#include "shapes.inc"
#include "glass.inc"
#include "metals.inc"
#include "woods.inc"
                    
camera {         
  location <-3, 6, -2>
  look_at <0, 0, 0>                
  angle 70
}

light_source { <2, 10, 5> color White }
light_source { <-10, 15, -7> color White }

plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

torus {
  2, 0.5 
  pigment { color rgbt <0, 0, 1, 0.7> }
  finish { phong 0.5 }
}

