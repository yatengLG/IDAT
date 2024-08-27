# -*- coding: utf-8 -*-
# @Author  : LG

from IDAT.ui.main_window import Ui_MainWindow
from IDAT.ui.choice_label_dialog import Ui_Dialog_Choice_Label
from IDAT.ui.add_annotation_dialog import Ui_dialog_add_annotation
from IDAT.ui.setting_dialog import Ui_Dialog_Setting
from IDAT.ui.shourcut_dialog import Ui_Dialog_Shortcut
from IDAT.ui.about_dialog import Ui_Dialog_About
from IDAT.canvas import Scene, View
from PyQt5 import QtCore, QtWidgets, QtGui
from IDAT.utils.file_ops import CATEGORYTUPLE, save_config, load_config
from IDAT.anno import Annotations, Annotation
from IDAT.rect import Rect
import imgviz
from xml.etree import ElementTree as ET
import sys
import os
from IDAT import icon_rc

cmap = imgviz.label_colormap()
IDAT_ROOT = os.path.split(os.path.abspath(__file__))[0]

class SettingDialog(QtWidgets.QDialog, Ui_Dialog_Setting):
    def __init__(self, parent, mainwindow):
        super(SettingDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.mainwindow = mainwindow
        self.label_tuple:list = []
        self.config_file:str = None
        self.connect()

    def init(self):
        label_tuples = self.mainwindow.category_tuples
        if label_tuples is None:
            return
        self.listWidget_labels.clear()
        self.lineEdit_label.clear()
        for label_tuple in label_tuples:
            category = label_tuple.category
            color = label_tuple.color
            item, widget = self.item_widget_generate(category, color)
            self.listWidget_labels.addItem(item)
            self.listWidget_labels.setItemWidget(item, widget)

    def button_choice_color(self):
        button = self.sender()
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet('QWidget {background-color: %s}' % (color.name()))

    def delete_category_item(self):
        button = self.sender()
        row = self.listWidget_labels.indexAt(button.parent().pos()).row()
        self.listWidget_labels.takeItem(row)
        if row <= len(self.mainwindow.category_tuples)-1:
            self.mainwindow.category_tuples.pop(row)

    def item_widget_generate(self, category, color):
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(200, 50))
        widget = QtWidgets.QWidget()

        layout = QtWidgets.QHBoxLayout()
        label_category = QtWidgets.QLabel()
        label_category.setText(category)
        label_category.setObjectName('category')

        button_color = QtWidgets.QPushButton()
        button_color.setStyleSheet('QWidget {background-color: %s}' % color)
        button_color.setFixedWidth(50)
        button_color.clicked.connect(self.button_choice_color)
        button_color.setObjectName('color')

        button_delete = QtWidgets.QPushButton()
        button_delete.setText('delete')
        button_delete.setFixedWidth(80)
        button_delete.clicked.connect(self.delete_category_item)
        button_delete.setObjectName('delete')

        layout.addWidget(label_category)
        layout.addWidget(button_color)
        layout.addWidget(button_delete)
        widget.setLayout(layout)
        return item, widget

    def load_cfg(self, file=None):
        if file is not None:
            # label_tuples = read_category_cfg(file)
            label_tuples = load_config(file)
            self.config_file = file

            self.mainwindow.actionSetting.setStatusTip(
                QtCore.QCoreApplication.translate("MainWindow", "Current config file: {}".format(self.config_file)))

        else:
            label_tuples = self.mainwindow.category_tuples
        if label_tuples is None:
            return
        self.listWidget_labels.clear()
        for label_tuple in label_tuples:
            category = label_tuple.category
            color = label_tuple.color
            item, widget = self.item_widget_generate(category, color)
            self.listWidget_labels.addItem(item)
            self.listWidget_labels.setItemWidget(item, widget)
        self.mainwindow.category_tuples = label_tuples
        return True

    def save_cfg(self, file):
        # save_category_cfg(self.mainwindow.category_tuples, file)
        save_config(self.mainwindow.category_tuples, file)
        return True

    def add(self):
        category = self.lineEdit_label.text()
        color = self.pushButton_color.palette().button().color().name()
        if category == '':
            QtWidgets.QMessageBox.warning(self, 'Warning', 'The category is empty.')
            return

        item, widget = self.item_widget_generate(category, color)
        self.listWidget_labels.addItem(item)
        self.listWidget_labels.setItemWidget(item, widget)

    def apply(self):
        self.mainwindow.category_tuples = []
        for index in range(self.listWidget_labels.count()):
            item = self.listWidget_labels.item(index)
            widget = self.listWidget_labels.itemWidget(item)
            label_category = widget.findChild(QtWidgets.QLabel, 'category')
            button_color = widget.findChild(QtWidgets.QPushButton, 'color')
            category = label_category.text()
            color = button_color.palette().button().color().name()
            self.mainwindow.category_tuples.append(CATEGORYTUPLE(category, color))
        if self.config_file is not None:
            self.save_cfg(self.config_file)
        self.mainwindow.load_category()

        r = QtWidgets.QMessageBox.information(self, 'Setting apply', 'OK!')
        if r:
            self.close()

    def cache(self):
        self.lineEdit_label.clear()
        self.pushButton_color.setStyleSheet('QWidget {background-color: #8ae234}')
        self.close()

    def export_cfg(self):
        file, suffix = QtWidgets.QFileDialog.getSaveFileName(self, caption='Save file path', filter=".yaml (*.yaml)")
        if file:
            if not file.endswith('.yaml'):
                file += '.yaml'
            if file:
                self.save_cfg(file)

    def import_cfg(self):
        file, suffix = QtWidgets.QFileDialog.getOpenFileName(self, caption='file path', filter=".yaml (*.yaml)")
        if file:
            self.load_cfg(file)

    def connect(self):
        self.pushButton_add.clicked.connect(self.add)
        self.pushButton_color.clicked.connect(self.button_choice_color)
        self.pushButton_cache.clicked.connect(self.cache)
        self.pushButton_apply.clicked.connect(self.apply)
        self.pushButton_import.clicked.connect(self.import_cfg)
        self.pushButton_export.clicked.connect(self.export_cfg)

