# !/usr/bin/python3
import sys
import os
from subprocess import Popen, PIPE, call as call_ext
from PyQt5.QtWidgets import (QApplication,
QWidget, QFileDialog, QMainWindow, QLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QIcon
from lib.widgets.controls import ControlWidgets
from lib.widgets.canvas import CanvasWidget
from lib.graphics.wizard import ImportWizard

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PGMP'
        self.mainWidget = QWidget(self)
        # self.setCentralWidget(self.mainWidget)
        self.canvasWidget = CanvasWidget(self.mainWidget)

        self.ctrlWidgets = ControlWidgets(self.mainWidget)

        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.mainLayout.sizeConstraint = QLayout.SetDefaultConstraint
        self.mainLayout.addLayout(self.ctrlWidgets.get_layout())

        self.canvasLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.canvasWidget.get_layout())
        self.initUI()

    def initUI(self):
        self.move(300, 300)
        self.resize(800, 600)
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.mainWidget)
        self.setWindowIcon(QIcon(SCRIPT_DIR + os.path.sep + 'icon.png'))

        self.ctrlWidgets.button7.clicked.connect(self.canvasWidget.create_canvas)
        self.ctrlWidgets.button3.clicked.connect(self.import_wizard)


    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.ctrlWidgets.stop_server()

        else:
            event.ignore()

    
    def import_wizard(self):
        name = 'Import Wizard'
        exPopup = ImportWizard(self)
        exPopup.setGeometry(100, 200, 100, 100)
        exPopup.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
