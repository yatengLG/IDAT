# -*- coding: utf-8 -*-
# @Author  : LG

from PyQt5 import QtCore, QtWidgets, QtGui
from rect import Rect
from enum import Enum
from typing import List
import numpy as np
from PIL import Image
import cv2

class Mode(Enum):
    VIEW = 0
    CREATE = 1
    EDIT = 2

class DRAWMODE(Enum):
    RECTANGLE = 0
    SEGMENTANYTHING = 1

class AnnotateMode(Enum):
    DETECT = 0
    MULTI_CLASSIFY = 1


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, mainwindow):
        super(Scene, self).__init__()
        self.mainwindow = mainwindow
        self.pixmap_item:QtWidgets.QGraphicsPixmapItem = None
        self.rects:List[Rect] = []
        self.mode:Mode = Mode.VIEW
        self.draw_mode:DRAWMODE = DRAWMODE.RECTANGLE
        self.current_rect:Rect = None
        self.leftpressed = False

        self.image_data = None
        self.mask_alpha = 0.8
        self.click_points = []
        self.click_points_mode = []

        self.guide_line_x:QtWidgets.QGraphicsLineItem = None
        self.guide_line_y:QtWidgets.QGraphicsLineItem = None

    def change_draw_to_create(self):
        self.mode = Mode.CREATE
        self.leftpressed = False
        if self.pixmap_item is not None:
            self.pixmap_item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
            self.mainwindow.actionCache.setEnabled(True)

    def change_draw_to_edit(self):
        self.mode = Mode.EDIT
        self.leftpressed = False
        if self.pixmap_item is not None:
            self.pixmap_item.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))

    def change_draw_to_view(self):
        self.mode = Mode.VIEW
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

    def load_image(self, file_path):
        self.clear()
        if self.mainwindow.use_segment_anything:
            self.mainwindow.segany.reset_image()
        self.image_data = np.array(Image.open(file_path))
        print('load img :', self.image_data.shape)
        if self.mainwindow.use_segment_anything:
            if self.image_data.ndim == 3 and self.image_data.shape[-1] == 3:  # 三通道图
                self.mainwindow.segany.set_image(self.image_data)
            elif self.image_data.ndim == 2:  # 单通道图
                self.image_data = self.image_data[:, :, np.newaxis]
                self.image_data = np.repeat(self.image_data, 3, axis=2)  # 转换为三通道
                self.mainwindow.segany.set_image(self.image_data)
            else:
                self.mainwindow.statusbar.showMessage(
                    "Segment anything don't support the image with shape {} .".format(self.image_data.shape))

        self.image_item = QtWidgets.QGraphicsPixmapItem()
        self.image_item.setZValue(0)
        self.addItem(self.image_item)
        self.mask_item = QtWidgets.QGraphicsPixmapItem()
        self.mask_item.setZValue(1)
        self.addItem(self.mask_item)

        pixmap = (QtGui.QPixmap(file_path))
        self.load_pixmap(pixmap)

    def load_pixmap(self, pixmap):

        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.pixmap_item.setZValue(0)
        self.pixmap_item.setPixmap(pixmap)
        self.addItem(self.pixmap_item)
        self.setSceneRect(self.pixmap_item.boundingRect())
        self.change_draw_to_view()

    def start_rect(self):
        self.draw_mode = DRAWMODE.RECTANGLE
        self.start_draw()

    def start_segment_any(self):
        self.draw_mode:DRAWMODE = DRAWMODE.SEGMENTANYTHING
        self.mainwindow.actionFinish_draw.setEnabled(True)
        self.start_draw()

    def start_draw(self):
        if self.mode != Mode.VIEW:
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
        self.current_rect.complete(category, color, difficult)
        self.rects.append(self.current_rect)
        self.mainwindow.dock_labels_add_label(self.current_rect)
        self.current_rect = None
        self.mainwindow.set_changed(True)
        self.mainwindow.label_visiable_checkbox_click(True)

        self.mainwindow.actionFinish_draw.setEnabled(False)

        # mask清空
        self.click_points.clear()
        self.click_points_mode.clear()
        self.update_mask()

        self.change_draw_to_view()

    def cache_draw(self):
        if self.current_rect is not None:
            self.removeItem(self.current_rect)
            self.current_rect:Rect = None
        self.mainwindow.label_visiable_checkbox_click(True)

        # mask清空
        self.click_points.clear()
        self.click_points_mode.clear()
        self.update_mask()

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
        print('mode:', self.mode)
        print('draw_mode:', self.draw_mode)
        if self.mode == Mode.CREATE:
            if self.draw_mode == DRAWMODE.RECTANGLE:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
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
            elif self.draw_mode == DRAWMODE.SEGMENTANYTHING:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    self.click_points.append([pos.x(), pos.y()])
                    self.click_points_mode.append(1)
                elif event.button() == QtCore.Qt.MouseButton.RightButton:
                    self.click_points.append([pos.x(), pos.y()])
                    self.click_points_mode.append(0)

                self.update_mask()

        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        # 限制范围
        pos = event.scenePos()
        if pos.x() < 0: pos.setX(0)
        if pos.x() > self.width(): pos.setX(self.width())
        if pos.y() < 0: pos.setY(0)
        if pos.y() > self.height(): pos.setY(self.height())

        if self.mode == Mode.CREATE and self.draw_mode == DRAWMODE.RECTANGLE:
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

    def update_mask(self):
        if not self.mainwindow.use_segment_anything:
            return
        if self.image_data is None:
            return
        if not (self.image_data.ndim == 3 and self.image_data.shape[-1] == 3):
            return
        if len(self.click_points) > 0 and len(self.click_points_mode) > 0:
            masks = self.mainwindow.segany.predict_with_point_prompt(self.click_points, self.click_points_mode)
            self.masks = masks
            color = np.array([0, 0, 255])
            h, w = masks.shape[-2:]

            l, t, r ,b = None, None, None, None
            for i in range(h):
                if t is None and np.any(masks[:, i, :]):
                    t = i

            for i in range(h-1, -1, -1):
                if b is None and np.any(masks[:, i, :]):
                    b = i

            for i in range(w):
                if l is None and np.any(masks[:, :, i]):
                    l = i

            for i in range(w-1, -1, -1):
                if r is None and np.any(masks[:, :, i]):
                    r = i
            self.current_rect.points.clear()
            self.current_rect.addPoint(QtCore.QPointF(l, t))
            self.current_rect.addPoint(QtCore.QPointF(r, b))
            self.current_rect.redraw()

            mask_image = masks.reshape(h, w, 1) * color.reshape(1, 1, -1)
            mask_image = mask_image.astype("uint8")
            mask_image = cv2.cvtColor(mask_image, cv2.COLOR_BGR2RGB)
            # 这里通过调整原始图像的权重self.mask_alpha，来调整mask的明显程度。
            mask_image = cv2.addWeighted(self.image_data, self.mask_alpha, mask_image, 1, 0)
            mask_image = QtGui.QImage(mask_image[:], mask_image.shape[1], mask_image.shape[0], mask_image.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)
            mask_pixmap = QtGui.QPixmap(mask_image)
            self.mask_item.setPixmap(mask_pixmap)


        else:
            mask_image = np.zeros(self.image_data.shape, dtype=np.uint8)
            mask_image = cv2.addWeighted(self.image_data, 1, mask_image, 0, 0)
            mask_image = QtGui.QImage(mask_image[:], mask_image.shape[1], mask_image.shape[0], mask_image.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)
            mask_pixmap = QtGui.QPixmap(mask_image)
            self.mask_item.setPixmap(mask_pixmap)



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
