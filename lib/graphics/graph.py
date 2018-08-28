#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 60

"""
Dynamic planar graph layout.
"""

import numpy as np
from vispy import gloo, app
from vispy.gloo import set_viewport, set_state, clear
from vispy.util.transforms import perspective, translate, rotate


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
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    // Line width of the markers
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

# Vertex shader for edges
vs = """
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

void main(){
    gl_Position = u_view * u_model * u_projection * vec4(a_position, 1.);
}
"""
# Fragment shader for edges
fs = """
void main(){
    gl_FragColor = vec4(0., 0., 0., 1.);
}
"""


class Canvas(app.Canvas):
    def __init__(self, edges, node_pos, **kwargs):
        # Initialize the canvas for real
        app.Canvas.__init__(self, keys='interactive', size=(1024, 1024),
                            **kwargs)
        self.edges = np.array(edges).astype(np.uint32)
        self.node_pos = node_pos
        ps = self.pixel_scale
        n = len(node_pos)
        # Window position
        self.position = 50, 50
        data = np.zeros(n, dtype=[('a_position', np.float32, 4),
                                  ('a_fg_color', np.float32, 4),
                                  ('a_bg_color', np.float32, 4),
                                  ('a_size', np.float32, 1),
                                  ('a_linewidth', np.float32, 1),
                                  ])

        data['a_position'] = self.node_pos
        data['a_fg_color'] = 0, 0, 0, 1
        color = np.random.uniform(0.5, 1., (n, 3))
        data['a_bg_color'] = np.hstack((color, np.ones((n, 1))))
        # Size of the markers
        data['a_size'] = np.random.randint(size=n, low=8*ps, high=20*ps)
        data['a_linewidth'] = 1.*ps

        u_antialias = 1

        self.vbo = gloo.VertexBuffer(data)
        self.index = gloo.IndexBuffer(self.edges)
        # self.view = np.eye(4, dtype=np.float32)
        self.view = translate((0, 0, 0))
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

        self.program_e = gloo.Program(vs, fs)
        self.program_e.bind(self.vbo)

        self.program_e['u_model'] = self.model
        self.program_e['u_view'] = self.view

        self.program_e['u_projection'] = self.projection

        set_state(clear_color='white', depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        self.show()

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_e.draw('lines', self.index)
        self.program.draw('points')

    def on_mouse_move(self, event):
        if event.is_dragging:
            dxy = event.pos - event.last_event.pos
            button = event.press_event.button
            if button == 1:

                self.model = self.model.dot(translate((dxy[0]*0.001,dxy[1]*(-0.001),0)))
                self.program['u_model'] = self.model
                self.program_e['u_model'] = self.model
                # self.program.bind(gloo.VertexBuffer(data))
            self.update()


    # PENDING: Replace with correct values as well as in the shaders
    def on_mouse_wheel(self, event):
        """Use the mouse wheel to zoom."""
        print(event.modifiers)
        delta = event.delta[1]
        if delta > 0:  # Zoom in
            factor = 0.9
        elif delta < 0:  # Zoom out
            factor = 1 / 0.9
        for _ in range(int(abs(delta))):
            if not event.modifiers:
                self.zoom(factor)
            else:
                self.zoom(factor, event.pos)


    # PENDING: Replace with correct values as well as in the shaders
    def zoom(self, factor, mouse_coords=None):
        """Factors less than zero zoom in, and greater than zero zoom out.
        If mouse_coords is given, the point under the mouse stays stationary
        while zooming. mouse_coords should come from MouseEvent.pos.
        """
        if mouse_coords is not None:  # Record the position of the mouse
            x, y = float(mouse_coords[0]), float(mouse_coords[1])
            x0, y0 = self.pixel_to_coords(x, y)

        self.scale *= factor
        self.scale = max(min(self.scale, self.max_scale), self.min_scale)
        self.program["scale"] = self.scale

        # Translate so the mouse point is stationary
        if mouse_coords is not None:
            x1, y1 = self.pixel_to_coords(x, y)
            self.translate_center(x1 - x0, y1 - y0)


if __name__ == '__main__':
    n = 100
    ne = 50
    ed = np.random.randint(size=(ne, 2), low=0,
                                  high=n).astype(np.uint32)
    n_p = np.hstack((.25 * np.random.randn(n, 2),
                                    np.zeros((n, 2))))
    c = Canvas(title="Graph", edges=ed, node_pos = n_p)
    app.run()
