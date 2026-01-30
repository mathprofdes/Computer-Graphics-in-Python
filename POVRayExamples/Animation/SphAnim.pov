#include "colors.inc" 

#declare trot = 30 + clock*360;
#declare prot = 50;
#declare r = 20.0;
#declare PI = 3.14159265358979323846;
#declare PI_DIV_180 = 0.017453292519943296;
#declare deg = PI_DIV_180;

camera {
  location <r*cos(prot*deg)*cos(trot*deg),r*sin(prot*deg),r*cos(prot*deg)*sin(trot*deg)>
  look_at <0, 0, 0>                
  angle 50
}

light_source { <2, 10, 5> color White shadowless }
light_source { <-5, 7, -3> color White area_light <1,0,0> <0,0,1> 5, 5}
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 

sphere {
  <2.5, 1, 2.5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { reflection {1.0} phong 0.7 }
  }
}

sphere {
  <-2.5, 1, 2.5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { reflection {1.0} phong 0.7 }
  } 
}

sphere {
  <-2.5, 1, -2.5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { reflection {1.0} phong 0.7 }
  }
}

sphere {
  <2.5, 1, -2.5>, 2
  texture {
    pigment { color <0,0,1> }
    finish { reflection {1.0} phong 0.7 }
  }
}
