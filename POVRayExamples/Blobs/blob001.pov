#include "colors.inc" 
#include "stones.inc"
#include "textures.inc"    // pre-defined scene elements
#include "shapes.inc"
#include "glass.inc"
#include "metals.inc"
#include "woods.inc"
          
camera {         
  location <-1, 3, -2>
  look_at <0, 0, 0>                
  angle 70
}

light_source { <2, 10, 5> color White }
light_source { <-10, 15, -7> color White }

plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 
            
blob {
  threshold .5
  sphere { <.5,0,0>, .8, 1 pigment {color rgb <0, 0, 1>} }
  sphere { <-.5,0,0>,.8, 1 pigment {color rgb <1, 0, 0.5>} }
  finish { phong 1 }
  translate <0,0,3>
}

blob {
  threshold .7
  sphere { <.5,0,0>, .8, 1 pigment {color rgb <0, 0, 1>} }
  sphere { <-.5,0,0>,.8, 1 pigment {color rgb <1, 0, 0.5>} }
  finish { phong 1 }
  translate <0,0,2>
}

blob {
  threshold .75
  sphere { <.5,0,0>, .8, 1 pigment {color rgb <0, 0, 1>} }
  sphere { <-.5,0,0>,.8, 1 pigment {color rgb <1, 0, 0.5>} }
  finish { phong 1 }
  translate <0,0,1>
}

blob {
  threshold .8
  sphere { <.5,0,0>, .8, 1 pigment {color rgb <0, 0, 1>} }
  sphere { <-.5,0,0>,.8, 1 pigment {color rgb <1, 0, 0.5>} }
  finish { phong 1 }
  translate <0,0,0>
}

blob {
  threshold .9
  sphere { <.5,0,0>, .8, 1 pigment {color rgb <0, 0, 1>} }
  sphere { <-.5,0,0>,.8, 1 pigment {color rgb <1, 0, 0.5>} }
  finish { phong 1 }
  translate <0,0,-1>
}
