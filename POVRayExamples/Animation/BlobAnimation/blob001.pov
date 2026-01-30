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
  threshold .8
  sphere { <r*sin(0),0,r*cos(0)>,.8, 1 pigment {color rgb <1, 0.5, 0.5>} finish {reflection 0.5  phong 1 }}
  sphere { <r*sin(2*pi/3),0,r*cos(2*pi/3)>,.8, 1 pigment {color rgb <1, 0.5, 0>} finish {reflection 0.5  phong 1 }}
  sphere { <r*sin(4*pi/3),0,r*cos(4*pi/3)>,.8, 1 pigment {color rgb <1, 0, 0.5>} finish {reflection 0.5  phong 1 }}
  
  sphere { <tr*sin(clock*6*pi),0,tr*cos(clock*6*pi)>,.8, 1 pigment {color rgb <1, 0, 0>} finish {reflection 0.5  phong 1 }}
 
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