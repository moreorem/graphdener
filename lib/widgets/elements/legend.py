from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel, QVBoxLayout, QListView
from PyQt5.QtGui import (QColor, QPainter, QStandardItemModel, QStandardItem, QBrush)
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPixmap
import math


class ColorLegend(QListView):
    def __init__(self, parent=None):
        super(ColorLegend, self).__init__(parent)
        model = QStandardItemModel(self)
        item = QStandardItem()
        item.setText("BALALSKDL")
        item.setBackground(QColor(255,255,0,255))
        self.setModel(model)
        model.appendRow(item)
        self.show()

    def addType(self, name, color):
        pass
