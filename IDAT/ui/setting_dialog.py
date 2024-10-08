# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/super/PycharmProjects/IDAT/setting_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Setting(object):
    def setupUi(self, Dialog_Setting):
        Dialog_Setting.setObjectName("Dialog_Setting")
        Dialog_Setting.resize(558, 340)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        Dialog_Setting.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog_Setting)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_Setting)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget_labels = QtWidgets.QListWidget(Dialog_Setting)
        self.listWidget_labels.setObjectName("listWidget_labels")
        self.verticalLayout.addWidget(self.listWidget_labels)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_label = QtWidgets.QLineEdit(Dialog_Setting)
        self.lineEdit_label.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_label.setReadOnly(False)
        self.lineEdit_label.setObjectName("lineEdit_label")
        self.horizontalLayout.addWidget(self.lineEdit_label)
        self.pushButton_color = QtWidgets.QPushButton(Dialog_Setting)
        self.pushButton_color.setMinimumSize(QtCore.QSize(30, 0))
        self.pushButton_color.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_color.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.pushButton_color.setText("")
        self.pushButton_color.setObjectName("pushButton_color")
        self.horizontalLayout.addWidget(self.pushButton_color)
        self.pushButton_add = QtWidgets.QPushButton(Dialog_Setting)
        self.pushButton_add.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_add.setMaximumSize(QtCore.QSize(150, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/书签_bookmark-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_add.setIcon(icon)
        self.pushButton_add.setAutoDefault(True)
        self.pushButton_add.setDefault(False)
        self.pushButton_add.setFlat(False)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_import = QtWidgets.QPushButton(Dialog_Setting)
        self.pushButton_import.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_import.setMaximumSize(QtCore.QSize(80, 16777215))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/传入3_afferent-three.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_import.setIcon(icon1)
        self.pushButton_import.setObjectName("pushButton_import")
        self.horizontalLayout_2.addWidget(self.pushButton_import)
        self.pushButton_export = QtWidgets.QPushButton(Dialog_Setting)
        self.pushButton_export.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_export.setMaximumSize(QtCore.QSize(80, 16777215))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/传出3_efferent-three.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_export.setIcon(icon2)
        self.pushButton_export.setObjectName("pushButton_export")
        self.horizontalLayout_2.addWidget(self.pushButton_export)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_cache = QtWidgets.QPushButton(Dialog_Setting)
        self.pushButton_cache.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_cache.setMaximumSize(QtCore.QSize(80, 16777215))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/关闭_close-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_cache.setIcon(icon3)
        self.pushButton_cache.setObjectName("pushButton_cache")
        self.horizontalLayout_2.addWidget(self.pushButton_cache)
        self.pushButton_apply = QtWidgets.QPushButton(Dialog_Setting)
        self.pushButton_apply.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_apply.setMaximumSize(QtCore.QSize(80, 16777215))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/校验_check-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_apply.setIcon(icon4)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.horizontalLayout_2.addWidget(self.pushButton_apply)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog_Setting)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Setting)

    def retranslateUi(self, Dialog_Setting):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Setting.setWindowTitle(_translate("Dialog_Setting", "Setting"))
        self.label.setText(_translate("Dialog_Setting", "Labels"))
        self.pushButton_add.setText(_translate("Dialog_Setting", "Add New Label"))
        self.pushButton_import.setText(_translate("Dialog_Setting", "Import"))
        self.pushButton_export.setText(_translate("Dialog_Setting", "Export"))
        self.pushButton_cache.setText(_translate("Dialog_Setting", "Cache"))
        self.pushButton_apply.setText(_translate("Dialog_Setting", "Apply"))
