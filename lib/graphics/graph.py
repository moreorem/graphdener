#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 60

"""
Dynamic planar graph layout.
"""
import numpy as np
import math
from vispy import gloo, app
from vispy.gloo import set_viewport, set_state, clear
from .util import create_arrowhead, get_segments_pos, set_marker_data
from ..services.actions import Call
from .elements import GlslBridge

SIZE = 20


class Canvas(app.Canvas):
    def __init__(self, edges, node_pos, graphId, color=None, **kwargs):
        # Initialize the canvas for real
        app.Canvas.__init__(self, keys='interactive', **kwargs)
        bridge = GlslBridge()
        self.graphId = graphId
        self.color = color
        self.constants = []
        self.edges = np.array(edges).astype(np.uint32)
        self.node_pos = node_pos
        self.scale = (1., 1., 1.)
        self.translate = 6.5
        print("GRAPH")
        self.programs = [gloo.Program(*bridge.vertgl),
                         gloo.Program(*bridge.edgegl),
                         gloo.Program(*bridge.argl)]

        ps = self.pixel_scale

        # Window position
        self.position = 50, 50
        # Initialize node data
        nodeData = set_marker_data(node_pos, SIZE, self.color, ps)
        """
        VVV--------------- ARROWHEAD PART ----------------VVV
        """
        # arrow index length must be a multiple of 3
        vPos = self.node_pos[:, 0:2].tolist()
        linesAB = get_segments_pos(vPos, self.edges)

        BCD = []
        for line in linesAB:
            B, C, D = create_arrowhead(line[0], line[1])
            BCD.append(B)
            BCD.append(C)
            BCD.append(D)

        # Set vertex number for total of arrowheads
        na = len(BCD)
        arrow_data = np.zeros(na, dtype=[
            ('a_position', np.float32, 2),
            ('a_fg_color', np.float32, 4),
            ('a_bg_color', np.float32, 3),
        ])

        arrow_data['a_position'] = np.array(BCD)

        # Divide arrowhead vertex number by 3 to create color for every three vertices
        col_n = na // 3
        c = np.random.uniform(0.5, 1., (col_n, 3))
        arrow_data['a_bg_color'] = np.repeat(c, [3], axis=0)

        self.vboar = gloo.VertexBuffer(arrow_data)
        """
        ^^^--------------- ARROWHEAD PART END ----------------^^^
        """
        # Initialize Buffers
        self.vbo = gloo.VertexBuffer(nodeData)
        self.index = gloo.IndexBuffer(self.edges)

        # Initialize programs
        self._init_programs()

        # Initialize scale and pan metrics
        for program in self.programs:
            program['u_scale'] = (1., 1., 1.)
            program['u_pan'] = (0., 0., 0.)

        set_state(clear_color='white', depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        set_viewport(0, 0, *self.physical_size)
        self.timer = app.Timer(1/30, connect=self.on_timer)
        self.show()

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_e.draw('lines', self.index)
        self.program_n.draw('points')
        self.program_a.draw('triangles')

    def on_mouse_move(self, event):
        if event.is_dragging:
            x0, y0 = self._normalize(event.press_event.pos)
            x1, y1 = self._normalize(event.last_event.pos)
            x, y = self._normalize(event.pos)
            dx, dy = x - x1, -(y - y1)
            button = event.press_event.button
            pan_x, pan_y, pan_z = self.program_n['u_pan']
            scale_x, scale_y, scale_z = self.program_n['u_scale']
            (scale_x_new, scale_y_new, scale_z_new) = self._calc_scale(dx)

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
        (scale_x_new, scale_y_new, scale_z_new) = self._calc_scale(dx)

        for program in self.programs:
            program['u_scale'] = (scale_x_new, scale_y_new, scale_z_new)
        self.update()

    def on_timer(self, event):
        # Call.apply_alg(self.graphId, 'force directed', *self.constants)

        positions = Call.get_n_pos(self.graphId)
        n = len(positions)
        pos = np.hstack((positions, np.zeros((n, 1))))

        self.vbo.set_data(set_marker_data(pos, SIZE, self.color, self.pixel_scale))
        self.update()

    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()

    def _calc_scale(self, dx=1., dy=1., dz=1.):
        scale_x, scale_y, scale_z = self.program_n['u_scale']
        scale_x_new, scale_y_new, scale_z_new = (scale_x * math.exp(2.5 * dx),
                                                 scale_y * math.exp(2.5 * dx), 1.)
        return (scale_x_new, scale_y_new, scale_z_new)

    def _normalize(self, x_y):
        x, y = x_y
        w, h = float(self.size[0]), float(self.size[1])
        return x / (w / 2.) - 1., y / (h / 2.) - 1.

    def _init_programs(self):
        # Initialize Node Program
        self.program_n = self._init_node_program(0)
        # Initialize Edge Program
        self.program_e = self._init_edge_program(1)
        # Initialize Arrowhead Program
        self.program_a = self._init_arrow_program(2)

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
    n = 1000000
    ne = 50000
    ed = np.random.randint(size=(ne, 2), low=0,
                           high=n).astype(np.uint32)
    n_p = np.hstack((20.25 * np.random.randn(n, 2),
                     np.zeros((n, 1))))
    vPos = n_p[:, 0:2].tolist()
    c = Canvas(title="Graph", edges=ed, node_pos=n_p)
    app.run()
