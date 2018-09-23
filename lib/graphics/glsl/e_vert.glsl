#include "math/constants.glsl"

uniform vec3 u_scale;
uniform vec3 u_pan;

attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_linewidth;

varying vec3 v_position;

void main(){
	vec3 position_tr = u_scale * (a_position + u_pan);
	v_position = a_position - 1.;
    gl_Position = vec4(position_tr, 1.);
}