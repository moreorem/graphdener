from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import QPointF
from PyQt5 import QtGui
import math


class ColorLegend(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # set lineColor
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(3) # set lineWidth
        self.move(200, 600)
        # set fillColor
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
        # polygon with n points, radius, angle of the first point
        self.polygon = self.createPoly(8, 150, 0)

    def createPoly(self, n, r, s):
        polygon = QtGui.QPolygonF()
        w = 360 / n # angle per step
        for i in range(n): # add the points of polygon
            t = w * i + s
            x = r * math.cos(math.radians(t))
            y = r * math.sin(math.radians(t))
            polygon.append(QPointF(self.width() / 2 + x, self.height() / 2 + y))

        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)



# class ColorSquare(ColorLegend):
#     def __init__(self, parent=None):
#         ColorLegend.__init__(self, parent)
#         # set lineColor
#         self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
#         self.pen.setWidth(3) # set lineWidth
#         self.move(1, 1)
#         # set fillColor
#         self.brush = QtGui.QBrush(QtGui.QColor(55, 55, 55, 255))
#         # polygon with n points, radius, angle of the first point
#         self.polygon = self.createPoly(10, 10, 0)

#     def createPoly(self, n, r, s):
#         polygon = QtGui.QPolygonF()
#         w = 360 / n # angle per step
#         for i in range(n): # add the points of polygon
#             t = w * i + s
#             x = r * math.cos(math.radians(t))
#             y = r * math.sin(math.radians(t))
#             polygon.append(QPointF(self.width() / 2 + x, self.height() / 2 + y))

#         return polygon

#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         painter.setPen(self.pen)
#         painter.setBrush(self.brush)
#         painter.drawPolygon(self.polygon)

