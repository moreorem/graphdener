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
    gl_Position = u_projection * u_view * u_model *
        vec4(a_position*u_size,1.0);
    gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""

frag = """
#version 120

// Constants
// ------------------------------------

// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

// Functions
// ------------------------------------
float marker(vec2 P, float size);


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
}

float marker(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}
"""

vs = """
attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

void main(){
    gl_Position = vec4(a_position, 1.);
}
"""

# Declares edge line color
fs = """
void main(){
    gl_FragColor = vec4(0., 0., 0., 1.);
}
"""


class GraphCanvas(app.Canvas):
    def __init__(self, nodes):
        # Initialize the canvas for real
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))
        # app.Canvas.__init__(self, keys='interactive', size=(1024, 1024),
        #                     **kwargs)
        ps = self.pixel_scale
        # Window position
        self.position = 50, 50

        # TODO: create array from node type to insert as a_bg_color
        # FIXME: Window size change cuts draw edges

        n = len(nodes)
        ne = 1000
        data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                                  ('a_fg_color', np.float32, 4),
                                  ('a_bg_color', np.float32, 4),
                                  ('a_size', np.float32, 1),
                                  ('a_linewidth', np.float32, 1),
                                  ])
        edges = np.random.randint(size=(ne, 2), low=0,
                                  high=n).astype(np.uint32)

        # Vertex position
        data['a_position'] = np.hstack((nodes,
                                       np.zeros((n, 1))))
        self.markers = Markers(pos=data['a_position'], face_color=colors, symbol='o')

        # Overlay, circle color
        data['a_fg_color'] = 0, 0, 0, 1
        # Fill color
        color = np.random.uniform(0.5, 1., (n, 3))
        data['a_bg_color'] = np.hstack((color, np.ones((n, 1))))
        # Vertex size
        # Sets the marker size at a random between 8 and 20 pixels
        data['a_size'] = np.random.randint(size=n, low=8*ps, high=20*ps)
        # Vertex outline width
        data['a_linewidth'] = 1.*ps # sets the marker line thickness
        u_antialias = 1

        self.vbo = gloo.VertexBuffer(data)
        self.index = gloo.IndexBuffer(edges)
        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)

        self.program = gloo.Program(vert, frag)
        self.program.bind(self.vbo)
        self.program['u_size'] = 1
        self.program['u_antialias'] = u_antialias
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view
        self.program['u_projection'] = self.projection

        set_viewport(0, 0, *self.physical_size)

        # Create object to attach vertex and fragment shaders
        self.program_e = gloo.Program(vs, fs)
        # Bind the edges to the vertex data
        self.program_e.bind(self.vbo)

        set_state(clear_color='white', depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))

        self.show()

    # def on_resize(self, event):
    #     set_viewport(0, 0, *event.physical_size)

    def on_resize(self, event):
        # self.visual.transform.scale = self.visual_size
        # set_vset_viewport(0, 0, *event.physical_size)iewport(0, 0, *event.physical_size)
        vp = (0, 0, self.physical_size[0], self.physical_size[1])
        self.set_viewport(*vp)
        # self.visual.transforms.configure(canvas=self, viewport=vp)

        self.apply_zoom()

    @property
    def visual_size(self):
        return self.physical_size[0] - 40, self.physical_size[1] - 40

    def on_draw(self, event):
        gloo.clear()
        self.context.clear('white')
        # self.visual.draw()
        # if not self.visual.animate_layout():
            # self.update()

        # Paint background
        # clear(color=True, depth=True)
        # # Draw lines with array of indices
        # print(self.index)
        self.program_e.draw('lines', self.index)
        self.program.draw('points')

        # # Draw points
        # self.program.draw('points')


if __name__ == '__main__':
    colors = np.empty((100, 3), dtype='float32')
    nodes = np.random.randint(size=(100, 2), low=0,
                                  high=1000).astype(np.uint32)
    c = GraphCanvas(nodes)
    app.run()
