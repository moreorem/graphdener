uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform vec3 u_scale;
uniform vec3 u_pan;

attribute vec2 from_xy;
attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

varying vec3 dxy;

void main(){
	
	dxy = vec3(0.01, 0.01, 0.);
	float denominator = from_xy[0] - a_position.x;
	float numerator = from_xy[1] - a_position.y;

	float angle = numerator / denominator;

	if (a_position.x - from_xy[0] > 0.)
		dxy[0] = -0.01;
	if (a_position.y - from_xy[1] > 0.)
		dxy[1] = -0.01;

	vec3 position_tr = u_scale * (a_position + u_pan + dxy);
	
    gl_Position = vec4(position_tr, 1.);
    gl_PointSize = u_scale.x * 2. + 2.;
}