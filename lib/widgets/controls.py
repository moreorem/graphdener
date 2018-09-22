from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QComboBox, QLabel, QLineEdit, QHBoxLayout, QCheckBox)
from ..services.actions import Call
from lib.widgets.wizard import ImportWizard

LABELS = ['Spring rest length', 'Repulsive force constant', 'Spring constant', 'Time step']
ALGS = ['random', 'circular', 'force directed']

class ControlWidgets(QWidget):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    # TODO: Use signals to notify the main window instead of connecting in it
    # canvasChanged = pyqtSignal(int)
    # self.canvasChanged.emit(self.canvas) //in method
    # self.controls.canvasChanged.connect() // in main
    # vComboChanged = pyqtSignal(str)

    # PENDING: Fix maximum controls width

    def __init__(self, parent=None):
        super(ControlWidgets, self).__init__(parent)
        self.forceConstants = []
        self.forceText = []
        self.forceLabels = []
        self.algorithm = 'random'
        self.isSingleFile = False
        self.selectedCanvasId = 0
        self.maxCanvasId = 0
        self.__controls()
        self.__layout()
        # Buttons
        self.algBtn.clicked.connect(self.applyAlg)
        self.importBtn.clicked.connect(self.import_wizard)
        # Checkboxes
        self.singleChk.stateChanged.connect(self.checkImport)
        # Dropdowns
        self.algSelector.activated[str].connect(self.algSelect)
        self.canvasSelector.activated[int].connect(self.selectCanvas)

        for i in range(len(LABELS)):
            self.forceLabels[i].setText(LABELS[i])

    def __controls(self):
        self.importBtn = QPushButton("Import Wizard")
        self.singleChk = QCheckBox("Single page import")
        self.algBtn = QPushButton("Apply Algorithm")
        self.drawBtn = QPushButton("Draw Graph")
        self.closeBtn = QPushButton("Kill Graph")

        # Add canvas selector
        self.csLabel = QLabel("Canvas Selector")
        self.canvasSelector = QComboBox(self)

        # Add distribution algorithm selector
        self.alLabel = QLabel("Algorithm Selector")
        self.algSelector = QComboBox(self)
        self.algSelector.addItems(ALGS)

        # Initialize force directed control labels and textboxes
        for i in range(len(LABELS)):
            self.forceLabels.append(QLabel())
            self.forceConstants.append(QLineEdit())

        for fcText in self.forceConstants:
            fcText.setText('0.0')

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.algLayout = QHBoxLayout()
        self.csLayout = QHBoxLayout()

        self.forceLayouts = []
        for i in range(len(LABELS)):
            self.forceLayouts.append(QHBoxLayout())

        # Alg layout
        self.algLayout.addWidget(self.alLabel)
        self.algLayout.addWidget(self.algSelector)
        # Canvas selector layout
        self.csLayout.addWidget(self.csLabel)
        self.csLayout.addWidget(self.canvasSelector)
        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.importBtn)
        self.vbox.addWidget(self.singleChk)
        self.vbox.addLayout(self.algLayout)
        self.vbox.addWidget(self.algBtn)
        self.vbox.addLayout(self.csLayout)
        self.vbox.addWidget(self.drawBtn)
        self.vbox.addWidget(self.closeBtn)

        for i in range(len(LABELS)):
            self.forceLayouts[i].addWidget(self.forceLabels[i])
            self.forceLayouts[i].addWidget(self.forceConstants[i])

        for layout in self.forceLayouts:
            self.vbox.addLayout(layout)

    def get_layout(self):
        return self.vbox

    def selectCanvas(self, data):
        self.selectedCanvasId = data

    def algSelect(self, text):
        self.algorithm = text

    def changeCanvasId(self, method):
        if method == 'add':
            self.canvasSelector.addItem(str(self.maxCanvasId))
            self.maxCanvasId += 1
        elif method == 'remove':
            self.maxCanvasId -= 1
            self.canvasSelector.removeItem(self.selectedCanvasId)

    def newGraph(self):
        # Creates new graph on new canvas and populates it
        Call.create_graph(self.selectedCanvasId)
        Call.populate_graph(self.selectedCanvasId)
        self.changeCanvasId('add')

    def applyAlg(self):
        self.forceText = [txtBox.text() for txtBox in self.forceConstants]
        # Applies distribution algorithm on selected graph

        Call.apply_alg(self.selectedCanvasId, self.algorithm, *self.forceText)

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

