#version 330 core

/**
Vertex shader using uniform projection and model matrices.

[in] icolor --- vec4 color from vertex array.
[in] position --- vec4 position from vertex array.

[out] color --- vec4 output color to the fragment shader.
*/

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 icolor;

out vec4 color;

uniform mat4 Projection;
uniform mat4 Model;

void main()
{
    color = icolor;
    gl_Position = Projection*Model*position;
}
