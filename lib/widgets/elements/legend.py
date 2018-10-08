from PyQt5.QtWidgets import QWidget, QListView
from PyQt5.QtGui import (QColor, QStandardItemModel, QStandardItem, QBrush)
import math


class ColorLegend(QListView):
    def __init__(self, parent=None):
        super(ColorLegend, self).__init__(parent)
        self.model = QStandardItemModel(self)
        self.setModel(self.model)

    def addType(self, name, color):
        print(color)
        item = QStandardItem()
        item.setText(name)
        item.setSelectable(False)
        item.setBackground(QColor(*color, 255))
        self.model.appendRow(item)
