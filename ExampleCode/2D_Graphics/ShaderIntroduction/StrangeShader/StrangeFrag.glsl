#version 330 core

/**
Strange fragment shader that colors fragments by the gl_FragCoord and some of the
GLSL buit-in functions.  The example also shows the use of functions inside a
glsl shader and using a uniform variable to control animation inside the shader.

[in] pos --- vec4 color from vertex array.
[in] color --- vec4 position from vertex array.

[out] col --- vec4 output color to the fragment shader.


*/

in vec4 pos;
in vec4 color;

out vec4 col;

uniform int shadernum = 0;
uniform float time = 0;

vec4 setColor1(vec4 p)
{
    return vec4(sin(p.x), cos(p.y-sin(p.x)), sin(cos(p.y) + p.x), 1);
}

vec4 setColor2(vec4 p)
{
    float x = floor(p.x) + floor(fract(p.x) + 0.5);
    float y = floor(p.y) + floor(fract(p.y) + 0.5);
    vec2 ipt = vec2(x, y);
    vec2 pt2 = vec2(p);
    float d = distance(ipt, pt2);
    vec4 col = vec4(0, 1, 0, 1);
    return (1-d) * col;
}

vec4 setColor3(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = length(pt2);
    vec4 col = vec4(1, 0, 0, 1);
    return d * col;
}

vec4 setColor4(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = cos(20*length(pt2));
    vec4 col = vec4(1, 0, 0, 1);
    return d * col;
}

vec4 setColor5(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = 0.5*(cos(10 * pt2.x)+1);
    vec4 col = vec4(0, 1, 0, 1);
    return d * col;
}

vec4 setColor6(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d1 = 0.5*(cos(10 * pt2.x)+1);
    float d2 = 0.5*(sin(20 * pt2.y)+1);
    vec4 col = d1*vec4(0, 1, 0, 1) + d2*vec4(1, 0, 0, 1);
    return col;
}

void main()
{
    if (shadernum == 0)
        col = color;
    else if (shadernum == 1)
        col = setColor1(3*pos);
    else if (shadernum == 2)
        col = setColor1(10*pos);
    else if (shadernum == 3)
        col = setColor2(5*pos);
    else if (shadernum == 4)
        col = setColor2(1/pos);
    else if (shadernum == 5)
        col = setColor3(pos);
    else if (shadernum == 6)
        col = setColor4(pos);
    else if (shadernum == 7)
        col = setColor5(pos);
    else if (shadernum == 8)
        col = setColor6(pos);
    else if (shadernum == 9)
        col = setColor6(pos + vec4(time, 0, 0, 0));
}
