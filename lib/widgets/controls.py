from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QComboBox, QLabel, QLineEdit, QHBoxLayout, QCheckBox)
from ..services.backend import Backend
from ..services.actions import Call
from lib.widgets.wizard import ImportWizard


LABELS = ['L', 'K_r', 'K_s', 'Delta_t']


# TODO: Convert Redraw button into create new graph

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
        self.isSingleFile = False
        self.canvasId = 1
        self.__controls()
        self.__layout()

        self.algBtn.clicked.connect(self.applyAlg)
        self.newBtn.clicked.connect(self.newGraph)
        self.importBtn.clicked.connect(self.import_wizard)
        self.singleChk.stateChanged.connect(self.checkImport)

        self.algComboBox.activated[str].connect(self.algSelect)
        self.canvasSelector.activated[str].connect(self.selectCanvas)

        for i in range(len(LABELS) - 1):
            self.forceLabels[i].setText(LABELS[i])

    def __controls(self):
        self.importBtn = QPushButton("Import Wizard")
        self.singleChk = QCheckBox("Single page import")
        self.algBtn = QPushButton("Apply Algorithm")
        self.newBtn = QPushButton("New Graph")
        self.button6 = QPushButton("Re-Draw")

        # Add canvas selector
        self.csLabel = QLabel("Canvas Selector")
        self.canvasSelector = QComboBox(self)
        self.canvasSelector.addItem("1")

        # Add distribution algorithm selector
        self.alLabel = QLabel("Algorithm Selector")
        self.algComboBox = QComboBox(self)
        self.algComboBox.addItem("circular")
        self.algComboBox.addItem("force directed")


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
        self.vbox.addWidget(self.importBtn)
        self.vbox.addWidget(self.singleChk)
        self.vbox.addWidget(self.newBtn)
        self.vbox.addWidget(self.alLabel)
        self.vbox.addWidget(self.algComboBox)
        self.vbox.addWidget(self.algBtn)
        self.vbox.addWidget(self.csLabel)
        self.vbox.addWidget(self.canvasSelector)

        for i in range(len(LABELS) - 1):
            self.forceLayouts[i].addWidget(self.forceLabels[i])
            self.forceLayouts[i].addWidget(self.forceConstants[i])

        for layout in self.forceLayouts:
            self.vbox.addLayout(layout)

    def get_layout(self):
        return self.vbox

    def selectCanvas(self, text):
        self.vertAttribute = text

    def algSelect(self, text):
        self.algorithm = text

    def newGraph(self):
        # Creates new graph on new canvas and populates it
        Call.create_graph(1)
        Call.populate_graph(1)
        self.canvasId += 1

    def applyAlg(self):
        # Refreshes current graph in case we want to change distribution
        result = Call.apply_alg(self.graph, *self.forceConstants)
        # result = Call.update_pos(1)
        print(result)

    def updateCanvasSelector(self, canvasId):
        self.canvasSelector.addItem(String(canvasId))

    # Activates the import wizard
    def import_wizard(self):
        exPopup = ImportWizard(self, self.isSingleFile)
        exPopup.setGeometry(100, 200, 800, 600)
        exPopup.show()

    def checkImport(self, state):
        if state:
            self.isSingleFile = True
        else:
            self.isSingleFile = False

