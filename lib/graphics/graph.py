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
from vispy.util.transforms import translate
from vispy.gloo import gl

this_dir = op.abspath(op.dirname(__file__))
GLFOLDER = '/glsl/'
FULLPATH = this_dir + GLFOLDER


class Canvas(app.Canvas):
    def __init__(self, edges, node_pos, color=None, **kwargs):
        # Initialize the canvas for real
        app.Canvas.__init__(self, keys='interactive', size=(800, 800),
                            **kwargs)

        # TODO: Refactoring by separating glsl in files and using list for programs
        with open(op.join(FULLPATH, 'n_vert.glsl'), 'rb') as f1:
            n_vert = f1.read().decode('ASCII')
        with open(op.join(FULLPATH, 'n_frag.glsl'), 'rb') as f2:
            n_frag = f2.read().decode('ASCII')
        with open(op.join(FULLPATH, 'e_vert.glsl'), 'rb') as f3:
            e_vert = f3.read().decode('ASCII')
        with open(op.join(FULLPATH, 'e_frag.glsl'), 'rb') as f4:
            e_frag = f4.read().decode('ASCII')
        with open(op.join(FULLPATH, 'a_vert.glsl'), 'rb') as f5:
            a_vert = f5.read().decode('ASCII')
        with open(op.join(FULLPATH, 'a_frag.glsl'), 'rb') as f6:
            a_frag = f6.read().decode('ASCII')

        self.programs = [gloo.Program(n_vert, n_frag),
                         gloo.Program(e_vert, e_frag),
                         gloo.Program(a_vert, a_frag)]

        self.edges = np.array(edges).astype(np.uint32)
        self.node_pos = node_pos

        # Create Index info for the arrowhead buffer
        # arIndex = list(zip(*self.edges))
        # arIndex = list(arIndex[1])

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

############# TESTING CODE!!! ###############################
        # arrow index length must be a multiple of 3
        arIndex = [0, 1, 2, 2, 4]
        array_vert = node_pos[0:6]
        print(array_vert)
        arrow_data = np.zeros(len(array_vert), dtype=[('a_position', np.float32, 3),
                                  ('a_fg_color', np.float32, 4),
                                  ('a_bg_color', np.float32, 4),
                                  ('a_size', np.float32, 1),
                                  ('a_linewidth', np.float32, 1),
                                  ])
        arrow_data['a_position'] = array_vert

        self.vboar = gloo.VertexBuffer(arrow_data)
#############################################################

        data['a_position'] = self.node_pos
        data['a_fg_color'] = 0, 0, 0, 1

        if color is None:
            self.color = np.random.uniform(0.5, 1., (n, 3))
        else:
            self.color = np.array(list(color))
        data['a_bg_color'] = np.hstack((self.color, np.ones((n, 1))))

        # Size of the markers
        data['a_size'] = np.random.randint(size=n, low=8 * ps, high=20 * ps)
        data['a_linewidth'] = 1. * ps
        # Initialize Buffers
        self.vbo = gloo.VertexBuffer(data)
        self.index = gloo.IndexBuffer(self.edges)
        self.arIndex = gloo.IndexBuffer(arIndex)

        # Declare the node and edge programs
        # Initialize Node Program
        self.program_n = self._init_node_program(0)
        # Initialize Edge Program
        self.program_e = self._init_edge_program(1)
        # Initialize Arrowhead Program
        self.program_a = self._init_arrow_program(2)
        # self.program_a['from_xy'] = angle

        # Initialize scale and pan metrics
        for program in self.programs:
            program['u_scale'] = (1., 1., 1.)
            program['u_pan'] = (0., 0., 0.)

        set_state(clear_color='white', depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        set_viewport(0, 0, *self.physical_size)
        self.show()

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_e.draw('lines', self.index)
        self.program_n.draw('points')
        self.program_a.draw('triangles', self.arIndex)

    def on_mouse_move(self, event):
        if event.is_dragging:
            x0, y0 = self._normalize(event.press_event.pos)
            x1, y1 = self._normalize(event.last_event.pos)
            x, y = self._normalize(event.pos)
            dx, dy = x - x1, -(y - y1)
            button = event.press_event.button
            pan_x, pan_y, pan_z = self.program_n['u_pan']
            scale_x, scale_y, scale_z = self.program_n['u_scale']
            (scale_x_new, scale_y_new, scale_z_new) = self.calc_scale(dx)

            if button == 1:
                pan = (pan_x + dx / scale_x, pan_y + dy / scale_y, 1.)
                for program in self.programs:
                    program['u_pan'] = pan

            elif button == 2:
                for program in self.programs:
                    program['u_scale'] = (scale_x_new, scale_y_new, scale_z_new)

            self.update()

    def on_mouse_wheel(self, event):
        """Use the mouse wheel to zoom."""
        dx = np.sign(event.delta[1]) * .05
        (scale_x_new, scale_y_new, scale_z_new) = self.calc_scale(dx)

        for program in self.programs:
            program['u_scale'] = (scale_x_new, scale_y_new, scale_z_new)
        # PENDING: Read pointer position to zoom in place
        # if mouse_coords is not None:  # Record the position of the mouse
        #     x, y = float(mouse_coords[0]), float(mouse_coords[1])
        #     x0, y0 = self.pixel_to_coords(x, y)
        self.update()

    def calc_scale(self, dx=1., dy=1., dz=1.):
        scale_x, scale_y, scale_z = self.program_n['u_scale']
        scale_x_new, scale_y_new, scale_z_new = (scale_x * math.exp(2.5 * dx),
                                                 scale_y * math.exp(2.5 * dx), 1.)
        return (scale_x_new, scale_y_new, scale_z_new)

    def _normalize(self, x_y):
        x, y = x_y
        w, h = float(self.size[0]), float(self.size[1])
        return x / (w / 2.) - 1., y / (h / 2.) - 1.

    def _init_node_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vbo)
        program['u_size'] = 1
        program['u_antialias'] = 1
        program['u_scale'] = self.scale
        return program

    def _init_edge_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vbo)
        program['u_scale'] = self.scale
        return program

    def _init_arrow_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vboar)
        program['size'] = 1.
        program['u_scale'] = self.scale
        return program


if __name__ == '__main__':
    n = 100
    ne = 50
    ed = np.random.randint(size=(ne, 2), low=0,
                           high=n).astype(np.uint32)
    n_p = np.hstack((0.25 * np.random.randn(n, 2),
                     np.zeros((n, 1))))
    # TESTME: For calculations to find line angle
    a = list(zip(*ed))[0]
    # angle = [[n_p[i][0], n_p[i][1]] for i in a]
    c = Canvas(title="Graph", edges=ed, node_pos=n_p)
    app.run()
