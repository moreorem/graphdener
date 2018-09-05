from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QComboBox)
from ..services.backend import Backend
from ..services.actions import Call


class ControlWidgets(QWidget):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    # TODO: Use signals to notify the main window instead of connecting in it
    # canvasChanged = pyqtSignal(int)
    # self.canvasChanged.emit(self.canvas) //in method
    # self.controls.canvasChanged.connect() // in main
    # vComboChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ControlWidgets, self).__init__(parent)
        self.__controls()
        self.__layout()
        self.button1.clicked.connect(Backend.start)
        self.button2.clicked.connect(Backend.stop)
        self.button4.clicked.connect(self.get_e_info)
        self.button5.clicked.connect(self.get_v_info)

        self.edgeComboBox.activated[str].connect(self.ea_selected)
        self.vertComboBox.activated[str].connect(self.va_selected)

    def __controls(self):
        self.button1 = QPushButton("start")
        self.button2 = QPushButton("stop")
        self.button3 = QPushButton("Import Wizard")
        self.button4 = QPushButton("Get edge attr.")
        self.button5 = QPushButton("Get vertex attr.")
        self.button6 = QPushButton("Re-Draw")

        # Add vertex info selector
        self.vertComboBox = QComboBox(self)
        self.vertComboBox.addItem("type", "types")
        self.vertComboBox.addItem("pos", "positions")
        self.vertComboBox.addItem("label", "labels")

        # Add edge info selector
        self.edgeComboBox = QComboBox(self)
        self.edgeComboBox.addItem("type", "types")
        self.edgeComboBox.addItem("label", "labels")
        self.edgeComboBox.addItem("weight", "weights")
        self.edgeComboBox.addItem("pos", "list")


    def __layout(self):
        self.vbox = QVBoxLayout()

        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)
        self.vbox.addWidget(self.button4)
        self.vbox.addWidget(self.edgeComboBox)
        self.vbox.addWidget(self.button5)
        self.vbox.addWidget(self.vertComboBox)
        self.vbox.addWidget(self.button6)

    def get_layout(self):
        return self.vbox

    def ea_selected(self, text):
        self.edgeAttribute = text

    def va_selected(self, text):
        self.vertAttribute = text

    def get_e_info(self):
        Call.get_edge(self.edgeAttribute)

    def get_v_info(self):
        Call.get_vert(self.vertAttribute)
