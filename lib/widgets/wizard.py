from PyQt5.QtWidgets import (QPushButton, QLabel, QFileDialog,
                             QComboBox, QWizard, QWizardPage, QLineEdit,
                             QVBoxLayout, QApplication, QHBoxLayout)
from ..services.actions import *


class QIComboBox(QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)


class ImportWizard(QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.setWindowTitle("Import Wizard")
        # Trigger close event when pressing Finish button to redirect variables to backend
        self.button(QWizard.FinishButton).clicked.connect(self.onFinished)
        self.filepath = [None, None]

    def onFinished(self):
        print("Finish")

        # Communicate with backend to send information
        Call.connect()
        # Transmit paths to backend
        Call.send_paths(self.filepath)


class Page1(QWizardPage):

    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.comboBox = QIComboBox(self)
        self.openFileBtn = QPushButton("Import Node List")
        self.stepLabel = QLabel()
        self.formatLabel = QLabel()
        self.text1 = QLineEdit()
        self.text2 = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.openFileBtn)
        layout.addWidget(self.formatLabel)

        patternLayout = QHBoxLayout()
        patternLayout.addWidget(self.text1)
        patternLayout.addWidget(self.comboBox)
        patternLayout.addWidget(self.text2)
        layout.addLayout(patternLayout)

        self.setLayout(layout)
        # Bind actions
        self.openFileBtn.clicked.connect(self.openFileNameDialog)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        # if user selected a file store its path to a variable
        if fileName:
            self.wizard().filepath[0] = fileName

    def initializePage(self):
        self.stepLabel.setText("Nodes information")
        self.formatLabel.setText("Nodes file format")


class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.setWindowTitle("Edge phase")

        self.label1 = QLabel()
        self.openFileBtn = QPushButton("Import Edge List")

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.openFileBtn)

        self.setLayout(layout)
        # Bind actions
        self.openFileBtn.clicked.connect(self.openFileNameDialog)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",
            "All Files (*);;Python Files (*.py)", options=options)
        # if user selected a file store its path to a variable
        if fileName:
            self.wizard().filepath[1] = fileName

    def initializePage(self):
        self.label1.setText("Edges information")
        # self.label2.setText("Example text")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wizard = ImportWizard()
    wizard.show()
    sys.exit(app.exec_())
