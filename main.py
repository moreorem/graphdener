# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon
from lib.widgets.controls import ControlWidgets
from lib.widgets.canvas import CanvasWidget
from lib.graphics.graphvis import GraphCanvas
from lib.graphics.wizard import ImportWizard
from lib.services.backend import Backend
from lib.services.actions import Call
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PGMP'
        self.mainWidget = QWidget(self)

        # self.canvasWidget = CanvasWidget(self.mainWidget)
        # self.canvasWidget = GraphCanvas(self.mainWidget)
        self.canvasWidget = QWidget(self) # test


        self.ctrlWidgets = ControlWidgets(self.mainWidget)

        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.mainLayout.sizeConstraint = QLayout.SetDefaultConstraint
        self.mainLayout.addLayout(self.ctrlWidgets.get_layout())
        # self.mainLayout.addLayout(self.canvasWidget.get_layout())
        self.canvas = None
        self.canvasLayout = QHBoxLayout()
        self.initUI()

    def initUI(self):
        self.move(300, 300)
        self.resize(800, 600)
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.mainWidget)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))

        # Re-draw Button action
        self.ctrlWidgets.button7.clicked.connect(
            self.create_canvas)
        # Import wizard Button
        self.ctrlWidgets.button3.clicked.connect(self.import_wizard)

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(
            self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            Backend.stop()

        else:
            event.ignore()

    def import_wizard(self):
        exPopup = ImportWizard(self)
        exPopup.setGeometry(100, 200, 800, 600)
        exPopup.show()

    def create_canvas(self):
        # FIXME: When pressing redraw button the interface corrupts
        if self.canvas is not None:
            pass
            # self.close_canvas()

        # Get node positions from backend
        nodes = Call.get_positions()
        colors = np.ones((len(nodes), 4), dtype=np.float32)
        for i in range(len(nodes)):
            colors[i] = (i / 500, 1.0 - i / 500, 0, 1)

        nd = np.matrix(nodes)
        self.canvas = GraphCanvas(nd, colors).native
        self.canvasLayout.addWidget(self.canvas)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
