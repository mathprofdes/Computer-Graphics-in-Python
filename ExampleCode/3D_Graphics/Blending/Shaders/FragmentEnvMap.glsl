#version 330 core

/**
Fragment shader that is specific for an environment map.

[in] normal --- vec3 normal vector at the vertex.
[in] position --- vec4 transformed position of the vertex, prior to
the view and projection transformations.

[out] fColor --- vec4 output color to the frame buffer.

[uniform] cmtex --- samplerCube, the texture.
[uniform] eye --- vec3 position of the camera.

*/

in vec3 normal;
in vec4 position;

uniform samplerCube cmtex;
uniform vec3 eye;

out vec4 fColor;

void main()
{
    vec3 tc = reflect(position.xyz-eye, normalize(normal));
    fColor = texture(cmtex, tc);
}
