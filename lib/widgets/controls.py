from PyQt5.QtWidgets import (QApplication,
QWidget, QFileDialog, QMainWindow,
QPushButton, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout)
from ..services.backend import Backend
from ..services.actions import Call


class ControlWidgets(QWidget):
    '''Class that contains the buttons and sliders that control the graph and general interaction'''

    def __init__(self, parent):
        super(ControlWidgets, self).__init__(parent)
        self.__controls()
        self.__layout()

        self.button1.clicked.connect(Backend.start)
        self.button2.clicked.connect(Backend.stop)

        # self.button4.clicked.connect(Backend.create_random_dataset)
        self.button5.clicked.connect(Backend.list_all_vertices)
        self.button6.clicked.connect(Call.get_positions)

    def __controls(self):
        self.button1 = QPushButton("start")
        self.button2 = QPushButton("stop")
        self.button3 = QPushButton("Import Wizard")

        self.button4 = QPushButton("Create Node")
        self.button5 = QPushButton("Get Vertices")
        self.button6 = QPushButton("Get Positions")

        self.button7 = QPushButton("Re-Draw")

    def __layout(self):
        self.vbox = QVBoxLayout()

        # add buttons and control widgets in the container box
        self.vbox.addWidget(self.button1)
        self.vbox.addWidget(self.button2)
        self.vbox.addWidget(self.button3)
        self.vbox.addWidget(self.button4)
        self.vbox.addWidget(self.button5)
        self.vbox.addWidget(self.button6)
        self.vbox.addWidget(self.button7)

    def get_layout(self):
        return self.vbox

    def connect_client(self):
        try:
            Backend.connect_client()
        except Backend.Error as e:
            print(e)

