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

data = [[1, 2], [5, 4], [1, 4], [2, 6], [3, 4]]
print(set(data[0]))

# Initialize arrays for position, color, edges, and types for each point in
# the graph.
npts = 100
nedges = 20
ngroups = 1
np.random.seed(127396)
pos = np.empty((npts, 2), dtype='float32')
colors = np.empty((npts, 3), dtype='float32')
edges = np.empty((nedges, 2), dtype='uint32')
types = np.empty(npts, dtype=int)

# Assign random starting positions
pos[:] = np.random.normal(size=pos.shape, scale=4.)

# Assign each point to a group
grpsize = npts // ngroups
ptr = 0
typ = 0
while ptr < npts:
    size = np.random.random() * grpsize + grpsize // 2
    types[int(ptr):int(ptr+size)] = typ
    typ += 1
    ptr = ptr + size

# Randomly select connections, with higher connection probability between
# points in the same group
conn = []
connset = set()
while len(conn) < nedges:
    i, j = np.random.randint(npts, size=2)
    if i == j:
        continue
    p = 0.7 if types[i] == types[j] else 0.01
    if np.random.random() < p:
        if (i, j) in connset:
            continue
        connset.add((i, j))
        connset.add((j, i))
        conn.append([i, j])
# Edges are stored as an edge list
edges[:] = conn

# Uses edge list as indexes to create pairs of x,y coordinates for the edge lines and connect pair of nodes
connections = np.array([[pos[i] for i in edges[j]] for j in range(len(edges))])

# Assign colors to each point based on its type
cmap = color.get_colormap('cubehelix')
typ_colors = np.array([cmap.map(x)[0, :3] for x in np.linspace(0.2, 0.8, typ)])
colors[:] = typ_colors[types]

# Add some RGB noise and clip
colors *= 1.1 ** np.random.normal(size=colors.shape)
colors = np.clip(colors, 0, 1)


class GraphCanvas(app.Canvas):
    def __init__(self, **kwargs):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))
        ps = self.pixel_scale
        # TODO: Lines made using agg, that can have variable width
        # lines = scene.Line(pos=pos, width=1., antialias=True, method='agg',
        #                    color=(1, 1, 1, 0.8), parent=view.scene)
        global connections, pos, edges, lines, markers, view, force, dist, i

        # Draw edge connections between nodes
        self.lines = Line(pos=connections, width=2., connect='segments',
                           antialias=False, method='gl',
                           color=(1, 0, 1, 1))

        # Draw node markers
        self.markers = Markers(pos=pos, face_color=colors, symbol='o')


        dx = np.empty((npts, npts, 2), dtype='float32')
        dx[:] = pos[:, np.newaxis, :]
        dx -= pos[np.newaxis, :, :]

        dist = (dx**2).sum(axis=2)**0.5
        dist[dist == 0] = 1.
        ndx = dx / dist[..., np.newaxis]

        force = np.zeros((npts, npts, 2), dtype='float32')

        # all points push away from each other
        force -= 0.1 * ndx / dist[..., np.newaxis]**2

        # connected points pull toward each other
        # pulsed force helps to settle faster:
        s = 0.1
        # s = 0.05 * 5 ** (np.sin(i/20.) / (i/100.))

        # s = 0.05 + 1 * 0.99 ** i
        mask = np.zeros((npts, npts, 1), dtype='float32')
        mask[edges[:, 0], edges[:, 1]] = s
        mask[edges[:, 1], edges[:, 0]] = s
        force += dx * dist[..., np.newaxis] * mask

        # points do not exert force on themselves
        force[np.arange(npts), np.arange(npts)] = 0

        force = force.sum(axis=0)
        pos += np.clip(force, -2, 2) * 0.02

        self.lines.set_data(pos=connections)
        self.markers.set_data(pos=pos, face_color=colors)

        i += 1
        # segments = SegmentCollection("agg", linewidth="local")
        # n = 100
        # P0 = np.dstack(
        #     (np.linspace(100, 1100, n), np.ones(n) * 50, np.zeros(n))).reshape(n, 3)
        # P0 = 2 * (P0 / (1200, 600, 1)) - 1
        # P1 = np.dstack(
        #     (np.linspace(110, 1110, n), np.ones(n) * 550, np.zeros(n))).reshape(n, 3)
        # P1 = 2 * (P1 / (1200, 600, 1)) - 1

        # segments.append(P0, P1, linewidth=np.linspace(1, 8, n))

        # scene.camera.set_range()


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
    # view = canvas.central_widget.add_view()
    # view.camera = 'panzoom'
    # view.camera.aspect = 1
    app.run()

