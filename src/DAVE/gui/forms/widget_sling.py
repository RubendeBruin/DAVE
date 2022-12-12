# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_sling.ui'
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
        Form.resize(427, 397)
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
        self.frame_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.sbDiameter = QDoubleSpinBox(self.frame_2)
        self.sbDiameter.setObjectName(u"sbDiameter")
        self.sbDiameter.setDecimals(3)
        self.sbDiameter.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.sbDiameter, 8, 1, 1, 1)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 9, 0, 1, 1)

        self.sbLength = QDoubleSpinBox(self.frame_2)
        self.sbLength.setObjectName(u"sbLength")
        self.sbLength.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sbLength.setDecimals(3)
        self.sbLength.setMinimum(0.000000000000000)
        self.sbLength.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbLength, 3, 1, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.sbMass = QDoubleSpinBox(self.frame_2)
        self.sbMass.setObjectName(u"sbMass")
        self.sbMass.setDecimals(3)
        self.sbMass.setMaximum(10000.000000000000000)
        self.sbMass.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.sbMass, 9, 1, 1, 1)

        self.sbEA = QDoubleSpinBox(self.frame_2)
        self.sbEA.setObjectName(u"sbEA")
        self.sbEA.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sbEA.setDecimals(1)
        self.sbEA.setMinimum(0.000000000000000)
        self.sbEA.setMaximum(999999999999.000000000000000)
        self.sbEA.setSingleStep(1000.000000000000000)

        self.gridLayout.addWidget(self.sbEA, 6, 1, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)

        self.sbK = QDoubleSpinBox(self.frame_2)
        self.sbK.setObjectName(u"sbK")
        self.sbK.setDecimals(1)
        self.sbK.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbK, 7, 1, 1, 1)

        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 7, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_12)

        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_14)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMaximumSize(QSize(16777215, 30))
        self.label_8.setAutoFillBackground(False)
        self.label_8.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_8)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sbLSpliceA = QDoubleSpinBox(self.frame_3)
        self.sbLSpliceA.setObjectName(u"sbLSpliceA")
        self.sbLSpliceA.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sbLSpliceA.setDecimals(3)
        self.sbLSpliceA.setMinimum(0.000000000000000)
        self.sbLSpliceA.setMaximum(999999999999.000000000000000)
        self.sbLSpliceA.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.sbLSpliceA, 6, 1, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)

        self.sbLEyeA = QDoubleSpinBox(self.frame_3)
        self.sbLEyeA.setObjectName(u"sbLEyeA")
        self.sbLEyeA.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sbLEyeA.setDecimals(3)
        self.sbLEyeA.setMinimum(0.000000000000000)
        self.sbLEyeA.setMaximum(999999999999.000000000000000)
        self.sbLEyeA.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.sbLEyeA, 3, 1, 1, 1)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_3)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMaximumSize(QSize(16777215, 30))
        self.label_9.setAutoFillBackground(False)
        self.label_9.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_9)

        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.sbLSpliceB = QDoubleSpinBox(self.frame_4)
        self.sbLSpliceB.setObjectName(u"sbLSpliceB")
        self.sbLSpliceB.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sbLSpliceB.setDecimals(3)
        self.sbLSpliceB.setMinimum(0.000000000000000)
        self.sbLSpliceB.setMaximum(999999999999.000000000000000)
        self.sbLSpliceB.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.sbLSpliceB, 6, 1, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 3, 0, 1, 1)

        self.sbLEyeB = QDoubleSpinBox(self.frame_4)
        self.sbLEyeB.setObjectName(u"sbLEyeB")
        self.sbLEyeB.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sbLEyeB.setDecimals(3)
        self.sbLEyeB.setMinimum(0.000000000000000)
        self.sbLEyeB.setMaximum(999999999999.000000000000000)
        self.sbLEyeB.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.sbLEyeB, 3, 1, 1, 1)

        self.label_11 = QLabel(self.frame_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 6, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_4)

        QWidget.setTabOrder(self.sbLength, self.sbEA)
        QWidget.setTabOrder(self.sbEA, self.sbK)
        QWidget.setTabOrder(self.sbK, self.sbDiameter)
        QWidget.setTabOrder(self.sbDiameter, self.sbMass)
        QWidget.setTabOrder(self.sbMass, self.sbLEyeA)
        QWidget.setTabOrder(self.sbLEyeA, self.sbLSpliceA)
        QWidget.setTabOrder(self.sbLSpliceA, self.sbLEyeB)
        QWidget.setTabOrder(self.sbLEyeB, self.sbLSpliceB)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Sling properties</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"EA [kN] **", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Mass [mT]", None))
        self.label.setText(QCoreApplication.translate("Form", u"Total length [m] *", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Diameter [m]", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Total stiffness [kN/m]", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"* Total length is measured between the insides of the eyes", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"** EA is the stiffness of the wire", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">End A</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Length eye (inside) [m]", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Length splice [m]", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">End B</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Length eye (inside) [m]", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Length splice [m]", None))
    # retranslateUi

