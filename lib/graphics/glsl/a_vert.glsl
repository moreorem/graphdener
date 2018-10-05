uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform vec3 u_scale;
uniform vec3 u_pan;
uniform float opacity;

attribute vec2 from_xy;
attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec3 a_bg_color;
attribute float a_linewidth;

varying vec3 bg_color;
varying float op;
const float M_SQRT3_2 = 0.86602540378;
// void arrowhead(vec A, vec B, vec& v1, vec& v2);


void main(){
	bg_color = a_bg_color;
	op = opacity;
	vec3 position_tr = u_scale * (a_position + u_pan);

    gl_Position = vec4(position_tr, 1.);
    gl_PointSize = u_scale.x * 2. + 2.;
}

