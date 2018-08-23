from ..graphics.graphvis import GraphCanvas
# from ..graphics.graph import GraphCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from ..services.actions import Call
import numpy as np

class CanvasWidget(QWidget):
    def __init__(self, parent):
        super(CanvasWidget, self).__init__(parent)
        self.__controls(parent)
        self.__layout()
        self.canvas = None

    def __controls(self, parent):
        self.canvasWidget = QWidget(parent)

    def __layout(self):
        self.vbox = QVBoxLayout()

    def get_layout(self):
        return self.vbox

    def close_canvas(self):
        self.canvas.close()
        self.vbox.removeWidget(self.canvas)
        self.canvas = None

    def create_canvas(self):
        # FIXME: When pressing redraw button the interface corrupts
        if self.canvas is not None:
            self.close_canvas()

        # Get node positions from backend
        nodes = Call.get_positions()
        colors = np.ones((len(nodes), 4), dtype=np.float32)
        for i in range(len(nodes)):
            colors[i] = (i / 500, 1.0 - i / 500, 0, 1)

        nd = np.matrix(nodes)
        self.canvas = GraphCanvas(nd, colors).native
        self.vbox.addWidget(self.canvas)

