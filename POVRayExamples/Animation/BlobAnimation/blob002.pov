#include "colors.inc" 
#include "stones.inc"
#include "textures.inc"    // pre-defined scene elements
#include "shapes.inc"
#include "glass.inc"
#include "metals.inc"
#include "woods.inc"
          
camera {         
  location <-2, 2, -2>
  look_at <0, -0.5, 0>                
  angle 70
}

light_source { <2, 10, 5> color White area_light <1,0,0> <0,0,1> 5, 5 orient circular }
light_source { <-10, 15, -7> color White area_light <1,0,0> <0,0,1> 5, 5 orient circular }

plane { <0, 1, 0>, -1.5
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> scale 2}
  finish { ambient 0.1 diffuse 0.4 }
} 

#declare tr = 1.5;
#declare r = tr; // tr*cos(clock*6*pi);

object{
blob {
  threshold .7
  sphere { <0.8,0,0>,1.5, 1 pigment {color rgb <1, 0.5, 0.5>} finish {reflection 0.5  phong 1 }}
  sphere { <-1,0,0>,1.5, 1 
  
  texture {
    T_Stone10
    //pigment { color Yellow}
    normal { bumps 0.5 scale 0.1 }
    finish { phong 0.5 }
    }}
  
  /*
  cylinder {
    <1, 0, 0>,     // Center of one end
    <-1, 0, 0>,     // Center of other end
    0.1, 1            // Radius
    texture {pigment {color rgb <1, 0.5, 0.5>} finish {reflection 0.5  phong 1 }}
    */
  //}

}
}
 
/*            
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
*/