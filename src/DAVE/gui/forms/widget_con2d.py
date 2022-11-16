# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_con2d.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_con2d(object):
    def setupUi(self, widget_con2d):
        if not widget_con2d.objectName():
            widget_con2d.setObjectName(u"widget_con2d")
        widget_con2d.resize(343, 408)
        widget_con2d.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_con2d)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(widget_con2d)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.frmMasterSlave = QFrame(widget_con2d)
        self.frmMasterSlave.setObjectName(u"frmMasterSlave")
        self.frmMasterSlave.setFrameShape(QFrame.StyledPanel)
        self.frmMasterSlave.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frmMasterSlave)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widgetSecondary = QNodePicker(self.frmMasterSlave)
        self.widgetSecondary.setObjectName(u"widgetSecondary")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetSecondary.sizePolicy().hasHeightForWidth())
        self.widgetSecondary.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.widgetSecondary, 2, 1, 1, 1)

        self.widgetMain = QNodePicker(self.frmMasterSlave)
        self.widgetMain.setObjectName(u"widgetMain")
        sizePolicy.setHeightForWidth(self.widgetMain.sizePolicy().hasHeightForWidth())
        self.widgetMain.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.widgetMain, 1, 1, 1, 1)

        self.label_9 = QLabel(self.frmMasterSlave)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setMinimumSize(QSize(80, 0))
        self.label_9.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)

        self.label_11 = QLabel(self.frmMasterSlave)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setMinimumSize(QSize(80, 0))
        self.label_11.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.label_11, 2, 0, 1, 1)


        self.verticalLayout.addWidget(self.frmMasterSlave)

        self.frame = QFrame(widget_con2d)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_14 = QLabel(self.frame)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_14)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_2)
        self.formLayout.setObjectName(u"formLayout")
        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.doubleSpinBox_1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_2)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_13)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy2.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy2)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame_3)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_4.setMaximum(99999999999999.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.doubleSpinBox_4)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.label_4)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(widget_con2d)

        QMetaObject.connectSlotsByName(widget_con2d)
    # setupUi

    def retranslateUi(self, widget_con2d):
        widget_con2d.setWindowTitle(QCoreApplication.translate("widget_con2d", u"Form", None))
        self.label.setText(QCoreApplication.translate("widget_con2d", u"2d-connector works on shortest distance and angle between two Frames or Bodies", None))
        self.label_9.setText(QCoreApplication.translate("widget_con2d", u"Main", None))
        self.label_11.setText(QCoreApplication.translate("widget_con2d", u"Secondary", None))
        self.label_14.setText(QCoreApplication.translate("widget_con2d", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Linear stiffness</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("widget_con2d", u"kN/m", None))
        self.label_13.setText(QCoreApplication.translate("widget_con2d", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Angular stiffness</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("widget_con2d", u"kN.m/rad", None))
    # retranslateUi

