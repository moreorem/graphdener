from PyQt5.QtWidgets import (QLabel, QPushButton, QComboBox, QGridLayout)


class GraphControl(QGridLayout):
    def __init__(self, parent=None):
        super(GraphControl, self).__init__()
        self.maxCanvasId = 0
        self.selectedCanvasId = 0
        self.__controls()
        self.__layout()
        self.setVerticalSpacing(2)
        self.enabled(True)

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

    def changeCanvasId(self, method):
        if method == 'add':
            self.canvasSelector.addItem(str(self.maxCanvasId))
            self.maxCanvasId += 1
        elif method == 'remove':
            self.maxCanvasId -= 1
            self.canvasSelector.removeItem(self.selectedCanvasId)

    def enabled(self, value):
        if not value:
            pass
    
