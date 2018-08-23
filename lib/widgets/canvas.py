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
        nd = np.matrix(nodes)
        self.canvas = GraphCanvas(nd).native
        self.vbox.addWidget(self.canvas)

