from PyQt5.QtWidgets import (QPushButton, QLabel, QFileDialog,
                             QComboBox, QWizard, QWizardPage, QLineEdit,
                             QVBoxLayout, QApplication, QHBoxLayout)
from ..services.actions import Call
from ..func import get_pattern

NODES_COLUMN_NAMES = ['id', 'label', 'type']
EDGES_COLUMN_NAMES = ['id', 'from', 'to', 'label', 'type', 'weight']


class ImportWizard(QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.setWindowTitle("Import Wizard")
        # Trigger close event when pressing Finish button to redirect variables to backend
        self.button(QWizard.FinishButton).clicked.connect(self.onFinished)
        self.button(QWizard.NextButton).clicked.connect(self.page(0).receiveInputs)
        # Initialize variables to send to backend
        self.filepath = [None, None]
        self.nodeColumns = []
        self.nodeDelimiters = []
        self.edgeColumns = []
        self.edgeDelimiters = []

    def onFinished(self):
        print("Finish")
        # Ask input from edge import page
        self.page(1).receiveInputs()

        regexN = get_pattern(self.nodeColumns, self.nodeDelimiters)
        regexE = get_pattern(self.edgeColumns, self.edgeDelimiters)
        # Communicate and transmit to backend
        Call.connect()
        Call.send_paths(self.filepath, regexN, regexE)


class Page1(QWizardPage):

    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.columnSelectors = []
        self.delimiterFields = []
        nCols = len(NODES_COLUMN_NAMES)

        # Initialize comboboxes and text fields
        for i in range(nCols):
            self.columnSelectors.append(QComboBox())
        for i in range(nCols + 1):
            self.delimiterFields.append(QLineEdit())

        self.openFileBtn = QPushButton("Import Node List")
        self.stepLabel = QLabel()
        self.formatLabel = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.openFileBtn)
        layout.addWidget(self.formatLabel)
        patternLayout = QHBoxLayout()

        for i in range(nCols + 1):
            patternLayout.addWidget(self.delimiterFields[i])
            if i < nCols:
                patternLayout.addWidget(self.columnSelectors[i])

        self.setLayout(layout)
        # Insert the layout of the regexp elements
        layout.addLayout(patternLayout)
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

        for comboBox in self.columnSelectors:
            comboBox.addItems(NODES_COLUMN_NAMES)
            comboBox.addItem('-')
            # Initialize first selection to avoid error
            comboBox.selection = NODES_COLUMN_NAMES[0]
            comboBox.activated.connect(self.handleActivated)

        # Initialize textboxes with multi-space expression
        for delimiterField in self.delimiterFields:
            delimiterField.setText('\\s+')
        self.delimiterFields[0].setText('^')

    def handleActivated(self, index):
        self.sender().selection = self.sender().itemText(index)

    def receiveInputs(self):
        ''' activates on next button and sends the input to wizard '''
        self.wizard().nodeDelimiters = [delim.text() for delim in self.delimiterFields]
        self.wizard().nodeColumns = [comboBox.selection for comboBox in self.columnSelectors]


class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        nCols = len(EDGES_COLUMN_NAMES)
        self.setWindowTitle("Edge phase")

        self.stepLabel = QLabel()
        self.openFileBtn = QPushButton("Import Edge List")
        self.columnSelectors = []
        self.delimiterFields = []

        # Initialize comboboxes and text fields
        for i in range(nCols):
            self.columnSelectors.append(QComboBox())
        for i in range(nCols + 1):
            self.delimiterFields.append(QLineEdit())

        layout = QVBoxLayout()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.openFileBtn)
        patternLayout = QHBoxLayout()

        for i in range(nCols + 1):
            patternLayout.addWidget(self.delimiterFields[i])
            if i < nCols:
                patternLayout.addWidget(self.columnSelectors[i])

        self.setLayout(layout)
        # Insert the layout of the regexp elements
        layout.addLayout(patternLayout)
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
        self.stepLabel.setText("Edges information")
        for comboBox in self.columnSelectors:
            comboBox.addItems(EDGES_COLUMN_NAMES)
            comboBox.addItem('-')
            # Initialize first selection to avoid error
            comboBox.selection = NODES_COLUMN_NAMES[0]
            comboBox.activated.connect(self.handleActivated)

        # Initialize textboxes with multi-space expression
        for delimiterField in self.delimiterFields:
            delimiterField.setText('\\s+')
        self.delimiterFields[0].setText('^')

    def handleActivated(self, index):
        self.sender().selection = self.sender().itemText(index)

    def receiveInputs(self):
        ''' activates on next button and sends the input to wizard '''
        self.wizard().edgeDelimiters = [delim.text() for delim in self.delimiterFields]
        self.wizard().edgeColumns = [comboBox.selection for comboBox in self.columnSelectors]


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wizard = ImportWizard()
    wizard.show()
    sys.exit(app.exec_())