class ShortcutDialog(QtWidgets.QDialog, Ui_Dialog_Shortcut):
    def __init__(self, parent):
        super(ShortcutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

class AboutDialog(QtWidgets.QDialog, Ui_Dialog_About):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

class ChoiceLabelDialog(QtWidgets.QDialog, Ui_Dialog_Choice_Label):
    def __init__(self, parent, mainwindow):
        super(ChoiceLabelDialog, self).__init__(parent)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

        self.current_category_tuple:CATEGORYTUPLE = None
        self.connect()

    def init(self):
        self.current_category_tuple = None
        self.lineEdit_category.clear()
        self.lineEdit_category.setStyleSheet('QWidget {background-color: #FFFFFF}')
        self.checkBox_difficult.setChecked(False)
        self.listWidget_category.clear()

        for category_tuple in self.mainwindow.category_tuples:
            category = category_tuple.category
            color = category_tuple.color
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 30))

            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(9, 1, 9, 1)

            label_category = QtWidgets.QLabel()
            label_category.setText(category)

            label_color = QtWidgets.QLabel()
            label_color.setFixedWidth(10)
            label_color.setStyleSheet("background-color: {};".format(color))

            layout.addWidget(label_color)
            layout.addWidget(label_category)
            widget.setLayout(layout)

            self.listWidget_category.addItem(item)
            self.listWidget_category.setItemWidget(item, widget)

    def choice_category(self):
        current_row = self.listWidget_category.currentRow()
        category_tuple = self.mainwindow.category_tuples[current_row]
        self.lineEdit_category.setText(category_tuple.category)
        self.lineEdit_category.setStyleSheet("border-width: 2px;border-style: solid; border-color: %s;" % category_tuple.color)
        self.current_category_tuple = category_tuple

    def apply(self):
        if self.current_category_tuple is None:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'No category selected.')
            return
        category = self.current_category_tuple.category
        color = self.current_category_tuple.color
        difficult = self.checkBox_difficult.checkState()
        self.mainwindow.scene.current_rect.complete(category, color, difficult)
        self.mainwindow.scene.rects.append(self.mainwindow.scene.current_rect)
        self.mainwindow.dock_labels_add_label(self.mainwindow.scene.current_rect)
        self.mainwindow.scene.current_rect = None
        self.mainwindow.set_changed(True)
        self.close()

    def cache(self):
        self.mainwindow.scene.cache_draw()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.cache()

    def reject(self):
        self.cache()

    def connect(self):
        self.pushButton_apply.clicked.connect(self.apply)
        self.pushButton_cache.clicked.connect(self.cache)
        self.listWidget_category.itemClicked.connect(self.choice_category)

