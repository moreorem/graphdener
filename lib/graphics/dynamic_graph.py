# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
"""
Plot clusters of data points and a graph of connections
"""
from vispy import app, scene, color
from vispy.scene.visuals import Line, Markers
import numpy as np
from vispy.visuals.collections import SegmentCollection
from vispy.visuals.transforms import STTransform

import visuals.graph_node as vis

n = 500
pos = np.zeros((n, 2))
colors = np.ones((n, 4), dtype=np.float32)
radius, theta, dtheta = 1.0, 0.0, 5.5 / 180.0 * np.pi
for i in range(500):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.1 - i * 0.02
    radius -= 0.45
    pos[i] = x, y
    colors[i] = (i/500, 1.0-i/500, 0, 1)

class GraphCanvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, keys='interactive', size=(512, 512),
                            title="Testing graph vertex visual")
        self.index = 0
        self.nodes = vis.GNodeVisual()
        self.nodes.set_data(pos, face_color=colors)
        self.nodes.symbol = vis.marker_types[self.index]
        self.nodes.transform = STTransform()

        self.show()

    def on_draw(self):
        pass


    # Activates in each timer tick
    # def update(self, event=None):
    #     if self._backend is not None:
    #         self._backend._vispy_update()
        # @canvas.connect
        # def on_mouse_move(event):
        #     print_mouse_event(event, 'Mouse move')

    def print_mouse_event(event, what):
        modifiers = ', '.join([key.name for key in event.modifiers])
        print('%s - pos: %r, button: %s, modifiers: %s, delta: %r' %
        (what, event.pos, event.button, modifiers, event.delta))


    timer = app.Timer(interval=0, connect=on_draw, start=True)

if __name__ == '__main__':
    # Display the data
    canvas = GraphCanvas()

    app.run()
