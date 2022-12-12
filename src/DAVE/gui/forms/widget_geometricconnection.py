# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_geometricconnection.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_GeometricConnection(object):
    def setupUi(self, GeometricConnection):
        if not GeometricConnection.objectName():
            GeometricConnection.setObjectName(u"GeometricConnection")
        GeometricConnection.resize(470, 687)
        GeometricConnection.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(GeometricConnection)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lblInfo_3 = QLabel(GeometricConnection)
        self.lblInfo_3.setObjectName(u"lblInfo_3")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInfo_3.sizePolicy().hasHeightForWidth())
        self.lblInfo_3.setSizePolicy(sizePolicy)
        self.lblInfo_3.setMaximumSize(QSize(16777215, 30))
        self.lblInfo_3.setAutoFillBackground(False)
        self.lblInfo_3.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.lblInfo_3)

        self.widget_2 = QWidget(GeometricConnection)
        self.widget_2.setObjectName(u"widget_2")
        self.formLayout = QFormLayout(self.widget_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.lblParent = QLabel(self.widget_2)
        self.lblParent.setObjectName(u"lblParent")
        self.lblParent.setStyleSheet(u"background: lightgray")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lblParent)

        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.lblChild = QLabel(self.widget_2)
        self.lblChild.setObjectName(u"lblChild")
        self.lblChild.setStyleSheet(u"background: lightgray")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lblChild)


        self.verticalLayout.addWidget(self.widget_2)

        self.label_8 = QLabel(GeometricConnection)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout.addWidget(self.label_8)

        self.lblInfo = QLabel(GeometricConnection)
        self.lblInfo.setObjectName(u"lblInfo")
        sizePolicy.setHeightForWidth(self.lblInfo.sizePolicy().hasHeightForWidth())
        self.lblInfo.setSizePolicy(sizePolicy)
        self.lblInfo.setMaximumSize(QSize(16777215, 30))
        self.lblInfo.setAutoFillBackground(False)
        self.lblInfo.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.lblInfo)

        self.rbPinHole = QRadioButton(GeometricConnection)
        self.rbPinHole.setObjectName(u"rbPinHole")

        self.verticalLayout.addWidget(self.rbPinHole)

        self.rbPinPin = QRadioButton(GeometricConnection)
        self.rbPinPin.setObjectName(u"rbPinPin")

        self.verticalLayout.addWidget(self.rbPinPin)

        self.lblInfo_2 = QLabel(GeometricConnection)
        self.lblInfo_2.setObjectName(u"lblInfo_2")
        sizePolicy.setHeightForWidth(self.lblInfo_2.sizePolicy().hasHeightForWidth())
        self.lblInfo_2.setSizePolicy(sizePolicy)
        self.lblInfo_2.setMaximumSize(QSize(16777215, 30))
        self.lblInfo_2.setAutoFillBackground(False)
        self.lblInfo_2.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.lblInfo_2)

        self.widget = QWidget(GeometricConnection)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.cbSFix = QCheckBox(self.widget)
        self.cbSFix.setObjectName(u"cbSFix")

        self.gridLayout.addWidget(self.cbSFix, 2, 1, 1, 1)

        self.pbChangeSide = QPushButton(self.widget)
        self.pbChangeSide.setObjectName(u"pbChangeSide")

        self.gridLayout.addWidget(self.pbChangeSide, 3, 2, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.pbFlip = QPushButton(self.widget)
        self.pbFlip.setObjectName(u"pbFlip")

        self.gridLayout.addWidget(self.pbFlip, 6, 2, 1, 1)

        self.sbMasterRotation = QDoubleSpinBox(self.widget)
        self.sbMasterRotation.setObjectName(u"sbMasterRotation")
        self.sbMasterRotation.setMinimum(-360.000000000000000)
        self.sbMasterRotation.setMaximum(360.000000000000000)
        self.sbMasterRotation.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.sbMasterRotation, 1, 2, 1, 1)

        self.cbSwivelFix = QCheckBox(self.widget)
        self.cbSwivelFix.setObjectName(u"cbSwivelFix")

        self.gridLayout.addWidget(self.cbSwivelFix, 5, 1, 1, 1)

        self.cbMFix = QCheckBox(self.widget)
        self.cbMFix.setObjectName(u"cbMFix")

        self.gridLayout.addWidget(self.cbMFix, 1, 1, 1, 1)

        self.sbSwivel = QDoubleSpinBox(self.widget)
        self.sbSwivel.setObjectName(u"sbSwivel")
        self.sbSwivel.setMinimum(-360.000000000000000)
        self.sbSwivel.setMaximum(360.000000000000000)
        self.sbSwivel.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.sbSwivel, 5, 2, 1, 1)

        self.sbSlaveRotation = QDoubleSpinBox(self.widget)
        self.sbSlaveRotation.setObjectName(u"sbSlaveRotation")
        self.sbSlaveRotation.setMinimum(-360.000000000000000)
        self.sbSlaveRotation.setMaximum(360.000000000000000)
        self.sbSlaveRotation.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.sbSlaveRotation, 2, 2, 1, 1)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 278, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GeometricConnection)

        QMetaObject.connectSlotsByName(GeometricConnection)
    # setupUi

    def retranslateUi(self, GeometricConnection):
        GeometricConnection.setWindowTitle(QCoreApplication.translate("GeometricConnection", u"Form", None))
        self.lblInfo_3.setText(QCoreApplication.translate("GeometricConnection", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connected circles</span></p><p><br/></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("GeometricConnection", u"Parent", None))
        self.lblParent.setText(QCoreApplication.translate("GeometricConnection", u"Parent Circle", None))
        self.label_5.setText(QCoreApplication.translate("GeometricConnection", u"Child", None))
        self.lblChild.setText(QCoreApplication.translate("GeometricConnection", u"Child circle", None))
        self.label_8.setText(QCoreApplication.translate("GeometricConnection", u"<html><head/><body><p>Use the node-tree to change parent or child:</p><p>Change parent by dragging this node onto a circle</p><p>Change child by dragging a circle onto this node</p></body></html>", None))
        self.lblInfo.setText(QCoreApplication.translate("GeometricConnection", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connection type</span></p><p><br/></p></body></html>", None))
        self.rbPinHole.setText(QCoreApplication.translate("GeometricConnection", u"Inside contact (Child circle in parent circle)", None))
        self.rbPinPin.setText(QCoreApplication.translate("GeometricConnection", u"Outside contact (Child circle outside parent circle)", None))
        self.lblInfo_2.setText(QCoreApplication.translate("GeometricConnection", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connection particulars</span><br/></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("GeometricConnection", u"Parent rotation", None))
        self.cbSFix.setText(QCoreApplication.translate("GeometricConnection", u"Fixed", None))
        self.pbChangeSide.setText(QCoreApplication.translate("GeometricConnection", u"change side", None))
        self.label_2.setText(QCoreApplication.translate("GeometricConnection", u"Child rotation", None))
        self.label_3.setText(QCoreApplication.translate("GeometricConnection", u"Swivel", None))
        self.pbFlip.setText(QCoreApplication.translate("GeometricConnection", u"flip", None))
        self.cbSwivelFix.setText(QCoreApplication.translate("GeometricConnection", u"Fixed", None))
        self.cbMFix.setText(QCoreApplication.translate("GeometricConnection", u"Fixed", None))
    # retranslateUi

