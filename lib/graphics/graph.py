#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 60

"""
Dynamic planar graph layout.
"""
import math
from os import path as op
import numpy as np
from vispy import gloo, app
from vispy.gloo import set_viewport, set_state, clear
from vispy.util.transforms import perspective, translate, rotate
from vispy import geometry

this_dir = op.abspath(op.dirname(__file__)) + '/glsl/'


class Canvas(app.Canvas):
    def __init__(self, edges, node_pos, **kwargs):
        # Initialize the canvas for real
        app.Canvas.__init__(self, keys='interactive', size=(1024, 1024),
                            **kwargs)
        # TODO: Refactoring by separating glsl in files and using list for programs
        with open(op.join(this_dir, 'n_vert.glsl'), 'rb') as f1:
            n_vert = f1.read().decode('ASCII')
        with open(op.join(this_dir, 'n_frag.glsl'), 'rb') as f2:
            n_frag = f2.read().decode('ASCII')
        with open(op.join(this_dir, 'e_vert.glsl'), 'rb') as f3:
            e_vert = f3.read().decode('ASCII')
        with open(op.join(this_dir, 'e_frag.glsl'), 'rb') as f4:
            e_frag = f4.read().decode('ASCII')
        with open(op.join(this_dir, 'a_vert.glsl'), 'rb') as f5:
            a_vert = f5.read().decode('ASCII')
        with open(op.join(this_dir, 'a_frag.glsl'), 'rb') as f6:
            a_frag = f6.read().decode('ASCII')

        self.programs = [gloo.Program(n_vert, n_frag),
                         gloo.Program(e_vert, e_frag),
                         gloo.Program(a_vert, a_frag)]

        self.edges = np.array(edges).astype(np.uint32)
        self.node_pos = node_pos
        ps = self.pixel_scale
        self.scale = (1., 1., 1.)
        self.translate = 6.5
        n = len(node_pos)
        # Window position
        self.position = 50, 50
        # Initialize node data
        data = np.zeros(n, dtype=[('a_position', np.float32, 3),
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
        data['a_size'] = np.random.randint(size=n, low=8 * ps, high=20 * ps)
        data['a_linewidth'] = 1. * ps

        self.vbo = gloo.VertexBuffer(data)
        self.index = gloo.IndexBuffer(self.edges)
        self.view = translate((0, 0, 0))
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)

        # Declare the node and edge programs
        self.program = self._init_node_program(0)
        self.center = self.program["center"] = [-0.5, 0]

        self.program_e = self._init_edge_program(1)
        self.program_a = self._init_arrow_program(2)

        set_state(clear_color='white', depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        set_viewport(0, 0, *self.physical_size)
        self.show()

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        # self.program_a.draw('triangles', self.index)
        self.program_e.draw('lines', self.index)
        self.program.draw('points')

    def on_mouse_move(self, event):
        if event.is_dragging:
            dxy = event.pos - event.last_event.pos
            button = event.press_event.button
            if button == 1:
                self.model = self.model.dot(translate((dxy[0] * 0.001, dxy[1] * (-0.001), 0)))
                self.program['u_model'] = self.model
                self.program_e['u_model'] = self.model

            self.update()

    # PENDING: Replace with correct values as well as in the shaders
    def on_mouse_wheel(self, event):
        """Use the mouse wheel to zoom."""
        print(event.modifiers)
        delta = event.delta[1]
        print(delta)

        if delta > 0:  # Zoom in
            factor = 0.9
        elif delta < 0:  # Zoom out
            factor = 1 / 0.9
        for _ in range(int(abs(delta))):
            if not event.modifiers:
                self.zoom(factor)
            else:
                self.zoom(factor, event.pos)

        dx = np.sign(event.delta[1]) * .05
        # print(event.pos)
        scale_x, scale_y, scale_z = self.program['u_scale']
        scale_x_new, scale_y_new, scale_z_new = (scale_x * math.exp(2.5 * dx),
                                                 scale_y * math.exp(2.5 * dx), 1.)
        self.program['u_scale'] /= factor
        # (max(1, scale_x_new), max(1, scale_y_new), 1.)
        self.program_e['u_scale'] /= factor
        # (max(1, scale_x_new), max(1, scale_y_new), 1.)
        print(self.program['u_scale'])

        self.update()

    # FIXME: Read pointer position to zoom in place
    def zoom(self, factor, mouse_coords=None):
        """Factors less than zero zoom in, and greater than zero zoom out.
        If mouse_coords is given, the point under the mouse stays stationary
        while zooming. mouse_coords should come from MouseEvent.pos.
        """
        if mouse_coords is not None:  # Record the position of the mouse
            x, y = float(mouse_coords[0]), float(mouse_coords[1])
            x0, y0 = self.pixel_to_coords(x, y)

        # Translate so the mouse point is stationary
        # if mouse_coords is not None:
        #     x1, y1 = self.pixel_to_coords(x, y)
        #     self.translate_center(x1 - x0, y1 - y0)


    def translate_center(self, dx, dy):
        """Translates the center point, and keeps it in bounds."""
        center = self.center
        center[0] -= dx
        center[1] -= dy
        center[0] = min(max(center[0], self.bounds[0]), self.bounds[1])
        center[1] = min(max(center[1], self.bounds[0]), self.bounds[1])
        self.program["center"] = self.center = center

    def pixel_to_coords(self, x, y):
        """Convert pixel coordinates to Mandelbrot set coordinates."""
        rx, ry = self.size
        nx = (x / rx - 0.5) + self.center[0]
        ny = ((ry - y) / ry - 0.5) + self.center[1]
        print(self.center)
        return [nx, ny]


    def _init_node_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vbo)
        program['u_size'] = 1
        program['u_antialias'] = 1
        program['u_model'] = self.model
        program['u_view'] = self.view
        program['u_scale'] = self.scale
        program['u_projection'] = self.projection

        return program

    def _init_edge_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vbo)
        program['u_model'] = self.model
        program['u_view'] = self.view
        program['u_scale'] = self.scale
        program['u_projection'] = self.projection

        return program

    def _init_arrow_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vbo)
        program['size'] = 1.
        program['linewidth'] = 1.
        program['v1'] = self.model
        program['v2'] = np.array(self.node_pos).astype(np.float32)
        program['u_scale'] = self.scale
        program['u_projection'] = self.projection

        return program


if __name__ == '__main__':
    n = 100
    ne = 50
    ed = np.random.randint(size=(ne, 2), low=0,
                           high=n).astype(np.uint32)
    n_p = np.hstack((0.25 * np.random.randn(n, 2),
                     np.zeros((n, 1))))
    c = Canvas(title="Graph", edges=ed, node_pos=n_p)
    app.run()
