uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform vec3 u_scale;
uniform vec3 u_pan;

attribute vec2 from_xy;
attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec3 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

varying vec3 dxy;
varying vec3 bg_color;

const float M_SQRT3_2 = 0.86602540378;
// void arrowhead(vec A, vec B, vec& v1, vec& v2);

void main(){
	bg_color = a_bg_color;
	dxy = vec3(0.01, 0.01, 0.);
	float denominator = from_xy[0] - a_position.x;
	float numerator = from_xy[1] - a_position.y;

	float angle = numerator / denominator;

	if (a_position.x - from_xy[0] > 0.)
		dxy[0] = -0.01;
	if (a_position.y - from_xy[1] > 0.)
		dxy[1] = -0.01;

	vec3 position_tr = u_scale * (a_position + u_pan);

    gl_Position = vec4(position_tr, 1.);
    gl_PointSize = u_scale.x * 2. + 2.;
}


// void arrowhead(vec3 A, vec3 B, vec3& v1, vec3& v2) 
// {
//     float h = 10*sqrtf(3), w = 10;
//     vec3 U = (B - A)/(B - A).length();
//     vec3 V = vec(-U.y, U.x);
//     v1 = B - h*U + w*V;
//     v2 = B - h*U - w*V;
// }