from ..graphics.graph import Canvas
from PyQt5.QtWidgets import (QWidget, QGridLayout)
from ..services.actions import Call
import numpy as np
from .. import func

COLOR_LIST = [(255, 228, 196), (139, 137, 137), (255, 250, 205),
                (230, 230, 250), (49, 79, 79), (100, 149, 237),
                (0, 0, 205), (0, 191, 255), (70, 130, 180),
                (64, 224, 208), (0, 100, 0), (127, 255, 0),
                (50, 205, 50), (107, 142, 35), (255, 255, 0),
                (218, 165, 32), (205, 92, 92), (244, 164, 96),
                (178, 34, 34), (250, 128, 114), (255, 0, 0),
                (255, 20, 147), (186, 85, 211), (138, 43, 226),
                (147, 112, 219)]


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
        gridslot = self.gridslot[self.n]

        result = Call.get_vert('pos')

        v = [eval(x) for x in result]
        va = np.array(v)
        ve = np.hstack((va, np.zeros((len(v), 1))))
        ed = Call.get_edge('pos')

        types = Call.get_vert('type')
        c_types = self._create_colors(types)
        c_types = tuple(c_types.values())
        print(c_types)

        canvas = Canvas(title='Graphdener Visualizer', edges=ed, node_pos=ve, colors=c_types).native

        self.grid.addWidget(canvas, gridslot[0], gridslot[1])
        self.n += 1
        # TODO: Improve grid_iteration in order to iterate once in every canvas creation

    def _create_colors(self, types):
        variety = list(set(types))
        color_types = {}
        i = 0
        for t in variety:
            color_types[t] = COLOR_LIST[i]
            i += 1
        return color_types
