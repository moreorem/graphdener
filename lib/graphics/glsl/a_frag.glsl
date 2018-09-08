varying float v_antialias;

void main(){
    // Decrease the alpha linearly as we come within 1 pixel of the edge.
    // Note: this only approximates the actual fraction of the pixel that is
    // covered by the visual's geometry. A more accurate measurement would
    // produce better antialiasing, but the effect would be subtle.
    gl_FragColor = vec4(1., 0., 0., 0.9);
}