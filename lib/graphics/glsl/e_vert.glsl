uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform vec3 u_scale;
uniform vec3 u_pan;

attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

void main(){
	vec3 position_tr = u_scale * (a_position + u_pan);
    gl_Position = vec4(position_tr, 1.);
}