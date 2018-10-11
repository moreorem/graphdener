# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QMessageBox, QGridLayout)
from lib.widgets import (ControlWidgets, CanvasWidget, StatusBar)
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
        self.setMinimumSize(800, 800)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))

        # BUILD THE GUI FROM OUTER TO INNER LAYOUTS
        # Initialize main container
        self.totalWidget = QWidget()
        # Initialize status bar
        self.statusBar = StatusBar()
        # Initialize canvas area
        self.canvasArea = CanvasWidget()
        # Initialize control group
        self.controls = ControlWidgets(self)
        # Set main container's layout
        self.totalLayout = QGridLayout()
        # Set controls and canvas containers layout
        # self.mainFrameLayout = QHBoxLayout()
        # Add mainframe layout to total
        # self.totalLayout.addLayout(self.mainFrameLayout)
        # Add control group to main frame
        # self.totalLayout.addWidget(self.controls, 0, 0)
        self.totalLayout.addLayout(self.controls.get_layout(), 0, 0)
        # Add canvase area to main frame
        # self.totalLayout.addLayout(self.canvasArea.get_layout(), 0,1)
        self.totalLayout.addWidget(self.canvasArea, 0, 1)
        # Add status bar widget to total
        self.totalLayout.addWidget(self.statusBar, 1, 0)
        # Declare analogies
        self.totalLayout.setRowStretch(1, 0)
        self.totalLayout.setRowStretch(0, 1)
        self.totalLayout.setColumnStretch(0, -1)
        self.totalLayout.setColumnStretch(1, 5)

        self.totalWidget.setLayout(self.totalLayout)
        self.setCentralWidget(self.totalWidget)
        # self.totalLayout.addStretch(1)

        # Draw / Close Button action
        self.controls.graphCtrl.drawBtn.clicked.connect(self.drawGraph)
        self.controls.graphCtrl.closeBtn.clicked.connect(self.killGraph)
        # Declare the console to the action class
        Call.console = self.statusBar
        # Start backend
        # Backend.start()
        Call.connect()

    def drawGraph(self):
        # Tell canvaswidget to do the draw process
        graphId = self.canvasArea.createCanvas()
        self.controls.setTypeList(self.canvasArea.colorTypes)
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
