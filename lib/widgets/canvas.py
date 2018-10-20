from ..graphics.graph import Graph
from PyQt5.QtWidgets import (QStackedWidget, QStackedLayout)
from ..services.actions import Call
import numpy as np


class CanvasWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.__layout()
        self.stackLayout.addWidget(self)
        self.graphContainer = {}
        self.setMinimumSize(400, 400)
        self.colorTypes = {}

    def __layout(self):
        self.stackLayout = QStackedLayout()

    def get_layout(self):
        return self.stackLayout

    def closeGraph(self, graphId):
        try:
            Call.kill_graph()
            canvas = self.graphContainer.pop(graphId)
            print("Closed canvas with Id", canvas.graphId)
            self.removeWidget(canvas)
            canvas.close()
        except KeyError as e:
            print("Cannot find canvas Id", e)

    def drawGraph(self):
        graphId = Call.create_graph()
        Call.populate_graph()
        Call.graphId = graphId
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
        self.graphContainer[graphId] = Graph(title='Visualizer',
                                             edges=ed, node_pos=ve,
                                             color=col,
                                             graphId=graphId).native
        self.addWidget(self.graphContainer[graphId])
        print(self.graphContainer[graphId].translate)
        if self.count() == 1:
            self.display(graphId)

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
        self.setCurrentWidget(self.graphContainer[i])

    def animate(self, trigger):
        print(dir(self.currentWidget().app))
        if trigger:
            print(self.graphContainer[0].app)
            self.currentWidget().Timer.start()
