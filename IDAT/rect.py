# -*- coding: utf-8 -*-
# @Author  : LG

from PyQt5 import QtCore, QtWidgets, QtGui
import typing

class Vertex(QtWidgets.QGraphicsPathItem):
    def __init__(self, rect, index):
        super(Vertex, self).__init__()
        self.rect = rect
        self.index = index
        self.color = QtGui.QColor('#ff0000')
        self.hover_size = 5
        self.nohover_size = 3

        self.nohover = QtGui.QPainterPath()
        self.nohover.addEllipse(
            QtCore.QRectF(-self.nohover_size // 2, -self.nohover_size // 2, self.nohover_size, self.nohover_size))
        self.hover = QtGui.QPainterPath()
        self.hover.addEllipse(
            QtCore.QRectF(-self.hover_size // 2, -self.hover_size // 2, self.hover_size, self.hover_size))

        self.setPath(self.nohover)
        self.setBrush(self.color)
        self.setPen(QtGui.QPen(self.color, 1))
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.setZValue(1e5)

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent'):
        self.setPath(self.hover)
        return super(Vertex, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent'):
        self.setPath(self.nohover)
        return super(Vertex, self).hoverLeaveEvent(event)

    def itemChange(self, change: 'QtWidgets.QGraphicsItem.GraphicsItemChange', value: typing.Any):
        if change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange and self.isEnabled():
            if not self.rect.is_completed:
                return super(Vertex, self).itemChange(change, value)
            value.setX(max(0, value.x()))
            value.setX(min(value.x(), self.scene().width()))
            value.setY(max(0, value.y()))
            value.setY(min(value.y(), self.scene().height()))
            self.rect.movePoint(self.index, value)

            self.scene().mainwindow.set_changed(True)
        return super(Vertex, self).itemChange(change, value)


class Rect(QtWidgets.QGraphicsRectItem):
    def __init__(self):
        super(Rect, self).__init__()
        self.points = []
        self.vertexs = []
        self.is_completed = False
        self.is_difficult = False
        self.color = QtGui.QColor('#000000')
        self.hover_alpha = 80
        self.nohover_alpha = 0

        self.setPen(QtGui.QPen(self.color, 1))
        self.setBrush(QtGui.QBrush(self.color, QtCore.Qt.BrushStyle.FDiagPattern))
        self.setZValue(1e4)

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def addPoint(self, pos):
        self.points.append(pos)

    def movePoint(self, index, pos):
        if index < 0 or index > len(self.points):
            return
        pos = self.mapFromScene(pos)
        if len(self.points) == 2:
            self.points[index] = pos
        elif len(self.points) == 4:
            if index == 0:
                self.points[1].setY(pos.y())
                self.points[2].setX(pos.x())
                self.moveVertex(1,self.mapToScene(self.points[1]))
                self.moveVertex(2,self.mapToScene(self.points[2]))
                self.points[0] = pos
            elif index == 1:
                self.points[0].setY(pos.y())
                self.points[3].setX(pos.x())
                self.moveVertex(0,self.mapToScene(self.points[0]))
                self.moveVertex(3,self.mapToScene(self.points[3]))
                self.points[1] = pos
            elif index == 2:
                self.points[0].setX(pos.x())
                self.points[3].setY(pos.y())
                self.moveVertex(0,self.mapToScene(self.points[0]))
                self.moveVertex(3,self.mapToScene(self.points[3]))
                self.points[2] = pos

            elif index == 3:
                self.points[1].setX(pos.x())
                self.points[2].setY(pos.y())
                self.moveVertex(1,self.mapToScene(self.points[1]))
                self.moveVertex(2,self.mapToScene(self.points[2]))
                self.points[3] = pos
        self.redraw()

    def moveVertex(self, index, pos):
        vertex = self.vertexs[index]
        vertex.setEnabled(False)
        vertex.setPos(pos)
        vertex.setEnabled(True)

    def removePoint(self, index):
        self.points.pop(index)
        self.redraw()

    def complete(self, category, color, difficult=False):
        self.category = category
        self.is_difficult = difficult
        self.color = QtGui.QColor(color)
        self.setPen(QtGui.QPen(self.color, 1, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap))
        self.color.setAlpha(self.nohover_alpha)
        self.setBrush(self.color)

        lt, rb = self.points
        self.points.clear()
        lt, rt, lb, tb = lt, QtCore.QPointF(rb.x(), lt.y()), QtCore.QPointF(lt.x(), rb.y()), rb
        self.points = [lt, rt, lb, tb]
        for index, point in enumerate(self.points):
            vertex = Vertex(self, index)
            vertex.color = self.color
            vertex.setPos(point)
            self.vertexs.append(vertex)
            self.scene().addItem(vertex)
        self.redraw()
        self.is_completed = True
        
    def redraw(self):
        if len(self.points) == 2:
            xmin, ymin = min(self.points[0].x(), self.points[1].x()), min(self.points[0].y(), self.points[1].y())
            w, h = abs(self.points[0].x() - self.points[1].x()), abs(self.points[0].y() - self.points[1].y())
            self.setRect(xmin, ymin, w, h)

        if len(self.points) == 4:
            xmin = min(self.points[0].x(), self.points[1].x(), self.points[2].x(), self.points[3].x())
            xmax = max(self.points[0].x(), self.points[1].x(), self.points[2].x(), self.points[3].x())
            ymin = min(self.points[0].y(), self.points[1].y(), self.points[2].y(), self.points[3].y())
            ymax = max(self.points[0].y(), self.points[1].y(), self.points[2].y(), self.points[3].y())
            w, h = xmax - xmin, ymax - ymin
            self.setRect(xmin, ymin, w, h)

    def hoverEnterEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent'):
        if self.is_completed:
            self.color.setAlpha(self.hover_alpha)
            self.setBrush(self.color)
        return super(Rect, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent'):
        if self.is_completed:
            self.color.setAlpha(self.nohover_alpha)
            self.setBrush(self.color)
        return super(Rect, self).hoverLeaveEvent(event)

    def itemChange(self, change: 'QtWidgets.QGraphicsItem.GraphicsItemChange', value: typing.Any):
        if self.is_completed:
            if change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged and self.isEnabled():
                if self.isSelected():
                    color = QtGui.QColor('#00A0FF')
                    color.setAlpha(self.hover_alpha)
                    self.setBrush(color)
                else:
                    self.setBrush(self.color)

                self.scene().mainwindow.dock_label_set_selected(self)

            if change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange:
                bias = value
                l, t, b, r = self.boundingRect().left(), self.boundingRect().top(), self.boundingRect().bottom(), self.boundingRect().right()
                if l + bias.x() < 0: bias.setX(-l)
                if r + bias.x() > self.scene().width(): bias.setX(self.scene().width() - r)
                if t + bias.y() < 0: bias.setY(-t)
                if b + bias.y() > self.scene().height(): bias.setY(self.scene().height() - b)

                for index, point in enumerate(self.points):
                    self.moveVertex(index, point + bias)
                self.scene().mainwindow.set_changed(True)
        return super(Rect, self).itemChange(change, value)

    def mouseDoubleClickEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.scene().edit_rect()

    def create_from_xyxy(self, category, xmin, ymin, xmax, ymax, is_difficult, color='#6D6D6D'):
        self.points = [QtCore.QPointF(xmin, ymin), QtCore.QPointF(xmax, ymax)]
        self.complete(category, color=color, difficult=is_difficult)

    def set_visible(self, visible):
        self.setVisible(visible)
        for vertex in self.vertexs:
            vertex.setVisible(visible)
