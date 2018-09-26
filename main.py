# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon
from lib.widgets.controls import ControlWidgets
from lib.widgets.canvas import CanvasWidget
from lib.services.backend import Backend
from lib.services.actions import Call
from lib.widgets.elements.legend import ColorLegend

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Main window details
        self.setWindowTitle('Graphdener')
        self.move(300, 300)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))

        # Initialize main container
        self.mainFrame = QWidget()
        self.setCentralWidget(self.mainFrame)
        # Set main container's layout
        self.mainFrameLayout = QHBoxLayout()
        self.mainFrame.setLayout(self.mainFrameLayout)

        # Initialize control group
        self.controls = ControlWidgets()
        # Add control group to main frame
        self.mainFrameLayout.addLayout(self.controls.get_layout())
        self.mainFrameLayout.addWidget(self.controls)
        self.mainFrameLayout.addStretch(1)

        # Initialize canvas area
        self.canvasArea = CanvasWidget(self)
        # Add canvas to main frame
        self.mainFrameLayout.addLayout(self.canvasArea.get_layout())
        self.mainFrameLayout.addWidget(self.canvasArea)

        # Draw / Close Button action
        self.controls.graphCtrl.drawBtn.clicked.connect(self.drawGraph)
        self.controls.graphCtrl.closeBtn.clicked.connect(self.killGraph)

        # Start backend
        # result = Backend.start()
        Call.connect()

    def drawGraph(self):
        # Inform backend to create and initialize the graph
        graphId = Call.create_graph()
        print("THE NEW GRAPH IS {}".format(graphId))
        Call.populate_graph(graphId)
        self.controls.newGraph(graphId)
        # Draw the graph on a new canvas with that ID
        self.canvasArea.createCanvas(graphId)

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
