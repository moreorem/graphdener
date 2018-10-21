#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 60

"""
Dynamic planar graph layout.
"""
import numpy as np
import math
from vispy import gloo
from vispy.app import Canvas, Timer
from vispy.gloo import set_viewport, set_state, clear
from .util import set_marker_data
from ..services.actions import Call
from .elements import GlslBridge, ArrowHead
from ..statics import MARKER_SIZE, FRAME_CAP
import threading
import time


class Graph(Canvas):
    def __init__(self, edges, node_pos, graphId, color=None, **kwargs):
        # Initialize the canvas for real
        Canvas.__init__(self, keys='interactive', **kwargs)
        bridge = GlslBridge()
        self.graphId = graphId
        self.color = color
        self.constants = []
        self.edges = np.array(edges).astype(np.uint32)
        self.node_pos = node_pos
        self.scale = (1., 1., 1.)

        self.programs = [gloo.Program(*bridge.vertgl),
                         gloo.Program(*bridge.edgegl),
                         gloo.Program(*bridge.argl)]

        ps = self.pixel_scale

        # Window position
        self.position = 50, 50
        # Initialize node data
        nodeData = set_marker_data(node_pos, MARKER_SIZE, self.color, ps)

        self.arrows = ArrowHead(node_pos, self.edges, MARKER_SIZE)

        # Initialize Buffers
        self.vbo = gloo.VertexBuffer(nodeData)
        self.index = gloo.IndexBuffer(self.edges)
        self.vboar = gloo.VertexBuffer(self.arrows.getArrowData())

        # Initialize programs
        self._init_programs()

        # Initialize scale and pan metrics
        for program in self.programs:
            program['u_scale'] = (1., 1., 1.)
            program['u_pan'] = (0., 0., 0.)

        set_state(clear_color='white', depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        set_viewport(0, 0, *self.physical_size)
        self.timer = Timer(1 / FRAME_CAP, connect=self.on_timer)
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
        # PENDING: Call algorithm on every tic and on different thread
        Call.apply_alg()
        positions = Call.get_n_pos()
        n = len(positions)
        pos = np.hstack((positions, np.zeros((n, 1))))

        self.vbo.set_data(set_marker_data(pos, MARKER_SIZE, self.color, self.pixel_scale))
        self.arrows.setArrowPos(pos, self.edges)
        self.vboar.set_data(self.arrows.getArrowData())
        self.update()

    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()

    def animate(self):
        if self.timer.running:
            self.timer.stop()
        else:
            # Maybe spawn a thread with a while timer loop to call algorithm
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
        program['a_size'] = MARKER_SIZE
        program['u_size'] = 1
        program['u_antialias'] = 1
        program['u_scale'] = self.scale
        return program

    def _init_edge_program(self, idx):
        program = self.programs[idx]
        program['opacity'] = 0.9
        program.bind(self.vbo)
        program['u_scale'] = self.scale
        return program

    def _init_arrow_program(self, idx):
        program = self.programs[idx]
        program.bind(self.vboar)
        program['u_scale'] = self.scale
        return program

    def test(self, delay):
        while(self.timer.running):
            print("Call Algorithm")
            time.sleep(delay)
