from ..graphics.graphvis import GraphCanvas
# from ..graphics.graph import GraphCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from ..services.actions import Call
import numpy as np

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.canvas = None
        self.gridslot = [0,0]

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
            colors[i] = (i / 500, 1.0 - i / 500, 0, 1)
        self.canvas = GraphCanvas(pos, colors).native
        self.grid.addWidget(self.canvas, self.gridslot[0], self.gridslot[1])
        # TODO: Use binary iteration to reserve slots
        # print(self.gridslot)
        if (self.gridslot[0] + self.gridslot[1]) != 2:
            if self.gridslot[0] == 1 and self.gridslot[1] == 0:
                self.gridslot[1] += 1
            if self.gridslot[1] == 1:
                self.gridslot[0] += 1
        #     self.gridslot[0] += 1
        # if self.gridslot[0] == 0:
        #     self.gridslot[1] += 1

