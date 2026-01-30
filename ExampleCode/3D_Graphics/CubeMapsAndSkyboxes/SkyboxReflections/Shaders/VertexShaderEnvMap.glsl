#version 330 core

/**
Vertex shader specifically for an environment map.  Incorporates
the transformation of vertices by a projection*view*model matrix. Calculates
the transformed position and normal vectors to be passes to the fragment shader.

[in] vposition --- vec4 vertex position from memory.
[in] vnormal --- vec4 normal vector from memory.

[out] normal --- vec3 transformed normal vector.
[out] position --- vec4 transformed vertex.

[uniform] PVM --- mat4 transformation matrix in the form projection*view*model.
[uniform] model --- mat4 model matrix.

*/

layout(location = 0) in vec4 vposition;
layout(location = 2) in vec3 vnormal;

uniform mat4 PV;
uniform mat4 model;

out vec3 normal;
out vec4 position;

void main()
{
    position = model * vposition;
    normal = mat3(model) * vnormal;
    gl_Position = PV * position;
}
