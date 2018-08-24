# !/usr/bin/python3.6
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QHBoxLayout, QMessageBox, QFrame)
from PyQt5.QtGui import QIcon
from lib.widgets.controls import ControlWidgets
from lib.widgets.canvas import CanvasWidget
from lib.graphics.wizard import ImportWizard
from lib.services.backend import Backend

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Main window details
        self.setWindowTitle('Graphdener')
        self.move(300, 300)
        self.resize(800, 600)
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

        # Re-draw Button action
        self.controls.button7.clicked.connect(self.canvasArea.create_canvas)
        # Import wizard Button
        self.controls.button3.clicked.connect(self.import_wizard)

        # Start backend
        # Backend.start()

    # Ask before quit
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(
            self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            Backend.stop()

        else:
            event.ignore()

    # Activates the import wizard
    def import_wizard(self):
        exPopup = ImportWizard(self)
        exPopup.setGeometry(100, 200, 800, 600)
        exPopup.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
