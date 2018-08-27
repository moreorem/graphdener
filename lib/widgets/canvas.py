from ..graphics.graphvis import GraphCanvas
from PyQt5.QtWidgets import (QWidget, QGridLayout)
# from ..services.actions import Call
import numpy as np
from .. import func

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.canvas = None
        self.gridslot = next(func.iterate_grid(2))

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
        # self.gridslot = next(func.iterate_grid(2))
        canvas = GraphCanvas().native
        self.grid.addWidget(canvas, self.gridslot[0], self.gridslot[1])

        # TODO: Improve grid_iteration in order to iterate once in every canvas creation

        return canvas

