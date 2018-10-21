# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QMessageBox, QGridLayout)
from lib.widgets import (ControlWidgets, CanvasWidget, StatusBar)
from lib.widgets.wizard import ImportWizard
from lib.services.backend import Backend
from lib.services.actions import Call
from PyQt5.QtGui import QIcon

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


# PENDING: Add color coded legend for the node types
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Main window details
        self.setWindowTitle('Graphdener')
        self.move(300, 300)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))
        # BUILD THE GUI FROM OUTER TO INNER LAYOUTS
        # Initialize main container
        self.totalWidget = QWidget()
        # Initialize status bar
        self.statusBar = StatusBar()
        # Initialize canvas area
        self.canvas = CanvasWidget()
        # Initialize control group
        self.controls = ControlWidgets()
        # Set main container's layout
        self.totalLayout = QGridLayout()
        # Add Controls layout
        self.totalLayout.addLayout(self.controls.get_layout(), 0, 0)
        # Add canvas area to main frame
        self.totalLayout.addWidget(self.canvas, 0, 1)
        # Add status bar widget to total
        self.totalLayout.addWidget(self.statusBar, 1, 0)
        # Declare analogies
        self.totalLayout.setRowStretch(1, 0)
        self.totalLayout.setRowStretch(0, 1)
        self.totalLayout.setColumnStretch(0, 0)
        self.totalLayout.setColumnStretch(1, 5)
        self.totalWidget.setLayout(self.totalLayout)
        self.setCentralWidget(self.totalWidget)
        self.__actions()
        # Declare the console to the action class
        Call.console = self.statusBar
        # Start backend
        # Backend.start()
        Call.connect()

    # Bind actions
    def __actions(self):
        self.controls.graphCtrl.closeBtn.clicked.connect(self.killGraph)
        self.controls.importCtrl.importBtn.clicked.connect(self.import_wizard)
        self.controls.graphCtrl.graphSelector.activated[int].connect(self.selectGraph)
        self.controls.algCtrl.animateBtn.clicked.connect(self.animate)

    # Activates the import wizard
    def import_wizard(self):
        exPopup = ImportWizard(self)
        exPopup.setGeometry(100, 200, 800, 600)
        exPopup.show()

    # Activate backend to create structs and draw graph
    def drawGraph(self):
        # Tell canvaswidget to do the draw process
        self.canvas.drawGraph()
        graphId = Call.graphId
        # Insert GraphID in dropdown selector
        self.controls.graphCtrl.addGraphId(graphId)
        self.controls.graphCtrl.enable(True)
        # Populate the legend
        self.controls.typeList.clear()
        self.controls.setTypeList(self.canvas.colorTypes)
        # Print the graph stats
        r = Call.get_stat()
        self.controls.importCtrl.nodeCount.setText("Nodes: " + str(r[1]))
        self.controls.importCtrl.edgeCount.setText("Edges: " + str(r[0]))
        # Inform controls about changes
        return graphId

    # Activates every time you select a graph from the dropdown
    def selectGraph(self, data):
        Call.graphId = int(data)
        r = Call.get_stat()
        self.controls.importCtrl.nodeCount.setText("Nodes: " + str(r[1]))
        self.controls.importCtrl.edgeCount.setText("Edges: " + str(r[0]))
        self.canvas.display(Call.graphId)

    # Destroy graph which is selected
    def killGraph(self):
        graphId = Call.graphId
        self.controls.graphCtrl.delGraphId()
        self.canvas.closeGraph(graphId)

    # Ask before quit dialog
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(
            self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Backend.stop()
        else:
            event.ignore()

    def animate(self):
        if self.controls.toggleAnimation():
            self.canvas.animate()
            self.controls.toggleAnimation()
        else:
            self.canvas.animate()
            self.controls.toggleAnimation()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
