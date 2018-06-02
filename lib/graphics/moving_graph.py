# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
"""
Plot clusters of data points and a graph of connections
"""
from vispy import app, scene, color, gloo
import numpy as np
from vispy.visuals.collections import SegmentCollection

data = [[1, 2], [5, 4], [1, 4], [2, 6], [3, 4]]
print(set(data[0]))
# a = tuple(zip(*list(set(data))))

print(a)
quit()
# Initialize arrays for position, color, edges, and types for each point in
# the graph.
npts = 8
nedges = 2
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

# Assign colors to each point based on its type
cmap = color.get_colormap('cubehelix')
typ_colors = np.array([cmap.map(x)[0, :3] for x in np.linspace(0.2, 0.8, typ)])
colors[:] = typ_colors[types]

# Add some RGB noise and clip
colors *= 1.1 ** np.random.normal(size=colors.shape)
colors = np.clip(colors, 0, 1)

# Add segment collection
segments = SegmentCollection("agg", linewidth="local")

# Display the data
canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='white')
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.aspect = 1

# Lines made using agg, that can have variable width
# lines = scene.Line(pos=pos, width=1., antialias=True, method='agg',
#                    color=(1, 1, 1, 0.8), parent=view.scene)
print(edges[0])
print(pos[5], pos[3])

print([ [ j for j in i] for i in edges] )

a = np.vstack([ [ list(zip(pos[j])) for j in i ] for i in edges])

print(a)
print(a.shape)
# print(np.vstack([np.array(i) for i in edges]) )
# print( np.vstack([ np.array(i) for i in edges ]) )

# print([ [ pos[j] for j in i] for i in edges[i] [:] ])

# print(list(np.array(pos)[edges][0]))
print(np.array((7.3297157, 6.3043547)))

# quit()
# Standard lines of width 1
lines = scene.Line(pos=np.array( [[(-2.3609583, 3.546692),(7.3297157, 6.3043547)], [(-2.1943018, -2.402215), (-2.325184, -1.6532228)]] )
    , width=5., connect='segments', antialias=True, method='gl',
                   color=(1, 0, 1, 1), parent=view.scene)

markers = scene.Markers(pos=pos, face_color=colors, symbol='o',
                        parent=view.scene)

view.camera.set_range()

# i = 1


# self.set_state(clear_color='white', depth_test=False, blend=True,
#                   blend_func=('src_alpha', 'one_minus_src_alpha'))



@canvas.connect
def on_draw(e):
    gloo.clear('white')
    segments.draw()

def update(ev):
    global pos, edges, lines, markers, view, force, dist, i

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
    #s = 0.05 * 5 ** (np.sin(i/20.) / (i/100.))

    #s = 0.05 + 1 * 0.99 ** i
    mask = np.zeros((npts, npts, 1), dtype='float32')
    mask[edges[:, 0], edges[:, 1]] = s
    mask[edges[:, 1], edges[:, 0]] = s
    force += dx * dist[..., np.newaxis] * mask

    # points do not exert force on themselves
    force[np.arange(npts), np.arange(npts)] = 0

    force = force.sum(axis=0)
    pos += np.clip(force, -3, 3) * 0.09

    lines.set_data(pos=pos)
    markers.set_data(pos=pos, face_color=colors)

    i += 1

@canvas.connect
def on_mouse_move(event):
    print_mouse_event(event, 'Mouse move')

def print_mouse_event(event, what):
    modifiers = ', '.join([key.name for key in event.modifiers])
    print('%s - pos: %r, button: %s, modifiers: %s, delta: %r' %
  (what, event.pos, event.button, modifiers, event.delta))


# timer = app.Timer(interval=0, connect=update, start=True)

if __name__ == '__main__':
    app.run()
