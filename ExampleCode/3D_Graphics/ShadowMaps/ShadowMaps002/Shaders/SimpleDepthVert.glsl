#version 330 core

layout (location = 0) in vec4 pos;

uniform mat4 PV;
uniform mat4 Model;

void main()
{
    gl_Position = PV * Model * pos;
}
