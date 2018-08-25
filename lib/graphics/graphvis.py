# -*- coding: utf-8 -*-

"""
Graph that consists of markers and lines visuals
"""
import numpy as np
from vispy import app, visuals
from vispy.visuals.transforms import STTransform
from vispy.util.transforms import rotate
from ..services.actions import Call

n = 486
pos = np.zeros((n, 2))
colors = np.ones((n, 4), dtype=np.float32)
radius, theta, dtheta = 1.0, 0.0, 5.5 / 180.0 * np.pi
for i in range(486):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.1 - i * 0.02
    radius -= 0.45
    pos[i] = x, y
    colors[i] = (i / 500, 1.0 - i / 500, 0, 1)

nodes = pos

N = 200
epos = np.zeros((N, 2), dtype=np.float32)
epos[:, 0] = np.linspace(10, 390, N)
epos[:, 1] = np.random.normal(size=N, scale=20, loc=0)


class GraphCanvas(app.Canvas):
    def __init__(self, parent=None):
        app.Canvas.__init__(self, keys='interactive', app='PyQt5',
                            size=(640, 480), title="Graph Visualization")

        self.index = 0
        self.markers = visuals.MarkersVisual()
        # FIXME: Correct colors array shape
        self.markers.set_data(nodes, face_color=colors)
        self.markers.symbol = 'o'
        self.markers.transform = STTransform()
        self.lines = [
            # visuals.LineVisual(pos=epos, color=(0, 0.5, 0.3, 1),
            #                    connect='segments', method='gl')
            visuals.LineVisual(pos=pos, color=(0, 0.5, 0.3, 1), width=5,
                               method='agg'),
        ]

        counts = [0, 0]

        for i, line in enumerate(self.lines):
            # arrange lines in a grid
            tidx = (line.method == 'agg')
            x = tidx
            y = (counts[tidx] + 1)
            counts[tidx] += 1
            line.transform = STTransform(translate=[x, y])
            # redraw the canvas if any visuals request an update
            line.events.update.connect(lambda evt: self.update())

        self.visuals = self.lines + [self.markers]
        self.theta = 0
        self.phi = 0
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

        # Gather positions from backend
        self.set_node_pos()

        self.show()

    def on_draw(self, event):
        self.context.clear(color='white')
        for visual in self.visuals:
            visual.draw()

    def on_mouse_wheel(self, event):
        """Use the mouse wheel to zoom."""
        for visual in self.visuals:
            visual.transform.zoom((1.25**event.delta[1],) * 2,
                                  center=event.pos)
        self.update()

    def on_resize(self, event):
        # Set canvas viewport and reconfigure visual transforms to match.
        vp = (0, 0, self.physical_size[0], self.physical_size[1])
        self.context.set_viewport(*vp)
        for visual in self.visuals:
            visual.transforms.configure(canvas=self, viewport=vp)

    def on_mouse_move(self, event):
        if event.is_dragging:
            dxy = event.pos - event.last_event.pos
            button = event.press_event.button

            if button == 1:
                for visual in self.visuals:
                    visual.transform.move(dxy)
            # elif button == 2:
            #     center = event.press_event.pos
            #     self.markers.transform.zoom(np.exp(dxy * (0.01, -0.01)),
            #         center)

            self.update()

    def on_timer(self, event):
        self.theta += .5
        self.phi += .5
        self.model = np.dot(rotate(self.theta, (0, 1, 0)),
                            rotate(self.phi, (0, 0, 1)))
        # self.program['u_model'] = self.model
        # for markers Call "unfreeze()" to allow addition of new attributes
        self.update()

    def on_key_press(self, event):
        pass
        # if event.text == ' ':
        #     self.index = (self.index + 1) % (len(visuals.marker_types))
        #     self.markers.symbol = visuals.marker_types[self.index]
        #     self.update()
        # elif event.text == 's':
        #     self.markers.scaling = not self.markers.scaling
        #     self.update()

    # TODO: Add on_mouse point event to hover above each node and show
    # the corresponding label
    def set_node_pos(self):
        pos = np.matrix(Call.get_positions())
        self.markers.set_data(pos, face_color=colors)




if __name__ == '__main__':
    canvas = GraphCanvas(nodes)
    app.run()
