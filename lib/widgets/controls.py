from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QCheckBox)
from ..services.actions import Call
from lib.widgets.wizard import ImportWizard
# from .elements.algoptions import AlgorithmControl
# from .elements.graphctrl import GraphControl
from .elements import (AlgorithmControl, GraphControl, AlgorithmOptions)


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
        self.algorithm = 'random'
        self.isSingleFile = False
        self.__controls()
        self.__layout()
        # Buttons
        self.algBtn.clicked.connect(self.applyAlg)
        self.importBtn.clicked.connect(self.import_wizard)
        # Checkboxes
        self.singleChk.stateChanged.connect(self.checkImport)
        # Dropdowns
        self.algCtrl.algSelector.activated[str].connect(self.algSelect)
        self.graphCtrl.canvasSelector.activated[int].connect(self.selectCanvas)

    def __controls(self):
        self.graphCtrl = GraphControl()
        self.algCtrl = AlgorithmControl()
        self.algOpt = AlgorithmOptions()
        self.importBtn = QPushButton("Import Wizard")
        self.singleChk = QCheckBox("Single page import")
        self.algBtn = QPushButton("Apply Algorithm")

    def __layout(self):
        self.vbox = QVBoxLayout()

        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.importBtn)
        self.vbox.addWidget(self.singleChk)
        # self.vbox.addLayout(self.algLayout)
        self.vbox.addWidget(self.algBtn)
        # Add the algorithm control unit
        self.vbox.addLayout(self.graphCtrl)
        self.vbox.addLayout(self.algCtrl)
        self.vbox.addLayout(self.algOpt)

    def get_layout(self):
        return self.vbox

    def selectCanvas(self, data):
        self.selectedCanvasId = data

    def algSelect(self, text):
        self.algorithm = text
        if text == 'force directed':
            self.algOpt.enabled(False)
        else:
            self.algOpt.enabled(True)

    def newGraph(self):
        # Creates new graph on new canvas and populates it
        Call.create_graph(self.selectedCanvasId)
        Call.populate_graph(self.selectedCanvasId)
        self.changeCanvasId('add')

    def applyAlg(self):
        forceText = self.algOpt.get_text()
        # Applies distribution algorithm on selected graph
        print("apply {}".format(self.algorithm))
        Call.apply_alg(self.selectedCanvasId, self.algorithm, *forceText)

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
