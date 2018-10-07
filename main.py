# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QHBoxLayout, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon
from lib.widgets import (ControlWidgets, CanvasWidget, StatusBar)
# from lib.widgets.controls import ControlWidgets
# from lib.widgets.canvas import CanvasWidget
from lib.services.backend import Backend
from lib.services.actions import Call
# from lib.widgets.elements.legend import ColorLegend

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


# PENDING: Add color coded legend for the node types
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Main window details
        self.setWindowTitle('Graphdener')
        self.move(300, 300)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))

        # BUILD THE GUI FROM OUTER TO INNER LAYOUTS
        # Initialize main container
        self.totalWidget = QWidget()
        # Initialize status bar
        self.statusBar = StatusBar(self)
        # Set main container's layout
        self.totalLayout = QVBoxLayout()
        self.totalWidget.setLayout(self.totalLayout)
        # Set controls and canvas containers layout
        self.mainFrameLayout = QHBoxLayout()
        # Add mainframe layout to total
        self.totalLayout.addLayout(self.mainFrameLayout)
        # Add status bar widget to total
        self.totalLayout.addWidget(self.statusBar)
        # Initialize control group
        self.controls = ControlWidgets(self)
        # Initialize canvas area
        self.canvasArea = CanvasWidget(self)
        # Add control group to main frame
        self.mainFrameLayout.addLayout(self.controls.get_layout())
        self.mainFrameLayout.addWidget(self.controls)
        # Add canvase area to main frame
        self.mainFrameLayout.addWidget(self.canvasArea)
        # self.mainFrameLayout.addLayout(self.canvasArea.get_layout())

        self.setCentralWidget(self.totalWidget)
        self.mainFrameLayout.addStretch(1)

        # Draw / Close Button action
        self.controls.graphCtrl.drawBtn.clicked.connect(self.drawGraph)
        self.controls.graphCtrl.closeBtn.clicked.connect(self.killGraph)

        Call.console = self.statusBar
        # Start backend
        # Backend.start()
        Call.connect()

    def drawGraph(self):
        # Tell canvaswidget to do the draw process
        graphId = self.canvasArea.createCanvas()
        # Inform controls about changes
        self.controls.newGraph(graphId)

    def killGraph(self):
        graphId = self.controls.killGraph()
        self.canvasArea.closeCanvas(graphId)

    # Ask before quit
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(
            self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Backend.stop()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
