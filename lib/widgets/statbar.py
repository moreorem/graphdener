from PyQt5.QtWidgets import (QStatusBar, QHBoxLayout)


class StatusBar(QStatusBar):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.vbox.addStretch(1)
        self.showMessage("Ready")

    def __controls(self):
        pass

    def __layout(self):
        self.vbox = QHBoxLayout()

    def write_out(self, msg):
        self.showMessage(str(msg))

    def get_layout(self):
        self.vbox
