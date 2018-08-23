#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vispy: gallery 60

"""
Dynamic planar graph layout.
"""

import numpy as np
from vispy import gloo, app
from vispy.gloo import set_viewport, set_state, clear
from vispy.app import use_app
from vispy.visuals import GraphVisual
from vispy.visuals.graphs import layouts
from vispy.visuals.transforms import STTransform
from vispy.util.transforms import perspective, translate
# from vispy.scene import visuals
from vispy.app import use_app
from vispy.visuals import GraphVisual
from vispy.scene.visuals import Line, Markers

vert = """
#version 120

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_linewidth;
uniform float u_antialias;
uniform float u_size;

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
    gl_Position = u_projection * u_view * u_model * vec4(a_position,3.0);
    gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""

frag = """
#version 120

// Constants
// ------------------------------------
#define resolution vec2(500.0, 500.0)
#define Thickness 0.003
// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

// Functions
// ------------------------------------
float marker(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}

float drawLine(vec2 p1, vec2 p2)
{
    vec2 uv = gl_FragCoord.xy / resolution.xy;

    float a = abs(distance(p1, uv));
    float b = abs(distance(p2, uv));
    float c = abs(distance(p1, p2));

    if ( a >= c || b >=  c ) return 0.0;

    float p = (a + b + c) * 0.5;

    // median to (p1, p2) vector
    float h = 2 / c * sqrt( p * ( p - a) * ( p - b) * ( p - c));

    return mix(1.0, 0.0, smoothstep(0.5 * Thickness, 1.5 * Thickness, h));
}

// Main
// ------------------------------------
void main()
{
    // size turns outline to circle
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;

    // The marker function needs to be linked with this shader
    float r = marker(gl_PointCoord, size);

    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias))
    {
        discard;
    }
    else if( d < 0.0 )
    {
       gl_FragColor = v_fg_color;
    }
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
    /*gl_FragColor = vec4(
        max( max( drawLine(vec2(0.1, 0.1), vec2(0.1, 0.9)),
                  drawLine(vec2(0.1, 0.9), vec2(0.7, 0.5))),
                  drawLine(vec2(0.1, 0.1), vec2(0.7, 0.5))));*/
}
"""

use_app('PyQt5')


class GraphCanvas(app.Canvas):

    def __init__(self, nodes):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))
        ps = self.pixel_scale

        # Window position
        self.position = 450, 250

        # TODO: create array from node type to insert as a_bg_color
        # FIXME: Window size change cuts draw edges

        n = len(nodes)
        ne = 1000
        data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                                  ('a_fg_color', np.float32, 4),
                                  ('a_bg_color', np.float32, 4),
                                  ('a_size', np.float32, 1),
                                  ('a_linewidth', np.float32, 1)])

        # Testing purposes
        # edges = np.random.randint(size=(ne, 2), low=0,
        #                           high=n).astype(np.uint32)

        # Vertex position
        data['a_position'] = 3.45 * np.hstack((np.random.randn(n, 2), np.zeros((n, 1))))
        # Fill color
        data['a_bg_color'] = np.random.uniform(0.85, 1.00, (n, 4))
        # Overlay, circle color
        data['a_fg_color'] = 0, 0, 0, 1
        # Sets the marker size at a random between 8 and 20 pixels
        data['a_size'] = np.random.randint(size=n, low=8*ps, high=20*ps)
        # Vertex outline width
        data['a_linewidth'] = 1.*ps # sets the marker line thickness
        u_linewidth = 1.0
        u_antialias = 1.0

        self.translate = 5
        self.program = gloo.Program(vert, frag)
        self.view = translate((0, 0, -self.translate))
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)

        self.apply_zoom()

        self.program.bind(gloo.VertexBuffer(data))
        self.program['u_linewidth'] = u_linewidth
        self.program['u_size'] = 5 / self.translate
        self.program['u_antialias'] = u_antialias
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view

        self.theta = 0
        self.phi = 0

        gloo.set_state('translucent', clear_color='white')


    @property
    def visual_size(self):
        return self.physical_size[0] - 40, self.physical_size[1] - 40

    def on_draw(self, event):
        gloo.clear()
        self.context.clear('white')

        self.program.draw('points')

    def apply_zoom(self):
        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
        self.projection = perspective(45.0, self.size[0] /
                                      float(self.size[1]), 1.0, 1000.0)
        self.program['u_projection'] = self.projection

    def on_mouse_wheel(self, event):
        self.translate -= event.delta[1]
        self.translate = max(2, self.translate)
        # move the camera closer when zooming
        self.view = translate((0, 0, -self.translate))

        self.program['u_view'] = self.view
        self.program['u_size'] = 5 / self.translate
        self.update()

if __name__ == '__main__':
    colors = np.empty((100, 3), dtype='float32')
    nodes = np.random.randn(100, 2)
    c = GraphCanvas(nodes)
    c.show()

    app.run()
