# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_name.ui',
# licensing of 'widget_name.ui' applies.
#
# Created: Thu Jul  2 20:34:21 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NameWidget(object):
    def setupUi(self, NameWidget):
        NameWidget.setObjectName("NameWidget")
        NameWidget.resize(503, 83)
        self.formLayout = QtWidgets.QFormLayout(NameWidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(NameWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.tbName = QtWidgets.QLineEdit(NameWidget)
        self.tbName.setObjectName("tbName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tbName)
        self.cbVisible = QtWidgets.QCheckBox(NameWidget)
        self.cbVisible.setObjectName("cbVisible")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbVisible)

        self.retranslateUi(NameWidget)
        QtCore.QMetaObject.connectSlotsByName(NameWidget)

    def retranslateUi(self, NameWidget):
        NameWidget.setWindowTitle(QtWidgets.QApplication.translate("NameWidget", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("NameWidget", "Name [unique]", None, -1))
        self.cbVisible.setText(QtWidgets.QApplication.translate("NameWidget", "Visual visible", None, -1))

