#version 400 core

/**

*/

in vec4 pos;
out vec4 col;

struct iterInfo
{
    int iter;
    float rad;
};

uniform vec2 center = vec2(0, 0);
uniform dvec2 centerD = dvec2(0, 0);
uniform float boarderPer = 0.25;
uniform float scale = 2;
uniform double scaleD = 2;
uniform float bailoutRad = 10;
uniform int exponent = 2;
uniform int maxiter = 100;
uniform bool doublePrec = false;
uniform bool smoothRender = true;
uniform vec4 setColor = vec4(0, 0, 0, 1);
uniform vec4 borderColor = vec4(1, 1, 1, 1);
uniform vec4 colorSet[100];
uniform float iterationScale = 2.5;
uniform float colorsOffset = 0;

vec2 cmult(vec2 a, vec2 b)
{
    return vec2(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x);
}

vec2 cadd(vec2 a, vec2 b)
{
    return vec2(a.x + b.x, a.y + b.y);
}

dvec2 cmultD(dvec2 a, dvec2 b)
{
    return dvec2(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x);
}

dvec2 caddD(dvec2 a, dvec2 b)
{
    return dvec2(a.x + b.x, a.y + b.y);
}

iterInfo mandIter(vec4 p, int power)
{
    vec2 c = scale * vec2(p) - center;
    vec2 q = vec2(0, 0);
    int i = 0;

    while(i < maxiter && length(q) < bailoutRad)
    {
        vec2 t = vec2(1, 0);
        for(int j = 0; j < power; j++)
            t = cmult(t, q);

        q = cadd(t, c);
        i++;
    }

    iterInfo info;
    info.iter = i;
    info.rad = length(q);

    return info;
}

iterInfo mandIterD(vec4 p, int power)
{
    dvec2 c = scaleD * dvec2(p) - centerD;
    dvec2 q = dvec2(0, 0);
    int i = 0;

    while(i < maxiter && length(q) < bailoutRad)
    {
        dvec2 t = dvec2(1, 0);
        for(int j = 0; j < power; j++)
            t = cmultD(t, q);

        q = caddD(t, c);
        i++;
    }

    iterInfo info;
    info.iter = i;
    info.rad = float(length(q));

    return info;
}

vec4 mandColor(iterInfo info, bool smth)
{
    vec4 color = vec4(0, 0, 0, 1);
    float siter = info.iter + 1 + log(log(bailoutRad) / log(info.rad)) / log(exponent);

    if(info.iter >= maxiter)
        siter = maxiter + 1;

    if(siter >= maxiter)
        color = setColor;
    else if(siter >= boarderPer * maxiter)
        color = borderColor;
    else
    {
        float scaledIter = siter * iterationScale + colorsOffset;

        int loc = int(scaledIter) % 100;
        int nextloc = (loc + 1) % 100;

        if(smth)
        {
            vec4 color1 = colorSet[loc];
            vec4 color2 = colorSet[nextloc];
            float frac = scaledIter - int(scaledIter);
            color = frac * color2 + (1 - frac) * color1;
        }
        else
            color = colorSet[loc];
    }

    return color;
}

void main()
{
    iterInfo info;

    if(doublePrec)
        info = mandIterD(pos, exponent);
    else
        info = mandIter(pos, exponent);

    col = mandColor(info, smoothRender);

}
