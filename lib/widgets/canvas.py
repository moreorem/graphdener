from ..graphics.graph import Canvas
from PyQt5.QtWidgets import (QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QFrame, QLabel, QStackedLayout)
from ..services.actions import Call
import numpy as np
from .. import func


class CanvasWidget(QFrame):
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        # QStackedWidget.__init__(self)
        self.__controls()
        self.__layout()
        self.canvasContainer = {}
        self.stackLayout.addWidget(self.stack)
        # self.gridslot = [i for i in func.iterate_grid(2)]
        self.setMinimumSize(600, 600)
        self.colorTypes = {}

    def __controls(self):
        self.stack = QStackedWidget()
        # self.canvasWidget = QWidget()

    def __layout(self):
        self.stackLayout = QStackedLayout()
        self.stackLayout.setStackingMode
        self.setLayout(self.stackLayout)

        # self.grid = QGridLayout()
        # self.setLayout(self.grid)

    def get_layout(self):
        return self.stackLayout

    def closeCanvas(self, canvasId):
        try:
            Call.kill_graph(canvasId)
            canvas = self.canvasContainer.pop(canvasId)
            print("Closed canvas with Id", canvas.graphId)
            # self.grid.removeWidget(canvas)
            self.stack.removeWidget(canvas)
            canvas.close()
        except KeyError as e:
            print("Cannot find canvas Id", e)

    def createCanvas(self):
        if len(self.canvasContainer.keys()) < 4:
            graphId = Call.create_graph()
            Call.populate_graph()
            print("Drawing canvas with id: {}...".format(graphId))
            positions = Call.get_n_pos()
            va = np.array(positions)
            ve = np.hstack((va, np.zeros((len(positions), 1))))
            # Get adjacency list
            ed = Call.get_adj()
            # Get node types
            types = Call.get_n_type()
            c_types = self.__createColors(types)
            # Create the color for each node
            col = [c_types[t] for t in types]
            # TODO: Set fixed canvas size for each canvas
            self.canvasContainer[graphId] = Canvas(title='Visualizer', edges=ed, node_pos=ve, color=col, graphId=graphId).native
            self.stack.addWidget(self.canvasContainer[graphId])
            print(self.stack.count())
            # self.grid.addWidget(self.canvasContainer[graphId], *self.gridslot[graphId])
            self.display(graphId)
            return graphId
            # TODO: Improve grid_iteration in order to iterate once in every canvas creation

    def __createColors(self, types):
        t = list(set(types))
        rgb_palette = np.random.uniform(0, 1, (len(t), 3)).astype(np.float32)
        # Make color map to send to the legend
        c = rgb_palette.dot(255).astype(int)
        colors = list(map(tuple, c))
        self.colorTypes = dict(zip(t, colors))
        # Make color map to send to the graph
        color_types = dict(zip(t, rgb_palette))
        return color_types

    def display(self, i):
        self.stack.setCurrentWidget(self.canvasContainer[0])

    def hide(self, w):
        self.removeWidget(w)
