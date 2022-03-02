# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_name.ui',
# licensing of 'widget_name.ui' applies.
#
# Created: Wed Mar  2 18:17:17 2022
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NameWidget(object):
    def setupUi(self, NameWidget):
        NameWidget.setObjectName("NameWidget")
        NameWidget.resize(337, 49)
        self.gridLayout = QtWidgets.QGridLayout(NameWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label2 = QtWidgets.QLabel(NameWidget)
        self.label2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label2.setObjectName("label2")
        self.gridLayout.addWidget(self.label2, 2, 2, 1, 1)
        self.cbVisible = QtWidgets.QCheckBox(NameWidget)
        self.cbVisible.setObjectName("cbVisible")
        self.gridLayout.addWidget(self.cbVisible, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(NameWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lbColor = QtWidgets.QLabel(NameWidget)
        self.lbColor.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.lbColor.setObjectName("lbColor")
        self.gridLayout.addWidget(self.lbColor, 2, 3, 1, 1)
        self.tbName = QtWidgets.QLineEdit(NameWidget)
        self.tbName.setObjectName("tbName")
        self.gridLayout.addWidget(self.tbName, 0, 1, 1, 3)

        self.retranslateUi(NameWidget)
        QtCore.QMetaObject.connectSlotsByName(NameWidget)

    def retranslateUi(self, NameWidget):
        NameWidget.setWindowTitle(QtWidgets.QApplication.translate("NameWidget", "Form", None, -1))
        self.label2.setText(QtWidgets.QApplication.translate("NameWidget", "Color:", None, -1))
        self.cbVisible.setText(QtWidgets.QApplication.translate("NameWidget", "Visual visible", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("NameWidget", "Name [unique]", None, -1))
        self.lbColor.setText(QtWidgets.QApplication.translate("NameWidget", "default", None, -1))

