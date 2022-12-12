# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_spmt.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_SPMTwidget(object):
    def setupUi(self, SPMTwidget):
        if not SPMTwidget.objectName():
            SPMTwidget.setObjectName(u"SPMTwidget")
        SPMTwidget.resize(278, 638)
        self.gridLayout = QGridLayout(SPMTwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(SPMTwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.label = QLabel(SPMTwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.label_4 = QLabel(SPMTwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 3, 1, 1)

        self.label_2 = QLabel(SPMTwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.sbRefForce = QDoubleSpinBox(SPMTwidget)
        self.sbRefForce.setObjectName(u"sbRefForce")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbRefForce.sizePolicy().hasHeightForWidth())
        self.sbRefForce.setSizePolicy(sizePolicy)
        self.sbRefForce.setLocale(QLocale(QLocale.English, QLocale.World))
        self.sbRefForce.setDecimals(3)
        self.sbRefForce.setMinimum(0.000000000000000)
        self.sbRefForce.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbRefForce, 4, 1, 1, 2)

        self.label_5 = QLabel(SPMTwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 3, 1, 1)

        self.label_6 = QLabel(SPMTwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.sbStiffness = QDoubleSpinBox(SPMTwidget)
        self.sbStiffness.setObjectName(u"sbStiffness")
        sizePolicy.setHeightForWidth(self.sbStiffness.sizePolicy().hasHeightForWidth())
        self.sbStiffness.setSizePolicy(sizePolicy)
        self.sbStiffness.setLocale(QLocale(QLocale.English, QLocale.World))
        self.sbStiffness.setDecimals(3)
        self.sbStiffness.setMinimum(0.000000000000000)
        self.sbStiffness.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbStiffness, 5, 1, 1, 2)

        self.label_8 = QLabel(SPMTwidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 5, 3, 1, 1)

        self.label_9 = QLabel(SPMTwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)

        self.label_11 = QLabel(SPMTwidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 7, 0, 1, 1)

        self.label_14 = QLabel(SPMTwidget)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 7, 3, 1, 1)

        self.label_10 = QLabel(SPMTwidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1)

        self.label_15 = QLabel(SPMTwidget)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 8, 3, 1, 1)

        self.label_13 = QLabel(SPMTwidget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 9, 0, 1, 1)

        self.label_16 = QLabel(SPMTwidget)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 9, 3, 1, 1)

        self.label_12 = QLabel(SPMTwidget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 10, 0, 1, 1)

        self.label_17 = QLabel(SPMTwidget)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 10, 3, 1, 1)

        self.label_18 = QLabel(SPMTwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setWordWrap(True)

        self.gridLayout.addWidget(self.label_18, 11, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 294, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 14, 2, 1, 1)

        self.sbRefExtension = QDoubleSpinBox(SPMTwidget)
        self.sbRefExtension.setObjectName(u"sbRefExtension")
        sizePolicy.setHeightForWidth(self.sbRefExtension.sizePolicy().hasHeightForWidth())
        self.sbRefExtension.setSizePolicy(sizePolicy)
        self.sbRefExtension.setLocale(QLocale(QLocale.English, QLocale.World))
        self.sbRefExtension.setFrame(True)
        self.sbRefExtension.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.sbRefExtension.setDecimals(3)
        self.sbRefExtension.setMinimum(0.000000000000000)
        self.sbRefExtension.setMaximum(10.000000000000000)
        self.sbRefExtension.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.sbRefExtension, 3, 1, 1, 2)

        self.sbDY = QDoubleSpinBox(SPMTwidget)
        self.sbDY.setObjectName(u"sbDY")
        sizePolicy.setHeightForWidth(self.sbDY.sizePolicy().hasHeightForWidth())
        self.sbDY.setSizePolicy(sizePolicy)
        self.sbDY.setLocale(QLocale(QLocale.English, QLocale.World))
        self.sbDY.setDecimals(3)
        self.sbDY.setMinimum(0.000000000000000)
        self.sbDY.setMaximum(100.000000000000000)
        self.sbDY.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.sbDY, 7, 1, 1, 2)

        self.sbDX = QDoubleSpinBox(SPMTwidget)
        self.sbDX.setObjectName(u"sbDX")
        sizePolicy.setHeightForWidth(self.sbDX.sizePolicy().hasHeightForWidth())
        self.sbDX.setSizePolicy(sizePolicy)
        self.sbDX.setLocale(QLocale(QLocale.English, QLocale.World))
        self.sbDX.setDecimals(3)
        self.sbDX.setMinimum(0.000000000000000)
        self.sbDX.setMaximum(100.000000000000000)
        self.sbDX.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.sbDX, 8, 1, 1, 2)

        self.sbNY = QSpinBox(SPMTwidget)
        self.sbNY.setObjectName(u"sbNY")

        self.gridLayout.addWidget(self.sbNY, 9, 1, 1, 2)

        self.sbNX = QSpinBox(SPMTwidget)
        self.sbNX.setObjectName(u"sbNX")

        self.gridLayout.addWidget(self.sbNX, 10, 1, 1, 2)

        self.rbPerpendicular = QRadioButton(SPMTwidget)
        self.rbPerpendicular.setObjectName(u"rbPerpendicular")

        self.gridLayout.addWidget(self.rbPerpendicular, 13, 0, 1, 3)

        self.widget_2 = QWidget(SPMTwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_19 = QLabel(self.widget_2)
        self.label_19.setObjectName(u"label_19")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_19)

        self.widgetParent = QNodePicker(self.widget_2)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.widgetParent)


        self.gridLayout.addWidget(self.widget_2, 0, 0, 1, 3)

        self.rbVertical = QRadioButton(SPMTwidget)
        self.rbVertical.setObjectName(u"rbVertical")
        self.rbVertical.setChecked(True)

        self.gridLayout.addWidget(self.rbVertical, 12, 0, 1, 3)

        self.label_3 = QLabel(SPMTwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)
        self.label_3.setMargin(0)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 4)


        self.retranslateUi(SPMTwidget)

        QMetaObject.connectSlotsByName(SPMTwidget)
    # setupUi

    def retranslateUi(self, SPMTwidget):
        SPMTwidget.setWindowTitle(QCoreApplication.translate("SPMTwidget", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("SPMTwidget", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Hydraulics</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("SPMTwidget", u"Ref. extension", None))
        self.label_4.setText(QCoreApplication.translate("SPMTwidget", u"[m]", None))
        self.label_2.setText(QCoreApplication.translate("SPMTwidget", u"Ref. force", None))
        self.label_5.setText(QCoreApplication.translate("SPMTwidget", u"[kN]", None))
        self.label_6.setText(QCoreApplication.translate("SPMTwidget", u"Stiffness", None))
        self.label_8.setText(QCoreApplication.translate("SPMTwidget", u"[kN/m]", None))
        self.label_9.setText(QCoreApplication.translate("SPMTwidget", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Axles</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("SPMTwidget", u"Spacing width", None))
        self.label_14.setText(QCoreApplication.translate("SPMTwidget", u"[m]", None))
        self.label_10.setText(QCoreApplication.translate("SPMTwidget", u"Spacing length", None))
        self.label_15.setText(QCoreApplication.translate("SPMTwidget", u"[m]", None))
        self.label_13.setText(QCoreApplication.translate("SPMTwidget", u"Number in width", None))
        self.label_16.setText(QCoreApplication.translate("SPMTwidget", u"[-]", None))
        self.label_12.setText(QCoreApplication.translate("SPMTwidget", u"Number in length", None))
        self.label_17.setText(QCoreApplication.translate("SPMTwidget", u"[-]", None))
        self.label_18.setText(QCoreApplication.translate("SPMTwidget", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Friction/Break</span></p></body></html>", None))
        self.rbPerpendicular.setText(QCoreApplication.translate("SPMTwidget", u"Force perp. to contact plane (no friction)", None))
        self.label_19.setText(QCoreApplication.translate("SPMTwidget", u"Parent", None))
        self.rbVertical.setText(QCoreApplication.translate("SPMTwidget", u"Force vertical (friction)", None))
        self.label_3.setText(QCoreApplication.translate("SPMTwidget", u"<html><head/><body>Hydraulic settings are defined by defining an reference force and extension as well as a stiffness.<br>If the SPMT is loaded with a force equal to the reference force then the average extension of the axles is the reference extension.<br/>The stiffness defines the stiffness of the whole SPMT, that is: all axles together.</body></html>", None))
    # retranslateUi

