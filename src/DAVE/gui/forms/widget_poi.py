# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_poi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_Poi(object):
    def setupUi(self, Poi):
        if not Poi.objectName():
            Poi.setObjectName(u"Poi")
        Poi.resize(350, 241)
        self.verticalLayout = QVBoxLayout(Poi)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Poi)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_8)

        self.widgetParent = QNodePicker(self.widget)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.widgetParent)


        self.verticalLayout.addWidget(self.widget)

        self.label_7 = QLabel(Poi)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setMaximumSize(QSize(16777215, 30))
        self.label_7.setAutoFillBackground(False)
        self.label_7.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_7)

        self.frame_2 = QFrame(Poi)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_2.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 6, 1, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_3.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 7, 1, 1, 1)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        self.doubleSpinBox_1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_1.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_1, 3, 1, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)

        self.retranslateUi(Poi)

        QMetaObject.connectSlotsByName(Poi)
    # setupUi

    def retranslateUi(self, Poi):
        Poi.setWindowTitle(QCoreApplication.translate("Poi", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("Poi", u"Parent", None))
        self.label_7.setText(QCoreApplication.translate("Poi", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Position on parent</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Poi", u"Z - position", None))
        self.label.setText(QCoreApplication.translate("Poi", u"X - position", None))
        self.label_2.setText(QCoreApplication.translate("Poi", u"Y - position", None))
    # retranslateUi

