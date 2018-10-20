from PyQt5.QtWidgets import (QLabel, QPushButton, QComboBox, QGridLayout)
from ...statics import ALGS


class AlgorithmControl(QGridLayout):
    def __init__(self, parent=None):
        super(AlgorithmControl, self).__init__()
        # self.selectedAlgorithm = 0
        self.__controls()
        self.__layout()
        self.__populate()
        self.setVerticalSpacing(0)
        self.enabled(True)
        self.animateBtn.setEnabled(False)

    def __controls(self):
        self.algLabel = QLabel("Algorithms")
        self.algSelector = QComboBox()
        self.algBtn = QPushButton("Apply Algorithm")
        self.animateBtn = QPushButton("Animate")

    def __layout(self):
        self.addWidget(self.algLabel, 0, 0)
        self.addWidget(self.algSelector, 1, 0)
        self.addWidget(self.algBtn, 1, 1)
        self.addWidget(self.animateBtn, 2, 0)

    def __populate(self):
        self.algSelector.addItems(ALGS)

    def enabled(self, value):
        if not value:
            pass

    def enableAnimator(self, value):
        self.animateBtn.setEnabled(value)
