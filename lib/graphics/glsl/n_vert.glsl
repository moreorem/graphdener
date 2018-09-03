#version 120

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
uniform float u_size;
// 2D scaling factor (zooming).
uniform vec3 u_scale;
uniform vec2 center;

uniform vec2 panzoom_scale;
uniform vec2 panzoom_translate;

// Attributes
// ------------------------------------
attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_linewidth;
attribute float a_size;

// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

vec4 panzoom(vec4 position);

void main (void) {
    v_size = a_size * u_size;
    v_linewidth = a_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = u_projection * u_view * u_model *
        vec4(a_position * u_size * u_scale,1.0);
    gl_PointSize = v_size*u_scale.x/2 + 2*(v_linewidth + 1.5*v_antialias);


}

vec4 panzoom(vec4 position)
{
    return vec4(panzoom_scale*position.xy + panzoom_translate, position.z, 1.0);
}