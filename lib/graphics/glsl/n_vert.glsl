#version 120

// Uniforms
// ------------------------------------
uniform float u_antialias;
uniform float u_size;
// 2D scaling factor (zooming).
uniform vec3 u_scale;
uniform vec3 u_pan;

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


void main (void) {
    v_size = a_size * u_size;
    v_linewidth = a_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    vec3 position_tr = u_scale * (a_position + u_pan);
    gl_Position = vec4(position_tr, 1.0);
    gl_PointSize = v_size*u_scale.x/2 + 2*(v_linewidth + 1.5*v_antialias);


}

