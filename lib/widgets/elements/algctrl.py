from PyQt5.QtWidgets import (QLabel, QPushButton, QComboBox, QGridLayout)

ALGS = ['random', 'circular', 'force directed']


class AlgorithmControl(QGridLayout):
    def __init__(self, parent=None):
        super(AlgorithmControl, self).__init__()
        self.selectedAlgorithm = 0
        self.__controls()
        self.__layout()
        self.__populate()
        self.setVerticalSpacing(2)
        self.enabled(True)

    def __controls(self):
        self.algLabel = QLabel("Algorithms")
        self.algSelector = QComboBox()
        self.algBtn = QPushButton("Apply Algorithm")

    def __layout(self):
        self.addWidget(self.algLabel, 0, 0)
        self.addWidget(self.algSelector, 1, 0)
        self.addWidget(self.algBtn, 1, 1)

    def __populate(self):
        self.algSelector.addItems(ALGS)

    def enabled(self, value):
        if not value:
            pass

