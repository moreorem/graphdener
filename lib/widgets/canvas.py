from ..graphics.graph import Canvas
from PyQt5.QtWidgets import (QWidget, QGridLayout)
from ..services.actions import Call
import numpy as np
from .. import func

COLOR_LIST = [(1.0, 0.8941176, 0.7686275),
                (0.545098, 0.5372549, 0.5372549),
                (1.0, 0.9803922, 0.8039216),
                (0.9019608, 0.9019608, 0.9803922),
                (0.1921569, 0.3098039, 0.3098039),
                (0.3921569, 0.5843137, 0.9294118),
                (0.0, 0.0, 0.8039216),
                (0.0, 0.7490196, 1.0),
                (0.2745098, 0.5098039, 0.7058824),
                (0.2509804, 0.8784314, 0.8156863),
                (0.0, 0.3921569, 0.0),
                (0.4980392, 1.0, 0.0),
                (0.1960784, 0.8039216, 0.1960784),
                (0.4196078, 0.5568627, 0.1372549),
                (1.0, 1.0, 0.0),
                (0.854902, 0.6470588, 0.1254902),
                (0.8039216, 0.3607843, 0.3607843),
                (0.9568627, 0.6431373, 0.3764706),
                (0.6980392, 0.1333333, 0.1333333),
                (0.9803922, 0.5019608, 0.4470588),
                (1.0, 0.0, 0.0),
                (1.0, 0.0784314, 0.5764706),
                (0.7294118, 0.3333333, 0.827451),
                (0.5411765, 0.1686275, 0.8862745),
                (0.5764706, 0.4392157, 0.8588235)]


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
        col = [c_types[t] for t in types]
        c_types = tuple(c_types.values())

        canvas = Canvas(title='Graphdener Visualizer', edges=ed, node_pos=ve, color=col).native

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
