from PyQt5.QtWidgets import (QLabel, QLineEdit, QGridLayout)
from ...statics import FLABELS as LABELS


class AlgorithmOptions(QGridLayout):
    def __init__(self, parent=None):
        super(AlgorithmOptions, self).__init__()
        self.forceLabels = []
        self.forceConstants = []
        self.__controls()
        self.__layout()
        self.setVerticalSpacing(2)
        self.enabled(False)


    def __controls(self):
        for i in range(len(LABELS)):
            self.forceLabels.append(QLabel())
            self.forceConstants.append(QLineEdit())
        self.set_labels()
        self.init_text()

    def __layout(self):
        for i in range(len(LABELS)):
            self.addWidget(self.forceLabels[i], i, 0)
            self.addWidget(self.forceConstants[i], i, 1)

    def set_labels(self):
        for i in range(len(LABELS)):
            self.forceLabels[i].setText(LABELS[i])

    def init_text(self):
        for fcText in self.forceConstants:
            fcText.setText('0.0')

    def get_text(self):
        return [txtBox.text() for txtBox in self.forceConstants]

    def enabled(self, value):
        for i in range(len(LABELS)):
            self.forceLabels[i].setEnabled(value)
            self.forceConstants[i].setEnabled(value)
