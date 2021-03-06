from PyQt5.QtWidgets import (QPushButton, QGridLayout, QCheckBox)


class ImportControl(QGridLayout):
    def __init__(self, parent=None):
        super(ImportControl, self).__init__()
        self.selectedAlgorithm = 0
        self.__controls()
        self.__layout()
        self.setVerticalSpacing(0)
        self.enabled(True)

    def __controls(self):
        self.importBtn = QPushButton("Import Wizard")
        self.singleChk = QCheckBox("Single page import")

    def __layout(self):
        self.addWidget(self.importBtn, 0, 0)
        self.addWidget(self.singleChk, 0, 1)

    def enabled(self, value):
        if not value:
            pass

