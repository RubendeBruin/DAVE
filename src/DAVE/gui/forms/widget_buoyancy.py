# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_buoyancy.ui',
# licensing of 'widget_buoyancy.ui' applies.
#
# Created: Sat Jul  4 14:51:56 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(501, 467)
        Form.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.sbDenstiy = QtWidgets.QDoubleSpinBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbDenstiy.sizePolicy().hasHeightForWidth())
        self.sbDenstiy.setSizePolicy(sizePolicy)
        self.sbDenstiy.setDecimals(3)
        self.sbDenstiy.setMinimum(-999999999999.0)
        self.sbDenstiy.setMaximum(99999999999999.0)
        self.sbDenstiy.setObjectName("sbDenstiy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sbDenstiy)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Water density</span></p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Water density [mT/m3]", None, -1))