class EditLabelDialog(QtWidgets.QDialog, Ui_Dialog_Choice_Label):
    def __init__(self, parent, mainwindow):
        super(EditLabelDialog, self).__init__(parent)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.rect:Rect =  None
        self.connect()

    def init(self, rect:Rect):
        self.rect = rect
        self.rect.is_completed = False
        self.current_category_tuple = None
        self.lineEdit_category.setText(rect.category)
        self.lineEdit_category.setStyleSheet("border-width: 2px;border-style: solid; border-color: %s;" % rect.color.name())

        self.checkBox_difficult.setChecked(rect.is_difficult)
        self.listWidget_category.clear()

        for category_tuple in self.mainwindow.category_tuples:
            category = category_tuple.category
            color = category_tuple.color
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 30))

            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(9, 1, 9, 1)

            label_category = QtWidgets.QLabel()
            label_category.setText(category)

            label_color = QtWidgets.QLabel()
            label_color.setFixedWidth(10)
            label_color.setStyleSheet("background-color: {};".format(color))

            layout.addWidget(label_color)
            layout.addWidget(label_category)
            widget.setLayout(layout)

            # item.setText(category)
            self.listWidget_category.addItem(item)
            self.listWidget_category.setItemWidget(item, widget)
            if category == rect.category and color == rect.color.name():
                self.current_category_tuple = category_tuple

    def choice_category(self):
        current_row = self.listWidget_category.currentRow()
        category_tuple = self.mainwindow.category_tuples[current_row]
        self.lineEdit_category.setText(category_tuple.category)
        self.lineEdit_category.setStyleSheet("border-width: 2px;border-style: solid; border-color: %s;" % category_tuple.color)
        self.current_category_tuple = category_tuple

    def apply(self):
        if self.rect is None:
            return
        if self.current_category_tuple is None:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'No category selected.')
            return
        category = self.current_category_tuple.category
        color = self.current_category_tuple.color
        difficult = bool(self.checkBox_difficult.checkState())

        if category != self.rect.category or difficult != self.rect.is_difficult:
            self.mainwindow.set_changed(True)

        self.rect.category = category
        self.rect.is_difficult = difficult
        self.rect.color = QtGui.QColor(color)
        self.rect.setPen(QtGui.QPen(self.rect.color, 1, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap))
        self.rect.color.setAlpha(self.rect.nohover_alpha)
        self.rect.setBrush(self.rect.color)
        self.rect.redraw()
        self.rect.is_completed = True
        self.rect = None
        self.mainwindow.dock_labels_updata()
        self.mainwindow.scene.change_draw_to_view()
        self.close()

    def cache(self):
        if self.rect is not None:
            self.rect.is_completed = True
            self.rect = None
        self.mainwindow.scene.change_draw_to_view()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.cache()

    def reject(self):
        self.cache()

    def connect(self):
        self.pushButton_apply.clicked.connect(self.apply)
        self.pushButton_cache.clicked.connect(self.cache)
        self.listWidget_category.itemClicked.connect(self.choice_category)

