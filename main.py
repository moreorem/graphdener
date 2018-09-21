# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QHBoxLayout, QMessageBox, QFrame)
from PyQt5.QtGui import QIcon
from lib.widgets.controls import ControlWidgets
from lib.widgets.canvas import CanvasWidget
from lib.services.backend import Backend
from lib.services.actions import Call

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Main window details
        self.setWindowTitle('Graphdener')
        self.move(300, 300)
        # self.resize(1400, 1000)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))

        # Initialize main container
        self.mainFrame = QFrame(self)
        self.setCentralWidget(self.mainFrame)
        # Set main container's layout
        self.mainFrameLayout = QHBoxLayout()
        self.mainFrame.setLayout(self.mainFrameLayout)

        # Initialize control group
        self.controls = ControlWidgets()
        # Add control group to main frame
        self.mainFrameLayout.addLayout(self.controls.get_layout())
        self.mainFrameLayout.addWidget(self.controls)

        # Initialize canvas area
        self.canvasArea = CanvasWidget()
        # Add canvas to main frame
        self.mainFrameLayout.addLayout(self.canvasArea.get_layout())
        self.mainFrameLayout.addWidget(self.canvasArea)

        # Draw / Close Button action
        self.controls.drawBtn.clicked.connect(self.drawGraph)
        self.controls.closeBtn.clicked.connect(self.killGraph)

        # Start backend
        Backend.start() #uncomment when not debugging
        Call.connect()

    # FIXME: Deprecated
    def getCanvasId(self):
        self.canvasArea.canvasId = self.controls.canvasId

    def drawGraph(self):
        canvasId = self.controls.maxCanvasId
        self.controls.changeCanvasId('add')
        # Inform backend to create and initialize the graph
        Call.create_graph(canvasId)
        Call.populate_graph(canvasId)
        # Draw the graph on a new canvas with that ID
        self.canvasArea.createCanvas(canvasId)

    def killGraph(self):
        self.controls.changeCanvasId('remove')
        canvasId = self.controls.selectedCanvasId
        self.canvasArea.closeCanvas(canvasId)

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
