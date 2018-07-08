from PyQt5.QtWidgets import (QMainWindow, QLayout, QPushButton,
                             QHBoxLayout, QMessageBox, QLabel, QFileDialog)
from PyQt5 import QtWidgets
from ..services.bendcomm import *

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)


class ImportWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.setWindowTitle("Import Wizard")

        # Trigger close event when pressing Finish button to redirect variables to backend
        self.finished.connect(self.closeEvent)

    def closeEvent(self):
        print("hallelujah!")
        if len(self.edgeListPath):
            print(self.edgeListPath)
            Client.send_paths(self.edgeListPath)

    def set_edgeListPath(self, path):
        self.edgeListPath = path


class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.comboBox = QIComboBox(self)
        self.comboBox.addItem("Python", "/path/to/filename1")
        self.comboBox.addItem("PyQt5", "/path/to/filename2")
        self.openFileBtn = QPushButton("Import Edge List")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.openFileBtn)
        self.setLayout(layout)

        self.openFileBtn.clicked.connect(self.openFileNameDialog)
        parent.edgeListPath = ''

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.parent.set_edgeListPath(fileName)

    def get_parent(self):
        return self.parent


class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Example text")
        self.label2.setText("Example text")



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = ImportWizard()
    wizard.show()
    sys.exit(app.exec_())