class AddAnnotDialog(QtWidgets.QDialog, Ui_dialog_add_annotation):
    def __init__(self, parent, mainwindow):
        super(AddAnnotDialog, self).__init__(parent)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.listWidget_category.itemClicked.connect(self.choice_category)
        self.pushButton_apply.clicked.connect(self.apply)
        # self.pushButton_apply.setShortcut('Enter')
        self.pushButton_cache.clicked.connect(self.cache)
        # self.pushButton_cache.setShortcut('Esc')

    def init(self):
        self.lineEdit_category.clear()
        self.lineEdit_category.setStyleSheet('QWidget {background-color: #FFFFFF}')
        self.current_category_tuple = None
        self.lineEdit_xmin.clear()
        self.lineEdit_ymin.clear()
        self.lineEdit_xmax.clear()
        self.lineEdit_ymax.clear()
        self.checkBox_difficult.setChecked(False)
        self.listWidget_category.clear()

        for category_tuple in self.mainwindow.category_tuples:
            category = category_tuple.category
            color = category_tuple.color
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 30))

            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(9, 1, 9, 1)

            label_category = QtWidgets.QLabel()
            label_category.setText(category)

            label_color = QtWidgets.QLabel()
            label_color.setFixedWidth(10)
            label_color.setStyleSheet("background-color: {};".format(color))

            layout.addWidget(label_color)
            layout.addWidget(label_category)
            widget.setLayout(layout)

            self.listWidget_category.addItem(item)
            self.listWidget_category.setItemWidget(item, widget)

    def choice_category(self):
        current_row = self.listWidget_category.currentRow()
        category_tuple = self.mainwindow.category_tuples[current_row]
        self.lineEdit_category.setText(category_tuple.category)
        self.lineEdit_category.setStyleSheet("border-width: 2px;border-style: solid; border-color: %s;" % category_tuple.color)
        self.current_category_tuple = category_tuple

    def apply(self):
        try:
            if self.current_category_tuple is None:
                QtWidgets.QMessageBox.warning(self.mainwindow, 'Warning', 'No category selected!')
                return
            xmin = int(self.lineEdit_xmin.text())
            ymin = int(self.lineEdit_ymin.text())
            xmax = int(self.lineEdit_xmax.text())
            ymax = int(self.lineEdit_ymax.text())
            is_difficult = self.checkBox_difficult.isChecked()
            category = self.current_category_tuple.category
            color = self.current_category_tuple.color

            # 添加矩形
            rect = Rect()
            self.mainwindow.scene.addItem(rect)
            rect.create_from_xyxy(category, xmin, ymin, xmax, ymax, is_difficult, color)
            self.mainwindow.scene.rects.append(rect)
            self.mainwindow.dock_labels_add_label(rect)
            self.mainwindow.set_changed(True)
            self.close()

        except:
            QtWidgets.QMessageBox.warning(self.mainwindow, 'Warning', 'Data error!')
            return

    def cache(self):
        self.close()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.scene = Scene(self)
        self.view = View(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.labelCoordinates = QtWidgets.QLabel('')
        self.status_bar.addPermanentWidget(self.labelCoordinates)
        self.setting_dialog = SettingDialog(self, self)
        self.shortcut_dialog = ShortcutDialog(self)
        self.about_dialog = AboutDialog(self)
        self.choice_label_dialog = ChoiceLabelDialog(self, self)
        self.edit_label_dialog = EditLabelDialog(self, self)
        self.add_annotation_dialog = AddAnnotDialog(self, self)

        self.files_root = None
        self.labels_root = None
        self.files_list = []
        self.current_index = 0
        self.pixmap:QtGui.QPixmap = None
        self.xml_path:str = None
        self.category_tuples = []
        self.is_changed = False

        self.trans = QtCore.QTranslator()

        self.init_gui()
        self.connect()

        # 默认类别配置
        default_yaml_path = os.path.join(IDAT_ROOT, 'default.yaml')
        if os.path.exists(default_yaml_path):
            self.setting_dialog.load_cfg(default_yaml_path)

        self.load_category()

    def init_gui(self):
        self.setWindowTitle('IDAT')
        self.actionPrior_image.setEnabled(False)
        self.actionNext_image.setEnabled(False)
        self.actionCreate.setEnabled(False)
        self.actionCache.setEnabled(False)
        self.actionEdit.setEnabled(False)
        self.actionDelete.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionZoom_in.setEnabled(False)
        self.actionZoom_out.setEnabled(False)
        self.actionFit_window.setEnabled(False)

    def translate(self, language='zh'):
        if language == 'zh':
            self.trans.load(os.path.join(IDAT_ROOT, 'ui/zh_CN'))
        else:
            self.trans.load(os.path.join(IDAT_ROOT, 'ui/en'))
        self.actionChinese.setChecked(language=='zh')
        self.actionEnglish.setChecked(language=='en')
        _app = QtWidgets.QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        self.about_dialog.retranslateUi(self.about_dialog)
        self.add_annotation_dialog.retranslateUi(self.add_annotation_dialog)
        self.choice_label_dialog.retranslateUi(self.choice_label_dialog)
        self.setting_dialog.retranslateUi(self.setting_dialog)
        self.shortcut_dialog.retranslateUi(self.shortcut_dialog)
        self.edit_label_dialog.retranslateUi(self.edit_label_dialog)

    def translate_to_chinese(self):
        self.translate('zh')

    def translate_to_english(self):
        self.translate('en')

    def load_category(self):
        self.listWidget_categories.clear()
        label_tuples = self.category_tuples
        if label_tuples is None:
            return

        for label_tuple in label_tuples:
            category = label_tuple.category
            color = label_tuple.color

            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(200, 40))
            widget = QtWidgets.QWidget()

            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(9, 1, 9, 1)

            label_category = QtWidgets.QLabel()
            label_category.setText(category)
            label_category.setObjectName('category')

            button_color = QtWidgets.QLabel()
            button_color.setStyleSheet('QWidget {background-color: %s}' % color)
            button_color.setFixedWidth(5)

            label_color = QtWidgets.QLabel()
            label_color.setText(color)
            label_color.setVisible(False)
            label_color.setObjectName('color')

            layout.addWidget(label_color)
            layout.addWidget(button_color)
            layout.addWidget(label_category)
            widget.setLayout(layout)

            self.listWidget_categories.addItem(item)
            self.listWidget_categories.setItemWidget(item, widget)
        if len(label_tuples) > 0:
            self.listWidget_categories.setCurrentRow(0)

    def open_image_dir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Open image directory')
        if not dir:
            return
        suffixs = ('jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'ppm', 'PPM')
        files_list = [f for f in os.listdir(dir) if f.endswith(suffixs)]
        if len(files_list) < 1:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'No pictures found!\nOnly pictures suffix as [{}] are supported!'.format(suffixs))
            return
        files_list.sort()
        self.files_list = files_list

        self.files_root = dir
        self.actionOpen_image_dir.setStatusTip(
            QtCore.QCoreApplication.translate("MainWindow", "Current image directory: {}".format(self.files_root)))

        self.labels_root = dir
        self.actionOpen_label_dir.setStatusTip(
            QtCore.QCoreApplication.translate("MainWindow", "Current label directory: {}".format(self.labels_root)))

        self.load_category_yaml_from_label_root()

        self.current_index = 0
        self.show_image(0)

        # update files dock
        self.listWidget_files.clear()
        for file_name in self.files_list:
            item = QtWidgets.QListWidgetItem()
            item.setText(file_name)
            self.listWidget_files.addItem(item)

    def open_label_dir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Open label directory')
        if dir:
            self.labels_root = dir
            self.actionOpen_label_dir.setStatusTip(
                QtCore.QCoreApplication.translate("MainWindow", "Current label directory: {}".format(self.labels_root)))

            self.load_category_yaml_from_label_root()

        if self.files_list:
            self.show_image()

    def load_category_yaml_from_label_root(self):
        category_yaml = os.path.join(self.labels_root, 'category.yaml')
        if os.path.exists(category_yaml):
            self.setting_dialog.load_cfg(category_yaml)
            self.load_category()
        else:
            object_names = self.get_object_name_from_xml(self.labels_root)
            category_list = []
            if len(object_names) > 0:
                for index, object_name in enumerate(object_names):
                    r, g, b = cmap[index+1]
                    category_list.append(CATEGORYTUPLE(object_name, QtGui.QColor(r, g, b).name()))
                save_config(category_list, file=category_yaml)
                self.setting_dialog.load_cfg(category_yaml)
                self.load_category()

    def get_object_name_from_xml(self, xml_root):
        object_name_set = set()
        for xml in os.listdir(xml_root):
            try:
                xml_path = os.path.join(xml_root, xml)
                root = ET.parse(xml_path).getroot()
                objects = root.findall('object')
                for object in objects:
                    name = object.find('name').text
                    object_name_set.add(name)
            except: pass
        object_name_set = list(object_name_set)
        object_name_set.sort()
        return object_name_set

    def show_image(self, index:int=None):
        self.scene.clear()
        self.scene.rects.clear()
        self.set_changed(False)
        self.checkBox_visiable.setChecked(True)
        self.listWidget_labels.clear()

        if len(self.files_list) == 0:
            return

        if index is not None and 0 <= index <= len(self.files_list)-1:
            self.current_index = index
        self.actionPrior_image.setEnabled(self.current_index != 0)
        self.actionNext_image.setEnabled(self.current_index != len(self.files_list) - 1)

        pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(os.path.join(self.files_root, self.files_list[self.current_index])))
        self.pixmap = pixmap
        self.scene.load_pixmap(pixmap)

        # update files dock
        self.listWidget_files.setCurrentRow(self.current_index)
        self.label_files.setText("{}/{}".format(self.current_index+1, len(self.files_list)))
        self.view.zoom_fit()

        filename = '.'.join(self.files_list[self.current_index].split('.')[:-1])
        self.xml_path = os.path.join(self.labels_root, filename + '.xml')

        self.load_anno()
        #
        self.actionCreate.setEnabled(True)
        self.actionZoom_in.setEnabled(True)
        self.actionZoom_out.setEnabled(True)
        self.actionFit_window.setEnabled(True)

    def load_anno(self):
        if not self.files_list:
            return

        if os.path.exists(self.xml_path):
            annos = Annotations()
            annos.load_annotation_from_xml(self.xml_path)

            for anno in annos.annotations:
                rect = Rect()
                self.scene.addItem(rect)
                color = '#6D6D6D'
                for cate, colo in self.category_tuples:
                    if cate == anno.category:
                        color = colo
                        break
                rect.create_from_xyxy(anno.category, anno.xmin, anno.ymin, anno.xmax, anno.ymax, anno.is_difficult, color)
                self.scene.rects.append(rect)
                self.dock_labels_add_label(rect)

    def prior_image(self):
        if self.current_index <= 0:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'It`s the first one.',
                                          buttons=QtWidgets.QMessageBox.StandardButton.Yes)
            return
        if self.is_changed:
            button = QtWidgets.QMessageBox.warning(self, 'Warning', 'Unsaved! Are you sure want to continue?', buttons=QtWidgets.QMessageBox.StandardButton.Yes|QtWidgets.QMessageBox.StandardButton.No)
            if button == QtWidgets.QMessageBox.StandardButton.No:
                return
        self.current_index -= 1
        self.show_image()

    def next_image(self):
        if self.current_index >= len(self.files_list)-1:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'It`s the last one.', buttons=QtWidgets.QMessageBox.StandardButton.Yes)
            return
        if self.is_changed:
            button = QtWidgets.QMessageBox.warning(self, 'Warning', 'Unsaved! Are you sure want to continue?', buttons=QtWidgets.QMessageBox.StandardButton.Yes|QtWidgets.QMessageBox.StandardButton.No)
            if button == QtWidgets.QMessageBox.StandardButton.No:
                return
        self.current_index += 1
        self.show_image()

    def jump_to(self):
        index = self.lineEdit_jump.text()
        if index:
            if not index.isdigit():
                if index in self.files_list:
                    index = self.files_list.index(index)+1
                else:
                    QtWidgets.QMessageBox.warning(self, 'Warning', 'Don`t exist image named: {}'.format(index))
                    self.lineEdit_jump.clear()
                    return
            index = int(index)-1
            if 0 <= index < len(self.files_list):
                self.show_image(index)
                self.lineEdit_jump.clear()
            else:
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Index must be in [1, {}].'.format(len(self.files_list)))
                self.lineEdit_jump.clear()
                self.lineEdit_jump.clearFocus()
                return

    def dock_files_click(self):
        row = self.listWidget_files.currentRow()
        self.show_image(row)

    def label_item_widget_generate(self, rect):
        category = rect.category
        color = rect.color.name()
        is_difficult = rect.is_difficult
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(200, 30))
        widget = QtWidgets.QWidget()

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(9, 1, 9, 1)
        label_category = QtWidgets.QLabel()
        label_category.setText(category)

        button_checkbox = QtWidgets.QCheckBox()
        button_checkbox.setFixedWidth(20)
        button_checkbox.setChecked(rect.isVisible())
        button_checkbox.clicked.connect(rect.set_visible)
        button_checkbox.setObjectName('checkbox')

        label_color = QtWidgets.QLabel()
        label_color.setFixedWidth(10)
        label_color.setStyleSheet("background-color: {};".format(color))

        label_difficult =  QtWidgets.QLabel()
        label_difficult.setFixedWidth(3)
        if is_difficult:
            label_difficult.setStyleSheet("background-color: {};".format('#000000'))

        layout.addWidget(button_checkbox)
        layout.addWidget(label_color)
        layout.addWidget(label_category)
        layout.addWidget(label_difficult, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        widget.setLayout(layout)
        return item, widget

    def dock_labels_add_label(self, rect):
        item, widget = self.label_item_widget_generate(rect)
        self.listWidget_labels.addItem(item)
        self.listWidget_labels.setItemWidget(item, widget)

    def dock_labels_select_change(self):
        items = self.listWidget_labels.selectedItems()
        rows = [self.listWidget_labels.row(item) for item in items]
        for index, rect in enumerate(self.scene.rects):
            if index in rows:
                if not rect.isSelected():
                    rect.setSelected(True)
                    self.status_bar.showMessage("({:.0f}, {:.0f}, {:.0f}, {:.0f})".format(rect.vertexs[0].pos().x(),
                                                                                          rect.vertexs[0].pos().y(),
                                                                                          rect.vertexs[3].pos().x(),
                                                                                          rect.vertexs[3].pos().y()),
                                                3000)
            else:
                if rect.isSelected():
                    rect.setSelected(False)
        #
        rects_select = [rect.isSelected() for rect in self.scene.rects]
        any_selected = any(rects_select)
        self.actionEdit.setEnabled(any_selected)
        self.actionDelete.setEnabled(any_selected)

    def dock_labels_double_click(self):
        self.scene.edit_rect()

    def dock_labels_updata(self):
        self.listWidget_labels.clear()
        for rect in self.scene.rects:
            self.dock_labels_add_label(rect)

    def dock_label_set_selected(self, rect):
        index = self.scene.rects.index(rect)
        item = self.listWidget_labels.item(index)
        if rect.isSelected():
            if not item.isSelected():
                item.setSelected(True)
        else:
            if item.isSelected():
                item.setSelected(False)

    def label_visiable_checkbox_click(self, check_state):
        for index, rect in enumerate(self.scene.rects):
            rect.set_visible(check_state)
            item = self.listWidget_labels.item(index)
            widget = self.listWidget_labels.itemWidget(item)
            checkbox = widget.findChild(QtWidgets.QCheckBox, 'checkbox')
            checkbox.setChecked(check_state)

    def add_annotation_manually(self):
        if self.pixmap is None:
            return
        self.add_annotation_dialog.init()
        self.add_annotation_dialog.show()

    def setting(self):
        self.setting_dialog.init()
        self.setting_dialog.show()

    def save(self):
        if self.files_list and self.pixmap:
            annos = Annotations()
            annos.width = self.pixmap.width()
            annos.height = self.pixmap.height()
            annos.depth = self.pixmap.depth()
            annos.image_path = os.path.join(self.files_root, self.files_list[self.current_index])
            for rect in self.scene.rects:
                points = [v.pos() for v in rect.vertexs]
                xs = [p.x() for p in points]
                ys = [p.y() for p in points]

                xmin, ymin, xmax, ymax = min(xs), min(ys), max(xs), max(ys)
                anno = Annotation(rect.category, xmin, ymin, xmax, ymax, rect.is_difficult)
                annos.annotations.append(anno)
            annos.save_annotation_to_xml(self.xml_path)
            self.status_bar.showMessage('Save to {}'.format(self.xml_path), 2000)
            self.set_changed(False)

    def set_changed(self, changed:bool):
        if changed:
            self.is_changed =True
            self.setWindowTitle('*{}'.format(os.path.join(self.files_root, self.files_list[self.current_index])))
            self.actionSave.setEnabled(True)
        else:
            self.is_changed = False
            self.setWindowTitle('{}'.format(os.path.join(self.files_root, self.files_list[self.current_index])))
            self.actionSave.setEnabled(False)

    def connect(self):
        self.actionOpen_image_dir.triggered.connect(self.open_image_dir)
        self.actionOpen_label_dir.triggered.connect(self.open_label_dir)
        self.actionPrior_image.triggered.connect(self.prior_image)
        self.actionNext_image.triggered.connect(self.next_image)
        self.actionCreate.triggered.connect(self.scene.start_draw)
        self.actionEdit.triggered.connect(self.scene.edit_rect)
        self.actionDelete.triggered.connect(self.scene.delete_rect)
        self.actionSave.triggered.connect(self.save)
        self.actionCache.triggered.connect(self.scene.cache_draw)
        self.actionZoom_in.triggered.connect(self.view.zoom_in)
        self.actionZoom_out.triggered.connect(self.view.zoom_out)
        self.actionFit_window.triggered.connect(self.view.zoom_fit)

        self.actionSetting.triggered.connect(self.setting)
        self.actionShortcut.triggered.connect(self.shortcut_dialog.show)
        self.actionAbout.triggered.connect(self.about_dialog.show)
        self.actionExit.triggered.connect(self.close)

        self.actionChinese.triggered.connect(self.translate_to_chinese)
        self.actionEnglish.triggered.connect(self.translate_to_english)

        self.listWidget_files.doubleClicked.connect(self.dock_files_click)
        self.lineEdit_jump.returnPressed.connect(self.jump_to)
        self.listWidget_labels.itemSelectionChanged.connect(self.dock_labels_select_change)
        self.listWidget_labels.doubleClicked.connect(self.dock_labels_double_click)
        self.checkBox_visiable.clicked.connect(self.label_visiable_checkbox_click)
        self.pushButton_add_manually.clicked.connect(self.add_annotation_manually)

def main():
    app = QtWidgets.QApplication([''])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

