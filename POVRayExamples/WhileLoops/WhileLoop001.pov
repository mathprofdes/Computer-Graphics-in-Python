#include "colors.inc" 
#include "stones.inc"

camera {         
  location <20, 10, 17>
  look_at <0, 0, 0>                
  angle 50
}

light_source { <2, 10, 5> color White }
light_source { <-10, 15, -7> color White }
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

#declare tor = torus {
  1, 0.2              // major and minor radius
  pigment { Green }
  finish { phong 0.5 }
}

#declare tx = -12;

#while (tx < 12)
  #declare ty = -12;
  #while (ty < 12)
    object{
      tor
      translate <tx,0,ty>
    }
    #declare ty = ty + 2;
  #end
  #declare tx = tx + 2;
#end

