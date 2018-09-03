# from ..graphics.graphvis import GraphCanvas
from ..graphics.graph import Canvas
from PyQt5.QtWidgets import (QWidget, QGridLayout)
from ..services.actions import Call
import numpy as np
from .. import func

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
        # canvas = GraphCanvas().native

        result = Call.get_vert('pos')

        v = [eval(x) for x in result]
        va = np.array(v)
        ve = np.hstack((va, np.zeros((len(v), 1))))
        print(ve)
        ed = [] #Call.get_edge('pos')
        print(ed)
        canvas = Canvas(title='Graphdener Visualizer', edges=ed, node_pos=ve).native

        self.grid.addWidget(canvas, gridslot[0], gridslot[1])
        self.n += 1
        # self.grid.
        # TODO: Improve grid_iteration in order to iterate once in every canvas creation
