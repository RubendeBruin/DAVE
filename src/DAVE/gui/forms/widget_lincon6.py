# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_lincon6.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_lincon6(object):
    def setupUi(self, widget_lincon6):
        if not widget_lincon6.objectName():
            widget_lincon6.setObjectName(u"widget_lincon6")
        widget_lincon6.resize(458, 637)
        widget_lincon6.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_lincon6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(widget_lincon6)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_8)

        self.frmMasterSlave = QFrame(widget_lincon6)
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

        self.label_7 = QLabel(widget_lincon6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_lincon6)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_1, 0, 2, 1, 2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_2.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 2, 1, 2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_3.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 2, 2, 1, 2)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.HLine)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_2, 3, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.HLine)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_3, 3, 1, 1, 2)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.HLine)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_4, 3, 3, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_4.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_4, 4, 2, 1, 2)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_5.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_5.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_5.setDecimals(3)
        self.doubleSpinBox_5.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_5.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_5, 5, 2, 1, 2)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.doubleSpinBox_6 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_6.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_6.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_6.setDecimals(3)
        self.doubleSpinBox_6.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_6.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_6, 6, 2, 1, 2)


        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(widget_lincon6)

        QMetaObject.connectSlotsByName(widget_lincon6)
    # setupUi

    def retranslateUi(self, widget_lincon6):
        widget_lincon6.setWindowTitle(QCoreApplication.translate("widget_lincon6", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("widget_lincon6", u"<html><head/><body><p>Stiffness are defined relative to the reference system of Main</p><p>Rotations are the projected rotations: For example rotation about Z is the arc-tan of the x and and y-components of the x-unit vector of secondary expressed in the coordinate system of main.</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("widget_lincon6", u"Main", None))
        self.label_11.setText(QCoreApplication.translate("widget_lincon6", u"Secondary", None))
        self.label_7.setText(QCoreApplication.translate("widget_lincon6", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Stiffness</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("widget_lincon6", u"X - translation [kN/m]", None))
        self.label_2.setText(QCoreApplication.translate("widget_lincon6", u"Y - translation", None))
        self.label_3.setText(QCoreApplication.translate("widget_lincon6", u"Z - translation", None))
        self.label_4.setText(QCoreApplication.translate("widget_lincon6", u"X-rotation [kNm/rad]", None))
        self.label_5.setText(QCoreApplication.translate("widget_lincon6", u"Y-rotation", None))
        self.label_6.setText(QCoreApplication.translate("widget_lincon6", u"Z-rotation", None))
    # retranslateUi

