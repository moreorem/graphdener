from ..graphics.canvas import MyCanvas
from ..graphics.graph import GraphCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from ..services.actions import Call


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

    def create_canvas(self):
        if self.canvas is not None:
            # self.vbox.removeWidget(self.canvas)
            self.close_canvas()
        nodes = Call.get_positions()
        print(float(list(nodes[0])[0]))

        self.canvas = GraphCanvas(*nodes).native
        # self.canvas = GraphCanvas().native
        self.vbox.addWidget(self.canvas)

