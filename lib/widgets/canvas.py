from ..graphics.graph import Canvas
from PyQt5.QtWidgets import (QWidget, QGridLayout)
from ..services.actions import Call
import numpy as np
from .. import func
from lib import statics


class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.canvas = None
        self.n = 0
        self.gridslot = [i for i in func.iterate_grid(2)]

    def __controls(self):
        self.canvasWidget = QWidget()

    def __layout(self):
        self.grid = QGridLayout()

    def get_layout(self):
        return self.grid

    def close_canvas(self):
        self.canvas.close()
        self.grid.removeWidget(self.canvas)
        self.canvas = None

    def create_canvas(self):
        # FIXME: When pressing redraw button the interface corrupts
        # if self.canvas is not None:
        #     self.close_canvas()
        # PENDING: When a new canvas is being added, shrinken previous and add a new one on the side
        # PENDING: Get canvas id from current canvas

        if self.n > 0:
             self.close_canvas()
        canvas_id = 1

        # TODO: Add this method to create_colors and store the correspondence to a dictionary['type'] = color
        # v_color = np.random.uniform(0, 1, (n_types, 3)).astype(np.float32)
        # TODO: Define node size according to the number of edges connected to it

        result = Call.get_vert('pos', canvas_id)

        v = [eval(x) for x in result]
        va = np.array(v)
        ve = np.hstack((va, np.zeros((len(v), 1))))
        ed = Call.get_edge('pos', canvas_id)

        types = Call.get_vert('type', canvas_id)
        c_types = self._create_colors(types)
        # Create the color for each node
        col = [c_types[t] for t in types]

        self.canvas = Canvas(title='Graphdener Visualizer', edges=ed, node_pos=ve, color=col).native

        gridslot = self.gridslot[self.n]

        self.grid.addWidget(self.canvas, gridslot[0], gridslot[1])
        self.n += 1
        # TODO: Improve grid_iteration in order to iterate once in every canvas creation

    def _create_colors(self, types):
        t = list(set(types))
        rgb_palette = np.random.uniform(0, 1, (len(t), 3)).astype(np.float32)
        color_types = dict(zip(t, rgb_palette))

        return color_types
