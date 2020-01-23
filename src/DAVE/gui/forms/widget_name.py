# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_name.ui',
# licensing of 'widget_name.ui' applies.
#
# Created: Thu Oct 31 16:19:27 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NameWidget(object):
    def setupUi(self, NameWidget):
        NameWidget.setObjectName("NameWidget")
        NameWidget.resize(503, 68)
        self.horizontalLayout = QtWidgets.QHBoxLayout(NameWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(NameWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.tbName = QtWidgets.QLineEdit(NameWidget)
        self.tbName.setObjectName("tbName")
        self.horizontalLayout.addWidget(self.tbName)

        self.retranslateUi(NameWidget)
        QtCore.QMetaObject.connectSlotsByName(NameWidget)

    def retranslateUi(self, NameWidget):
        NameWidget.setWindowTitle(QtWidgets.QApplication.translate("NameWidget", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("NameWidget", "Name [unique]", None, -1))

