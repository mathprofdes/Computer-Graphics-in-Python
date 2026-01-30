#version 330 core

/**
Shader that takes projection, rotation, translation, and scaling
matrices as uniform variables and uses their product as the transformation
matrix for each vertex.

[in] icolor --- vec4 color from vertex array.
[in] position --- vec4 position from vertex array.

[out] color --- vec4 output color to the fragment shader.

Mats --- Uniform struct type holding the transformation matrices.

*/

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 icolor;

out vec4 color;

// Prototypes may be used in shaders if needed. This one could be removed.
vec4 alter(vec4 p);

struct Matrices
{
    mat4 Projection;
    mat4 Rotation;
    mat4 Scale;
    mat4 Translate;
};

uniform Matrices Mats;

vec4 alter(vec4 p)
{
    mat4 proj = Mats.Projection * Mats.Translate * Mats.Rotation * Mats.Scale;
    return proj*p;
}

void main()
{
    color = icolor;
    gl_Position = alter(position);
}
