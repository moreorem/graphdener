from canvas import MyCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)


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
            self.close_canvas()
        self.canvas = MyCanvas(100).native
        self.vbox.addWidget(self.canvas)
