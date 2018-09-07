/**
 * Copyright (c) Vispy Development Team
 * Distributed under the (new) BSD License. See LICENSE.txt for more info.
 *
 * This file contains the fragment shader template for arrow heads.
 * 
 * Variables
 * ---------
 *
 * $arrow_type
 *     The type of arrow head. Examples incude: curved, stealth, triangle_30
 *     and more.
 * $fill_type
 *     How to fill the arrow head. Possible values: "filled", "outline" or
 *     "stroke".
 *
 * Varyings
 * --------
 * v_size
 *     The arrow head size in pixels
 * v_point_size
 *     The actual size of the point used for drawing. This is larger than the
 *     given arrow head size to make sure rotating goes well, and allows some
 *     space for anti-aliasing.
 * v_color
 *     The color for the arrow head
 * v_orientation
 *     A direction vector for the orientation of the arrow head
 * v_antialias
 *     Anti-alias width
 * v_linewidth
 *     Width for the stroke or outline of the shape.
 */

#include "math/constants.glsl"
//#include "arrowheads/arrowheads.glsl"
//#include "antialias/antialias.glsl"

// Varyings
// ------------------------------------
varying float v_size;
varying float v_point_size;
varying vec4  v_color;
varying vec3  v_orientation;
varying float v_antialias;
varying float v_linewidth;

float arrow_triangle(vec2 texcoord, float size, 
                     float linewidth, float antialias, float height);
vec4 filled(float distance, float linewidth, float antialias, vec4 bg_color);

void main()
{
    // 1. Move the origin to the center of the point
    // 2. Rotate the canvas for drawing the arrow
    // 3. Scale the coordinates with v_point_size
    vec2 P = gl_PointCoord.xy - vec2(0.5, 0.5);
    P = vec2(v_orientation.x*P.x - v_orientation.y*P.y,
             v_orientation.y*P.x + v_orientation.x*P.y) * v_point_size;

    float distance = arrow_triangle(P, v_size, v_linewidth, v_antialias);
    gl_FragColor = filled(distance, v_linewidth, v_antialias, v_color,
                              v_color);
}



float arrow_triangle(vec2 texcoord, float size, 
                     float linewidth, float antialias, float height)
{
    vec2 start = -vec2(size/2.0, 0.0);
    vec2 end   = +vec2(size/2.0, 0.0);

    // Head : 3 lines
    vec2 p1 = start + size*vec2(0.0, +height);
    vec2 p2 = start + size*vec2(0.0, -height);

    float d1 = line_distance(texcoord, end, p1);
    float d2 = line_distance(texcoord, p2, end);
    float d3 = start.x - texcoord.x;


    return max(max(d1, d2), d3);
}

vec4 filled(float distance, float linewidth, float antialias, vec4 bg_color)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance < 0.0 ) {
        frag_color = bg_color;
    } else if( signed_distance < 0.0 ) {
        frag_color = bg_color;
    } else {
        frag_color = vec4(bg_color.rgb, alpha * bg_color.a);
    }

    return frag_color;
}