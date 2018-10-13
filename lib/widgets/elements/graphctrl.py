from PyQt5.QtWidgets import (QLabel, QPushButton, QComboBox, QGridLayout)


class GraphControl(QGridLayout):
    def __init__(self, parent=None):
        super(GraphControl, self).__init__()
        self.canvasList = []
        self.selectedGraphId = 0
        self.__controls()
        self.__layout()
        self.setVerticalSpacing(2)
        self.enable(False)

    def __controls(self):
        self.drawBtn = QPushButton("Draw Graph")
        self.closeBtn = QPushButton("Kill Graph")
        # Add canvas selector
        self.csLabel = QLabel("Canvas Selector")
        self.canvasSelector = QComboBox()

    def __layout(self):
        self.addWidget(self.csLabel, 0, 0)
        self.addWidget(self.canvasSelector, 1, 0)
        self.addWidget(self.drawBtn, 2, 0)
        self.addWidget(self.closeBtn, 2, 1)

    def addGraphId(self, graphId):
        self.canvasSelector.addItem(str(graphId))
        self.canvasSelector.setCurrentText(str(graphId))
        self.canvasList.append(graphId)

    def delGraphId(self):
        selIdx = self.canvasSelector.currentIndex()
        graphId = self.canvasSelector.currentText()
        self.canvasSelector.removeItem(selIdx)
        self.canvasList.pop(int(graphId))
        return int(graphId)

    def enable(self, value):
        self.drawBtn.setEnabled(value)
        self.closeBtn.setEnabled(value)
        self.canvasSelector.setEnabled(value)
