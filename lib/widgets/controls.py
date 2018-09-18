from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QComboBox, QLabel, QLineEdit, QHBoxLayout)
from ..services.backend import Backend
from ..services.actions import Call

LABELS = ['L', 'K_r', 'K_s', 'Delta_t']


class ControlWidgets(QWidget):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    # TODO: Use signals to notify the main window instead of connecting in it
    # canvasChanged = pyqtSignal(int)
    # self.canvasChanged.emit(self.canvas) //in method
    # self.controls.canvasChanged.connect() // in main
    # vComboChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ControlWidgets, self).__init__(parent)
        self.forceConstants = []
        self.forceLabels = []
        self.graph = 1

        self.__controls()
        self.__layout()

        self.button1.clicked.connect(Backend.start)
        self.button2.clicked.connect(Backend.stop)
        self.button4.clicked.connect(self.refresh)
        self.button5.clicked.connect(self.get_v_info)

        self.edgeComboBox.activated[str].connect(self.ea_selected)
        self.vertComboBox.activated[str].connect(self.va_selected)

        for i in range(len(LABELS) - 1):
            self.forceLabels[i].setText(LABELS[i])

    def __controls(self):
        self.button1 = QPushButton("start")
        self.button2 = QPushButton("stop")
        self.button3 = QPushButton("Import Wizard")
        self.button4 = QPushButton("Refresh")
        self.button5 = QPushButton("Get vertex attr.")
        self.button6 = QPushButton("Re-Draw")

        # Add vertex info selector
        self.vertComboBox = QComboBox(self)
        self.vertComboBox.addItem("type", "types")
        self.vertComboBox.addItem("pos", "positions")
        self.vertComboBox.addItem("label", "labels")

        # Add distribution algorithm selector
        self.edgeComboBox = QComboBox(self)
        self.edgeComboBox.addItem("circular")
        self.edgeComboBox.addItem("force directed")

        # Initialize force directed control labels and textboxes
        for i in range(len(LABELS) - 1):
            self.forceLabels.append(QLabel())
            self.forceConstants.append(QLineEdit())

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.forceLayouts = []
        for i in range(len(LABELS) - 1):
            self.forceLayouts.append(QHBoxLayout())

        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)
        self.vbox.addWidget(self.button4)
        self.vbox.addWidget(self.edgeComboBox)
        self.vbox.addWidget(self.button5)
        self.vbox.addWidget(self.vertComboBox)
        self.vbox.addWidget(self.button6)

        for i in range(len(LABELS) - 1):
            self.forceLayouts[i].addWidget(self.forceLabels[i])
            self.forceLayouts[i].addWidget(self.forceConstants[i])

        for layout in self.forceLayouts:
            self.vbox.addLayout(layout)

    def get_layout(self):
        return self.vbox

    def va_selected(self, text):
        self.vertAttribute = text

    def ea_selected(self, text):
        self.edgeAttribute = text

    def get_v_info(self):
        Call.get_vert(self.vertAttribute, 1)

    def refresh(self):
        Call.create_graph(self.graph)
        self.graph += 1

