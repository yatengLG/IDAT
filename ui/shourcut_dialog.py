# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/super/PycharmProjects/IDAT/ui/shourcut_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Shortcut(object):
    def setupUi(self, Dialog_Shortcut):
        Dialog_Shortcut.setObjectName("Dialog_Shortcut")
        Dialog_Shortcut.resize(550, 250)
        Dialog_Shortcut.setMinimumSize(QtCore.QSize(550, 250))
        Dialog_Shortcut.setMaximumSize(QtCore.QSize(550, 250))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_Shortcut)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog_Shortcut)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.widget_3.setFont(font)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout.setContentsMargins(18, -1, 18, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        self.label_5.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.widget_3)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 0, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.widget_3)
        self.label_19.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 0, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget_3)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 0, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget_3)
        self.label_16.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.widget_3)
        self.label_11.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 2, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.widget_3)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_3)
        self.label_8.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget_3)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget_3)
        self.label_13.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 3, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget_3)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 4, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget_3)
        self.label_15.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(133, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Dialog_Shortcut)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Shortcut)

    def retranslateUi(self, Dialog_Shortcut):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Shortcut.setWindowTitle(_translate("Dialog_Shortcut", "Shortcut"))
        self.label.setText(_translate("Dialog_Shortcut", "Shortcut"))
        self.label_5.setText(_translate("Dialog_Shortcut", "Esc"))
        self.label_18.setText(_translate("Dialog_Shortcut", "Prior image"))
        self.label_19.setText(_translate("Dialog_Shortcut", "A"))
        self.label_17.setText(_translate("Dialog_Shortcut", "Next image"))
        self.label_16.setText(_translate("Dialog_Shortcut", "D"))
        self.label_4.setText(_translate("Dialog_Shortcut", "Cache create"))
        self.label_2.setText(_translate("Dialog_Shortcut", "Segment anything"))
        self.label_10.setText(_translate("Dialog_Shortcut", "Create rect"))
        self.label_11.setText(_translate("Dialog_Shortcut", "C"))
        self.label_20.setText(_translate("Dialog_Shortcut", "Finish Draw"))
        self.label_8.setText(_translate("Dialog_Shortcut", "E"))
        self.label_7.setText(_translate("Dialog_Shortcut", "Delete rect"))
        self.label_6.setText(_translate("Dialog_Shortcut", "Del"))
        self.label_12.setText(_translate("Dialog_Shortcut", "Save annotation"))
        self.label_13.setText(_translate("Dialog_Shortcut", "S"))
        self.label_14.setText(_translate("Dialog_Shortcut", "Zoom fit"))
        self.label_15.setText(_translate("Dialog_Shortcut", "F"))
        self.label_3.setText(_translate("Dialog_Shortcut", "Q"))
import icon_rc
