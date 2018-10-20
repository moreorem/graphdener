from PyQt5.QtWidgets import (QLabel, QPushButton, QComboBox, QGridLayout)


class GraphControl(QGridLayout):
    def __init__(self, parent=None):
        super(GraphControl, self).__init__()
        self.selectedGraphId = 0
        self.__controls()
        self.__layout()
        self.setVerticalSpacing(2)
        self.enable(False)

    def __controls(self):
        self.closeBtn = QPushButton("Kill Graph")
        # Add canvas selector
        self.csLabel = QLabel("Canvas Selector")
        self.graphSelector = QComboBox()

    def __layout(self):
        self.addWidget(self.csLabel, 0, 0)
        self.addWidget(self.graphSelector, 1, 0)
        self.addWidget(self.closeBtn, 1, 1)

    def addGraphId(self, graphId):
        self.graphSelector.addItem(str(graphId))
        self.graphSelector.setCurrentIndex(0)

    def delGraphId(self):
        selIdx = self.graphSelector.currentIndex()
        graphId = self.graphSelector.currentText()
        self.graphSelector.removeItem(selIdx)
        return int(graphId)

    def enable(self, value):
        self.graphSelector.setEnabled(value)
