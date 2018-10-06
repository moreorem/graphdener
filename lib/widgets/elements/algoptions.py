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
        self.enabled('', False)

    def __controls(self):
        for i in range(len(LABELS)):
            self.forceLabels.append(QLabel())
            self.forceConstants.append(QLineEdit())
        self.randLabel = QLabel()
        self.randSpread = QLineEdit()
        self.set_labels()
        self.init_text()

    def __layout(self):
        for i in range(len(LABELS)):
            self.addWidget(self.forceLabels[i], i, 0)
            self.addWidget(self.forceConstants[i], i, 1)
        self.addWidget(self.randLabel, len(LABELS) + 1, 0)
        self.addWidget(self.randSpread, len(LABELS) + 1, 1)

    def set_labels(self):
        for i in range(len(LABELS)):
            self.forceLabels[i].setText(LABELS[i])
        self.randLabel.setText("Scatter Factor")

    def init_text(self):
        for fcText in self.forceConstants:
            fcText.setText('0.0')
        self.randSpread.setText("10")

    def get_text(self, item):
        if item == 'force directed':
            return [txtBox.text() for txtBox in self.forceConstants]
        elif item == 'random':
            return [self.randSpread.text()]

    def enabled(self, wd, value):
        if wd == 'forced':
            for i in range(len(LABELS)):
                self.forceLabels[i].setEnabled(value)
                self.forceConstants[i].setEnabled(value)
        elif wd == 'rand':
            self.randLabel.setEnabled(value)
            self.randSpread.setEnabled(value)
        else:
            for i in range(len(LABELS)):
                self.forceLabels[i].setEnabled(value)
                self.forceConstants[i].setEnabled(value)
            self.randLabel.setEnabled(value)
            self.randSpread.setEnabled(value)
