#version 330 core

/**
Simple pass through vertex shader.

[in] icolor --- vec4 color from vertex array.
[in] position --- vec4 position from vertex array.

[out] color --- vec4 output color to the fragment shader.

Uniform projection matrix for the aspect ratio adjustment.

*/

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 icolor;

out vec4 color;
out vec4 pos;

uniform mat4 Projection;

void main()
{
    color = icolor;
    pos = position; 
    gl_Position = Projection*position;
}
