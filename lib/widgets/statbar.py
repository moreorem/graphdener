from PyQt5.QtWidgets import (QStatusBar, QHBoxLayout)


class StatusBar(QStatusBar):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    # TODO: Ready state when not doing something
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.__controls()
        self.__layout()
        # self.__actions()
        self.vbox.addStretch(1)
        self.showMessage("Ready")

    def __controls(self):
        pass

    def __layout(self):
        self.vbox = QHBoxLayout()
        # Add subcomponents

    def write_out(self, msg):
        self.showMessage(str(msg))

    def get_layout(self):
        self.vbox
