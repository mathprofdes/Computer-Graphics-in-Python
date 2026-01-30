#include "colors.inc" 
#include "stones.inc"

camera {         
  location <15, 5, 0>
  look_at <0, 1, 0>                
  angle 50
}

light_source { <10, 15, 0> color White }
light_source { <-10, 15, -7> color White }
         
         
plane { <0, 1, 0>, -1
  pigment { checker color rgb <1,0,0> color rgb <0,0,0> }
  finish { ambient 0.1 diffuse 0.4 }
} 
/*
sphere {
  <0, 1, 2>, 2
  texture {
    pigment { color Yellow}
    finish { phong 0.5 }
  }
}
*/
/*
text {
    ttf "timrom.ttf" "POV-Ray"
	0.5, 0

  rotate -90*y
  scale 3
  translate <-1,0,-6>
  texture {
    T_Stone10     // Pre-defined from stones.inc
    scale 5
    finish { phong 0.75 }
  }
}
*/

difference  {

box {
  <-4, -1,   -7>,  // Near lower left corner
  < -1.25, 3,  7>     // Far upper right corner
  texture {
    T_Stone10     // Pre-defined from stones.inc
    scale 5
    finish { phong 0.75 }
  }
}

text {
    ttf "timrom.ttf" "POV-Ray"
	0.5, 0

  rotate -90*y
  scale 3
  translate <-1,0,-6>
  texture {
    T_Stone10     // Pre-defined from stones.inc
    scale 5
    finish { phong 0.75 }
  }
}

}

/*
box {
  <-1, -1,   -1>,  // Near lower left corner
  < 1, 1,  -3>     // Far upper right corner
  texture {
    T_Stone10     // Pre-defined from stones.inc
    scale 5
    finish { phong 0.75 }
  }
}
*/