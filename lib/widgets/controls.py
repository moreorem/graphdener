from PyQt5.QtWidgets import (QVBoxLayout, QFrame, QWidget)
from ..services.actions import Call
from lib.widgets.wizard import ImportWizard
from .elements import (AlgorithmControl, GraphControl, AlgorithmOptions, ImportControl, ColorLegend)


class ControlWidgets(QWidget):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

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
        # self.setFrameShape(QFrame.VLine)

    def __controls(self):
        self.graphCtrl = GraphControl()
        self.algCtrl = AlgorithmControl()
        self.algOpt = AlgorithmOptions()
        self.importCtrl = ImportControl()
        self.typeList = ColorLegend(self)
        self.typeList.move(60, 200)
        self.typeList.resize(50, 50)

    def __layout(self):
        self.vbox = QVBoxLayout()
        # Add subcomponents
        self.vbox.addLayout(self.importCtrl)
        self.vbox.addLayout(self.graphCtrl)
        self.vbox.addLayout(self.algCtrl)
        self.vbox.addLayout(self.algOpt)
        self.vbox.addWidget(self.typeList)

    def __actions(self):
        # Buttons
        self.algCtrl.algBtn.clicked.connect(self.applyAlg)
        self.importCtrl.importBtn.clicked.connect(self.import_wizard)
        # Dropdowns
        self.algCtrl.algSelector.activated[str].connect(self.algSelect)
        self.graphCtrl.canvasSelector.activated[int].connect(self.selectGraph)

    def get_layout(self):
        return self.vbox

    def algSelect(self, text):
        self.algorithm = text
        if text == 'force directed':
            self.algOpt.enabled('forced', True)
        elif text == 'random':
            self.algOpt.enabled('forced', False)
            self.algOpt.enabled('rand', True)
        else:
            self.algOpt.enabled('forced', False)
            self.algOpt.enabled('rand', False)

    def newGraph(self, graphId):
        # Informs the graph control group to update graph id
        self.graphCtrl.addGraphId(graphId)

    def killGraph(self):
        return self.graphCtrl.delGraphId()

    def selectGraph(self, data):
        # self.selectedCanvasId = dat
        Call.graphId = int(data)
        r = Call.get_stat()
        self.importCtrl.nodeCount.setText("Nodes: " + str(r[1]))
        self.importCtrl.edgeCount.setText("Edges: " + str(r[0]))
        # TODO: Enable only the graph that is selected

    def applyAlg(self):
        if self.algorithm == 'force directed':
            algText = self.algOpt.get_text('force directed')
        elif self.algorithm == 'random':
            algText = self.algOpt.get_text('random')
        else:
            algText = ['']
        # Applies distribution algorithm on selected graph
        print("apply {}".format(self.algorithm))
        Call.apply_alg(self.algorithm, *algText)

    # Activates the import wizard
    def import_wizard(self):
        exPopup = ImportWizard(self)
        exPopup.setGeometry(100, 200, 800, 600)
        exPopup.show()
        self.graphCtrl.enable(True)

    # Populate list widget with colors and type names
    def setTypeList(self, colorMap):
        for k in colorMap.keys():
            self.typeList.addType(k, colorMap[k])
