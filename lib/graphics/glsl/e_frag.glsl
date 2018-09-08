varying float v_antialias;
// attribute vec3 line_pos;
varying vec3 v_position;

void main(){
    // Decrease the alpha linearly as we come within 1 pixel of the edge.
    // Note: this only approximates the actual fraction of the pixel that is
    // covered by the visual's geometry. A more accurate measurement would
    // produce better antialiasing, but the effect would be subtle.
    gl_FragColor = vec4(0., 0., 0., 1.);
}