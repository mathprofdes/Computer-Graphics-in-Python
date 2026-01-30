// Persistence Of Vision raytracer version 3.5 sample file.
//
// -w320 -h240
// -w800 -h600 +a0.3

#include "colors.inc"

camera {location <2,3,-10> direction z*1 look_at <-2,2,0>}

plane {y,0 pigment {White} }
plane {z,0 pigment {SteelBlue} hollow on }

#declare Object1 =
union {
	torus {2 .1 rotate <100,10,0> translate z*1}
	text {ttf "cyrvetic.ttf","projected",.1,0}
	text {ttf "cyrvetic.ttf","through",.1,0 translate y*-1}
	scale .4 translate <-1,3,-7>
}

object {Object1 pigment {YellowGreen}}

light_source {<0,20,-50> White*2
area_light <5, 0, 0>, <0, 5, 0>, 3, 3
projected_through {Object1}
//jitter
}

light_source {<0,3,-9> White*1 shadowless}
