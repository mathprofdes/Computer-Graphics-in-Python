#version 330 core

/**
Vertex shader that incorporates the transformation of vertices
by a projection*view*model matrix. Also updates position and normal
vectors by pre-projected matrices.

[in] vposition --- vec4 vertex position from memory.
[in] vcolor --- vec4 vertex color from memory.
[in] vnormal --- vec3 normal vector from memory.

[out] color --- vec4 output color to the fragment shader.
[out] position --- vec4 output transformed position (before view and projection)
to the fragment shader.
[out] normal --- vec3 output transformed normal to the fragment shader.

[uniform] PVM --- mat4 transformation matrix in the form projection*view*model.
[uniform] Model --- mat4 model transformation matrix.
[uniform] NormalMatrix --- mat3 normal transformation matrix.

*/

layout(location = 0) in vec4 vposition;
layout(location = 1) in vec4 vcolor;
layout(location = 2) in vec3 vnormal;

uniform mat4 ProjView = mat4(1);
uniform mat4 Model = mat4(1);
uniform mat3 NormalMatrix = mat3(1);

out vec4 color;
out vec4 position;
out vec3 normal;

void main()
{
    color = vcolor;
    normal = normalize(NormalMatrix * vnormal);
    position = Model * vposition;
    gl_Position = ProjView * position;
}
