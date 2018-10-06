from PyQt5.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    # PENDING: Fix maximum controls width
    # PENDING: Decide on wether to use qwidget or qframe
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.__actions()
        self.vbox.addStretch(1)

    def __controls(self):
        pass
    def __layout(self):
        self.vbox = QVBoxLayout()
        # Add subcomponents

