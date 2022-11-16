# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_body.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(407, 218)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QSize(16777215, 30))
        self.label_7.setAutoFillBackground(False)
        self.label_7.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_7)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_2.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 7, 1, 1, 1)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        self.doubleSpinBox_1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_1.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_1, 4, 1, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)

        self.doubleSpinBox_mass = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_mass.setObjectName(u"doubleSpinBox_mass")
        self.doubleSpinBox_mass.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_mass.setDecimals(3)
        self.doubleSpinBox_mass.setMinimum(0.000000000000000)
        self.doubleSpinBox_mass.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_mass, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_3.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 8, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.doubleSpinBox_mass, self.doubleSpinBox_1)
        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Mass and CoG position</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Mass [mT]", None))
        self.label.setText(QCoreApplication.translate("Form", u"CoG position X", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"CoG position Y", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"CoG position Z", None))
    # retranslateUi

