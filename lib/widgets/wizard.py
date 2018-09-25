from PyQt5.QtWidgets import (QPushButton, QLabel, QFileDialog,
                             QComboBox, QWizard, QWizardPage, QLineEdit,
                             QVBoxLayout, QHBoxLayout)
from ..services.actions import Call
from ..func import get_pattern
from ..statics import NODECNAMES, EDGECNAMES, UNIFIEDCNAMES


# TODO: Call new graph after import wizard
class ImportWizard(QWizard):
    def __init__(self, parent=None, isSingleFile=False):
        super(ImportWizard, self).__init__(parent)
        self.isSingleFile = isSingleFile
        if isSingleFile:
            self.addPage(Page2b(self))
        else:
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
        self.unifiedColumns = []
        self.unifiedDelimiters = []

    def onFinished(self):
        print("Finish")
        # Ask input from edge import page
        self.page(1).receiveInputs()
        Call.connect()
        regex = ['', '']

        if self.isSingleFile:
            regexU = get_pattern(self.unifiedColumns, self.unifiedDelimiters)
            regex[0] = regexU
            colNames = self.unifiedColumns
        else:
            regexN = get_pattern(self.nodeColumns, self.nodeDelimiters)
            regexE = get_pattern(self.edgeColumns, self.edgeDelimiters)
            regex[0] = regexN
            regex[1] = regexE
            colNames = [self.nodeColumns, self.edgeColumns]
            print(regex)
        # Send items to backend
        result = Call.send_paths(self.filepath, regex, self.isSingleFile, colNames)
        # TODO: Make use of return state to enable graph controls
        if result == 'paths imported':
            return True


class Page1(QWizardPage):

    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.columnSelectors = []
        self.delimiterFields = []
        nCols = len(NODECNAMES)

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
        i = 0
        for comboBox in self.columnSelectors:
            comboBox.addItems(NODECNAMES)
            comboBox.addItem('-')
            # Initialize first selection to avoid error
            comboBox.setCurrentIndex(i)
            comboBox.activated.connect(self.handleActivated)
            comboBox.selection = comboBox.currentText()
            i += 1

        # Initialize textboxes with multi-space expression
        for delimiterField in self.delimiterFields:
            delimiterField.setText('\\s+')
        self.delimiterFields[0].setText('')
        self.delimiterFields[-1].setText('')

    def handleActivated(self, index):
        self.sender().selection = self.sender().itemText(index)

    def receiveInputs(self):
        ''' activates on next button and sends the input to wizard '''
        self.wizard().nodeDelimiters = [delim.text() for delim in self.delimiterFields]
        self.wizard().nodeColumns = [comboBox.selection for comboBox in self.columnSelectors]


class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        nCols = len(EDGECNAMES)
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
        i = 0
        for comboBox in self.columnSelectors:
            comboBox.addItems(EDGECNAMES)
            comboBox.addItem('-')
            # Initialize first selection to avoid error
            comboBox.setCurrentIndex(i)
            comboBox.activated.connect(self.handleActivated)
            comboBox.selection = comboBox.currentText()
            i += 1

        # Initialize textboxes with multi-space expression
        for delimiterField in self.delimiterFields:
            delimiterField.setText('\\s+')
        self.delimiterFields[0].setText('')
        self.delimiterFields[-1].setText('')

    def handleActivated(self, index):
        self.sender().selection = self.sender().itemText(index)

    def receiveInputs(self):
        ''' activates on next button and sends the input to wizard '''
        self.wizard().edgeDelimiters = [delim.text() for delim in self.delimiterFields]
        self.wizard().edgeColumns = [comboBox.selection for comboBox in self.columnSelectors]


# To be called only on single file Import
class Page2b(QWizardPage):
    def __init__(self, parent=None):
        super(Page2b, self).__init__(parent)
        nCols = len(UNIFIEDCNAMES)
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
            comboBox.addItems(EDGECNAMES)
            comboBox.addItem('-')
            # Initialize first selection to avoid error
            comboBox.selection = NODECNAMES[0]
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
