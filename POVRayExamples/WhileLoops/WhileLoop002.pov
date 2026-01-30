#include "colors.inc" 
#include "stones.inc"

#declare trot = 210;
#declare prot = 40;
#declare r = 20.0;
#declare PI = 3.14159265358979323846;
#declare PI_DIV_180 = 0.017453292519943296;
#declare deg = PI_DIV_180;

camera {
  location <r*cos(prot*deg)*cos(trot*deg),r*sin(prot*deg),r*cos(prot*deg)*sin(trot*deg)>
  look_at <0, 3, 0>                
  angle 50
}

light_source { <20, 100, 50> color White }
light_source { <-100, 150, -70> color White }

plane { <0, 1, 0>, 0
  pigment { checker color rgb <.5,.5,.5> color rgb <0,0,0> }
  finish { reflection {0.5} phong 0.2  }
} 

#declare obj = box {
  <0,0,0>, <1,1,1>   
  pigment { Green }
  finish { phong 1 }
}

#declare level = 3;

#while (level)
  #declare obj = object{obj scale 1/3}
  
  #declare obj = 
  object{
    union
    {
      object { obj}
      object { obj translate <1/3,0,0>}
      object { obj translate <2/3,0,0>}
      object { obj translate <0,0,1/3>}
      object { obj translate <0,0,2/3>}
      object { obj translate <1/3,0,2/3>}
      object { obj translate <2/3,0,1/3>}
      object { obj translate <2/3,0,2/3>}
      object { obj translate <0,2/3,0>}
      object { obj translate <1/3,2/3,0>}
      object { obj translate <2/3,2/3,0>}
      object { obj translate <0,2/3,1/3>}
      object { obj translate <0,2/3,2/3>}
      object { obj translate <1/3,2/3,2/3>}        
      object { obj translate <2/3,2/3,1/3>}
      object { obj translate <2/3,2/3,2/3>}
      object { obj translate <0,1/3,0>}
      object { obj translate <2/3,1/3,2/3>}
      object { obj translate <0,1/3,2/3>}
      object { obj translate <2/3,1/3,0>}        
    }
  }
  #declare level = level - 1;  
#end

object{
  obj
  scale 5
}
    