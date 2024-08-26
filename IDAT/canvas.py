# -*- coding: utf-8 -*-
# @Author  : LG

from PyQt5 import QtCore, QtWidgets, QtGui
from IDAT.rect import Rect
from enum import Enum
from typing import List


class DRAWMode(Enum):
    VIEW = 0
    CREATE = 1
    EDIT = 2

class AnnotateMode(Enum):
    DETECT = 0
    MULTI_CLASSIFY = 1


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, mainwindow):
        super(Scene, self).__init__()
        self.mainwindow = mainwindow
        self.pixmap_item:QtWidgets.QGraphicsPixmapItem = None
        self.rects:List[Rect] = []
        self.drawmode:DRAWMode = View
        self.current_rect:Rect = None
        self.leftpressed = False

        self.guide_line_x:QtWidgets.QGraphicsLineItem = None
        self.guide_line_y:QtWidgets.QGraphicsLineItem = None

    def change_draw_to_create(self):
        self.drawmode = DRAWMode.CREATE
        self.leftpressed = False
        if self.pixmap_item is not None:
            self.pixmap_item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
            self.mainwindow.actionCache.setEnabled(True)

    def change_draw_to_edit(self):
        self.drawmode = DRAWMode.EDIT
        self.leftpressed = False
        if self.pixmap_item is not None:
            self.pixmap_item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))

    def change_draw_to_view(self):
        self.drawmode = DRAWMode.VIEW
        self.leftpressed = False
        # 移除辅助线
        if self.guide_line_x is not None and self.guide_line_y is not None:
            if self.guide_line_x in self.items():
                self.removeItem(self.guide_line_x)
            if self.guide_line_y in self.items():
                self.removeItem(self.guide_line_y)
            self.guide_line_x = None
            self.guide_line_y = None
        if self.pixmap_item is not None:
            self.pixmap_item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            self.mainwindow.actionCache.setEnabled(False)

    def load_pixmap(self, pixmap):

        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.pixmap_item.setZValue(0)
        self.pixmap_item.setPixmap(pixmap)
        self.addItem(self.pixmap_item)
        self.setSceneRect(self.pixmap_item.boundingRect())
        self.change_draw_to_view()

    def start_draw(self):
        if len(self.mainwindow.listWidget_categories) < 1:
            QtWidgets.QMessageBox.warning(self.mainwindow, 'Warning', 'The category list is empty.\nSet categorys before labeling.')
            return
        if self.drawmode != DRAWMode.VIEW:
            return
        self.mainwindow.label_visiable_checkbox_click(False)
        self.change_draw_to_create()
        self.current_rect = Rect()
        self.addItem(self.current_rect)

    def finish_draw(self):
        item = self.mainwindow.listWidget_categories.currentItem()
        widget = self.mainwindow.listWidget_categories.itemWidget(item)
        label_category = widget.findChild(QtWidgets.QLabel, 'category')
        label_color = widget.findChild(QtWidgets.QLabel, 'color')
        category = label_category.text()
        color = label_color.text()

        difficult = False
        self.mainwindow.scene.current_rect.complete(category, color, difficult)
        self.mainwindow.scene.rects.append(self.mainwindow.scene.current_rect)
        self.mainwindow.dock_labels_add_label(self.mainwindow.scene.current_rect)
        self.mainwindow.scene.current_rect = None
        self.mainwindow.set_changed(True)
        self.mainwindow.label_visiable_checkbox_click(True)

        self.change_draw_to_view()

    def cache_draw(self):
        if self.current_rect is not None:
            self.removeItem(self.current_rect)
            self.current_rect:Rect = None
        self.mainwindow.label_visiable_checkbox_click(True)
        self.change_draw_to_view()

    def edit_rect(self):
        self.change_draw_to_edit()
        rects = [item for item in self.selectedItems() if item in self.rects]
        if len(rects) < 1:
            return
        rect = rects[0]
        self.mainwindow.edit_label_dialog.init(rect)
        self.mainwindow.edit_label_dialog.show()

    def delete_rect(self):
        for rect in self.selectedItems():
            if rect in self.rects and rect.isSelected():
                index = self.rects.index(rect)
                for vertex in rect.vertexs:
                    self.removeItem(vertex)
                    del vertex
                self.removeItem(rect)
                del rect
                item = self.mainwindow.listWidget_labels.item(index)
                # self.mainwindow.listWidget_labels.removeItemWidget(item)
                self.rects.pop(index)
                self.mainwindow.dock_labels_updata()
        self.mainwindow.set_changed(True)

    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        # 限制范围
        pos = event.scenePos()
        if pos.x() < 0: pos.setX(0)
        if pos.x() > self.width(): pos.setX(self.width())
        if pos.y() < 0: pos.setY(0)
        if pos.y() > self.height(): pos.setY(self.height())

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.drawmode == DRAWMode.CREATE:
                # scenepos = event.scenePos()
                if self.leftpressed:
                    self.current_rect.removePoint(len(self.current_rect.points) - 1)
                    self.current_rect.addPoint(pos)
                    self.finish_draw()
                    self.leftpressed = False
                else:
                    # 第一次点击
                    self.current_rect.addPoint(pos)
                    self.current_rect.addPoint(pos)
                    self.leftpressed = True
        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        # 限制范围
        pos = event.scenePos()
        if pos.x() < 0: pos.setX(0)
        if pos.x() > self.width(): pos.setX(self.width())
        if pos.y() < 0: pos.setY(0)
        if pos.y() > self.height(): pos.setY(self.height())

        if self.drawmode == DRAWMode.CREATE:
            # 移除旧辅助线
            if self.guide_line_x is not None and self.guide_line_y is not None:
                if self.guide_line_x in self.items():
                    self.removeItem(self.guide_line_x)

                if self.guide_line_y in self.items():
                    self.removeItem(self.guide_line_y)

                self.guide_line_x = None
                self.guide_line_y = None
            # 添加新辅助线
            if self.guide_line_x is None and self.width() > 0 and self.height() > 0:
                self.guide_line_x = QtWidgets.QGraphicsLineItem(QtCore.QLineF(pos.x(), 0, pos.x(), self.height()))
                self.addItem(self.guide_line_x)
            if self.guide_line_y is None and self.width() > 0 and self.height() > 0:
                self.guide_line_y = QtWidgets.QGraphicsLineItem(QtCore.QLineF(0, pos.y(), self.width(), pos.y()))
                self.addItem(self.guide_line_y)

            self.current_rect.movePoint(len(self.current_rect.points)-1, pos)

        self.mainwindow.labelCoordinates.setText("({:.0f}, {:.0f})".format(pos.x(), pos.y()))
        super(Scene, self).mouseMoveEvent(event)


class View(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.factor = 0.8
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setMouseTracking(True)

    def zoom(self, factor, point=None):
        mouse_old = self.mapToScene(point) if point is not None else None
        pix_widget = self.transform().scale(factor, factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if pix_widget > 10 or pix_widget < 0.01:
            return
        self.scale(factor,factor)
        if point is not None:
            mouse_now = self.mapToScene(point)
            center_now = self.mapToScene(self.viewport().width() // 2, self.viewport().height() // 2)
            center_new = mouse_old - mouse_now + center_now
            self.centerOn(center_new)

    def zoom_fit(self):
        self.fitInView(0, 0, self.scene().width(), self.scene().height(),  QtCore.Qt.AspectRatioMode.KeepAspectRatio)

    def zoom_in(self):
        self.zoom(1 / self.factor)

    def zoom_out(self):
        self.zoom(self.factor)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        angel= event.angleDelta()
        if angel.y() < 0:
            self.zoom(self.factor, event.pos())
        elif angel.y() > 0:
            self.zoom(1/self.factor, event.pos())
        else:
            pass
