from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QCheckBox, QFrame)
from ..services.actions import Call
from lib.widgets.wizard import ImportWizard
# from .elements.algoptions import AlgorithmControl
# from .elements.graphctrl import GraphControl
from .elements import (AlgorithmControl, GraphControl, AlgorithmOptions, ImportControl, ColorLegend)



class ControlWidgets(QFrame):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    # TODO: Use signals to notify the main window instead of connecting in it
    # canvasChanged = pyqtSignal(int)
    # self.canvasChanged.emit(self.canvas) //in method
    # self.controls.canvasChanged.connect() // in main
    # vComboChanged = pyqtSignal(str)

    # PENDING: Fix maximum controls width
    def __init__(self, parent=None):
        super(ControlWidgets, self).__init__(parent)
        self.maxCanvasId = 0
        self.selectedCanvasId = 0
        self.algorithm = 'random'
        self.isSingleFile = False
        self.__controls()
        self.__layout()
        self.__actions()
        self.vbox.addStretch(1)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.show()

    def __controls(self):
        self.graphCtrl = GraphControl()
        self.algCtrl = AlgorithmControl()
        self.algOpt = AlgorithmOptions()
        self.importCtrl = ImportControl()
        self.w = ColorLegend(self)

    def __layout(self):
        self.vbox = QVBoxLayout()
        # Add subcomponents
        self.vbox.addLayout(self.importCtrl)
        self.vbox.addLayout(self.graphCtrl)
        self.vbox.addLayout(self.algCtrl)
        self.vbox.addLayout(self.algOpt)
        self.vbox.addWidget(self.w)

    def __actions(self):
        # Buttons
        self.algCtrl.algBtn.clicked.connect(self.applyAlg)
        self.importCtrl.importBtn.clicked.connect(self.import_wizard)
        # Checkboxes
        self.importCtrl.singleChk.stateChanged.connect(self.checkImport)
        # Dropdowns
        self.algCtrl.algSelector.activated[str].connect(self.algSelect)
        self.graphCtrl.canvasSelector.activated[int].connect(self.graphCtrl.selectCanvas)

    def get_layout(self):
        return self.vbox

    def algSelect(self, text):
        self.algorithm = text
        print(self.algorithm)

        if text == 'force directed':
            self.algOpt.enabled(True)
        else:
            self.algOpt.enabled(False)

    def newGraph(self, graphId):
        # Informs the graph control group to update graph id
        self.graphCtrl.addGraphId(graphId)

    def killGraph(self):
        return self.graphCtrl.delGraphId()

    def applyAlg(self):
        forceText = self.algOpt.get_text()
        # Applies distribution algorithm on selected graph
        print("apply {}".format(self.algorithm))
        Call.apply_alg(int(self.selectedCanvasId), self.algorithm, *forceText)

    # Activates the import wizard
    def import_wizard(self):
        exPopup = ImportWizard(self, self.isSingleFile)
        exPopup.setGeometry(100, 200, 800, 600)
        exPopup.show()
        self.graphCtrl.enable(True)

    def checkImport(self, state):
        self.isSingleFile = state
        print(self.isSingleFile)

    def modifyIdList(self):
        pass
