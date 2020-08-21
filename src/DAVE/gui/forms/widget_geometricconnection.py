# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_geometricconnection.ui',
# licensing of 'widget_geometricconnection.ui' applies.
#
# Created: Fri Aug 21 15:25:52 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_GeometricConnection(object):
    def setupUi(self, GeometricConnection):
        GeometricConnection.setObjectName("GeometricConnection")
        GeometricConnection.resize(470, 687)
        GeometricConnection.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(GeometricConnection)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblInfo_3 = QtWidgets.QLabel(GeometricConnection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInfo_3.sizePolicy().hasHeightForWidth())
        self.lblInfo_3.setSizePolicy(sizePolicy)
        self.lblInfo_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblInfo_3.setAutoFillBackground(False)
        self.lblInfo_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblInfo_3.setObjectName("lblInfo_3")
        self.verticalLayout.addWidget(self.lblInfo_3)
        self.widget_2 = QtWidgets.QWidget(GeometricConnection)
        self.widget_2.setObjectName("widget_2")
        self.formLayout = QtWidgets.QFormLayout(self.widget_2)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lblParent = QtWidgets.QLabel(self.widget_2)
        self.lblParent.setStyleSheet("background: lightgray")
        self.lblParent.setObjectName("lblParent")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lblParent)
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lblChild = QtWidgets.QLabel(self.widget_2)
        self.lblChild.setStyleSheet("background: lightgray")
        self.lblChild.setObjectName("lblChild")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lblChild)
        self.verticalLayout.addWidget(self.widget_2)
        self.label_8 = QtWidgets.QLabel(GeometricConnection)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.lblInfo = QtWidgets.QLabel(GeometricConnection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInfo.sizePolicy().hasHeightForWidth())
        self.lblInfo.setSizePolicy(sizePolicy)
        self.lblInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblInfo.setAutoFillBackground(False)
        self.lblInfo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblInfo.setObjectName("lblInfo")
        self.verticalLayout.addWidget(self.lblInfo)
        self.rbPinHole = QtWidgets.QRadioButton(GeometricConnection)
        self.rbPinHole.setObjectName("rbPinHole")
        self.verticalLayout.addWidget(self.rbPinHole)
        self.rbPinPin = QtWidgets.QRadioButton(GeometricConnection)
        self.rbPinPin.setObjectName("rbPinPin")
        self.verticalLayout.addWidget(self.rbPinPin)
        self.lblInfo_2 = QtWidgets.QLabel(GeometricConnection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInfo_2.sizePolicy().hasHeightForWidth())
        self.lblInfo_2.setSizePolicy(sizePolicy)
        self.lblInfo_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblInfo_2.setAutoFillBackground(False)
        self.lblInfo_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblInfo_2.setObjectName("lblInfo_2")
        self.verticalLayout.addWidget(self.lblInfo_2)
        self.widget = QtWidgets.QWidget(GeometricConnection)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.cbSFix = QtWidgets.QCheckBox(self.widget)
        self.cbSFix.setObjectName("cbSFix")
        self.gridLayout.addWidget(self.cbSFix, 2, 1, 1, 1)
        self.pbChangeSide = QtWidgets.QPushButton(self.widget)
        self.pbChangeSide.setObjectName("pbChangeSide")
        self.gridLayout.addWidget(self.pbChangeSide, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.pbFlip = QtWidgets.QPushButton(self.widget)
        self.pbFlip.setObjectName("pbFlip")
        self.gridLayout.addWidget(self.pbFlip, 6, 2, 1, 1)
        self.sbMasterRotation = QtWidgets.QDoubleSpinBox(self.widget)
        self.sbMasterRotation.setMinimum(-360.0)
        self.sbMasterRotation.setMaximum(360.0)
        self.sbMasterRotation.setSingleStep(10.0)
        self.sbMasterRotation.setObjectName("sbMasterRotation")
        self.gridLayout.addWidget(self.sbMasterRotation, 1, 2, 1, 1)
        self.cbSwivelFix = QtWidgets.QCheckBox(self.widget)
        self.cbSwivelFix.setObjectName("cbSwivelFix")
        self.gridLayout.addWidget(self.cbSwivelFix, 5, 1, 1, 1)
        self.cbMFix = QtWidgets.QCheckBox(self.widget)
        self.cbMFix.setObjectName("cbMFix")
        self.gridLayout.addWidget(self.cbMFix, 1, 1, 1, 1)
        self.sbSwivel = QtWidgets.QDoubleSpinBox(self.widget)
        self.sbSwivel.setMinimum(-360.0)
        self.sbSwivel.setMaximum(360.0)
        self.sbSwivel.setSingleStep(10.0)
        self.sbSwivel.setObjectName("sbSwivel")
        self.gridLayout.addWidget(self.sbSwivel, 5, 2, 1, 1)
        self.sbSlaveRotation = QtWidgets.QDoubleSpinBox(self.widget)
        self.sbSlaveRotation.setMinimum(-360.0)
        self.sbSlaveRotation.setMaximum(360.0)
        self.sbSlaveRotation.setSingleStep(10.0)
        self.sbSlaveRotation.setObjectName("sbSlaveRotation")
        self.gridLayout.addWidget(self.sbSlaveRotation, 2, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtWidgets.QSpacerItem(20, 278, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(GeometricConnection)
        QtCore.QMetaObject.connectSlotsByName(GeometricConnection)

    def retranslateUi(self, GeometricConnection):
        GeometricConnection.setWindowTitle(QtWidgets.QApplication.translate("GeometricConnection", "Form", None, -1))
        self.lblInfo_3.setText(QtWidgets.QApplication.translate("GeometricConnection", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connected circles</span></p><p><br/></p></body></html>", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("GeometricConnection", "Parent", None, -1))
        self.lblParent.setText(QtWidgets.QApplication.translate("GeometricConnection", "Parent Circle", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("GeometricConnection", "Child", None, -1))
        self.lblChild.setText(QtWidgets.QApplication.translate("GeometricConnection", "Child circle", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("GeometricConnection", "<html><head/><body><p>Use the node-tree to change parent or child:</p><p>Change parent by dragging this node onto a circle</p><p>Change child by dragging a circle onto this node</p></body></html>", None, -1))
        self.lblInfo.setText(QtWidgets.QApplication.translate("GeometricConnection", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connection type</span></p><p><br/></p></body></html>", None, -1))
        self.rbPinHole.setText(QtWidgets.QApplication.translate("GeometricConnection", "Inside contact (Child circle in parent circle)", None, -1))
        self.rbPinPin.setText(QtWidgets.QApplication.translate("GeometricConnection", "Outside contact (Child circle outside parent circle)", None, -1))
        self.lblInfo_2.setText(QtWidgets.QApplication.translate("GeometricConnection", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connection particulars</span><br/></p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("GeometricConnection", "Parent rotation", None, -1))
        self.cbSFix.setText(QtWidgets.QApplication.translate("GeometricConnection", "Fixed", None, -1))
        self.pbChangeSide.setText(QtWidgets.QApplication.translate("GeometricConnection", "change side", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("GeometricConnection", "Child rotation", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("GeometricConnection", "Swivel", None, -1))
        self.pbFlip.setText(QtWidgets.QApplication.translate("GeometricConnection", "flip", None, -1))
        self.cbSwivelFix.setText(QtWidgets.QApplication.translate("GeometricConnection", "Fixed", None, -1))
        self.cbMFix.setText(QtWidgets.QApplication.translate("GeometricConnection", "Fixed", None, -1))

