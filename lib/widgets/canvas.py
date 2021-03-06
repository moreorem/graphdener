from ..graphics.graph import Canvas
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QStackedLayout)
from ..services.actions import Call
import numpy as np
from .. import func


class CanvasWidget(QFrame):
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.canvasContainer = {}
        self.gridslot = [i for i in func.iterate_grid(2)]
        self.setMinimumSize(400, 400)

    def __controls(self):
        pass

    def __layout(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(100)

    def get_layout(self):
        return self.grid

    def closeCanvas(self, canvasId):
        try:
            canvas = self.canvasContainer.pop(canvasId)
            self.grid.removeWidget(canvas)
            canvas.close()
        except KeyError as e:
            print("Cannot find canvas Id", e)

    def createCanvas(self, canvasId):
        # TODO: Consider QStackedLayout
        if canvasId in self.canvasContainer.keys():
            print("Canvas with that id already exists!")
            return canvasId
        print("Drawing canvas with id: {}...".format(canvasId))
        positions = Call.get_n_pos(canvasId)
        va = np.array(positions)
        ve = np.hstack((va, np.zeros((len(positions), 1))))
        # Get adjacency list
        ed = Call.get_adj(canvasId)
        # Get node types
        types = Call.get_n_type(canvasId)
        c_types = self.__createColors(types)
        # Create the color for each node
        col = [c_types[t] for t in types]
        print(self.gridslot[canvasId])
        # TODO: Set fixed canvas size for each canvas
        self.canvasContainer[canvasId] = Canvas(title='Visualizer', edges=ed,
                                                node_pos=ve, color=col,
                                                graphId=canvasId).native
        self.grid.addWidget(self.canvasContainer[canvasId],*self.gridslot[canvasId])
        # TODO: Improve grid_iteration in order to iterate once in every canvas creation

    def __createColors(self, types):
        t = list(set(types))
        rgb_palette = np.random.uniform(0, 1, (len(t), 3)).astype(np.float32)
        color_types = dict(zip(t, rgb_palette))
        return color_types

    def setCanvasId(self, canvasId):
        self.canvasId = canvasId

