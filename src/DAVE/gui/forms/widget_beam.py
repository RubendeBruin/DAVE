# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_beam.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_beam(object):
    def setupUi(self, widget_beam):
        if not widget_beam.objectName():
            widget_beam.setObjectName(u"widget_beam")
        widget_beam.resize(460, 500)
        widget_beam.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_beam)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frmMasterSlave = QFrame(widget_beam)
        self.frmMasterSlave.setObjectName(u"frmMasterSlave")
        self.frmMasterSlave.setFrameShape(QFrame.StyledPanel)
        self.frmMasterSlave.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frmMasterSlave)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sbnSegments = QSpinBox(self.frmMasterSlave)
        self.sbnSegments.setObjectName(u"sbnSegments")
        self.sbnSegments.setMinimum(1)
        self.sbnSegments.setMaximum(1000)

        self.gridLayout_2.addWidget(self.sbnSegments, 4, 1, 1, 1)

        self.label_20 = QLabel(self.frmMasterSlave)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_2.addWidget(self.label_20, 4, 2, 1, 1)

        self.label_9 = QLabel(self.frmMasterSlave)
        self.label_9.setObjectName(u"label_9")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(80, 0))
        self.label_9.setMaximumSize(QSize(9999, 16777215))

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_19 = QLabel(self.frmMasterSlave)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_2.addWidget(self.label_19, 4, 0, 1, 1)

        self.label_11 = QLabel(self.frmMasterSlave)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(80, 0))
        self.label_11.setMaximumSize(QSize(9999, 16777215))

        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)

        self.widgetMain = QNodePicker(self.frmMasterSlave)
        self.widgetMain.setObjectName(u"widgetMain")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetMain.sizePolicy().hasHeightForWidth())
        self.widgetMain.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.widgetMain, 0, 1, 1, 2)

        self.widgetSecondary = QNodePicker(self.frmMasterSlave)
        self.widgetSecondary.setObjectName(u"widgetSecondary")
        sizePolicy1.setHeightForWidth(self.widgetSecondary.sizePolicy().hasHeightForWidth())
        self.widgetSecondary.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.widgetSecondary, 2, 1, 1, 2)


        self.verticalLayout.addWidget(self.frmMasterSlave)

        self.label_7 = QLabel(widget_beam)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_beam)
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
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_3.setDecimals(0)
        self.doubleSpinBox_3.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_3.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 5, 1, 1, 2)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 1, 0, 1, 1)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 4, 3, 1, 1)

        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 6, 3, 1, 1)

        self.sbMass = QDoubleSpinBox(self.frame)
        self.sbMass.setObjectName(u"sbMass")
        self.sbMass.setDecimals(5)
        self.sbMass.setMaximum(999999.000000000000000)
        self.sbMass.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.sbMass, 1, 1, 1, 2)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.label_18 = QLabel(self.frame)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 1, 3, 1, 1)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_1, 0, 1, 1, 2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_2.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 4, 1, 1, 2)

        self.label_14 = QLabel(self.frame)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 5, 3, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_4.setDecimals(0)
        self.doubleSpinBox_4.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_4.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_4, 6, 1, 1, 2)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_5.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_5.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_5.setDecimals(0)
        self.doubleSpinBox_5.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_5.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_5, 2, 1, 1, 2)

        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 2, 3, 1, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.cbTensionOnly = QCheckBox(self.frame)
        self.cbTensionOnly.setObjectName(u"cbTensionOnly")

        self.gridLayout.addWidget(self.cbTensionOnly, 3, 1, 1, 2)


        self.verticalLayout.addWidget(self.frame)

        self.label_8 = QLabel(widget_beam)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.sbnSegments, self.doubleSpinBox_1)
        QWidget.setTabOrder(self.doubleSpinBox_1, self.sbMass)
        QWidget.setTabOrder(self.sbMass, self.doubleSpinBox_5)
        QWidget.setTabOrder(self.doubleSpinBox_5, self.cbTensionOnly)
        QWidget.setTabOrder(self.cbTensionOnly, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)
        QWidget.setTabOrder(self.doubleSpinBox_3, self.doubleSpinBox_4)

        self.retranslateUi(widget_beam)

        QMetaObject.connectSlotsByName(widget_beam)
    # setupUi

    def retranslateUi(self, widget_beam):
        widget_beam.setWindowTitle(QCoreApplication.translate("widget_beam", u"Form", None))
        self.label_20.setText(QCoreApplication.translate("widget_beam", u"[-]", None))
        self.label_9.setText(QCoreApplication.translate("widget_beam", u"Second connection", None))
        self.label_19.setText(QCoreApplication.translate("widget_beam", u"Number of Segments", None))
        self.label_11.setText(QCoreApplication.translate("widget_beam", u"First connection", None))
        self.label_7.setText(QCoreApplication.translate("widget_beam", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Properties (for total beam)</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("widget_beam", u"EIy", None))
        self.label_6.setText(QCoreApplication.translate("widget_beam", u"[m]", None))
        self.label.setText(QCoreApplication.translate("widget_beam", u"Length", None))
        self.label_17.setText(QCoreApplication.translate("widget_beam", u"Mass", None))
        self.label_13.setText(QCoreApplication.translate("widget_beam", u"[kN*m2]", None))
        self.label_15.setText(QCoreApplication.translate("widget_beam", u"[kN*m2]", None))
        self.label_4.setText(QCoreApplication.translate("widget_beam", u"GIp", None))
        self.label_18.setText(QCoreApplication.translate("widget_beam", u"[mT]", None))
        self.label_3.setText(QCoreApplication.translate("widget_beam", u"EIz", None))
        self.label_14.setText(QCoreApplication.translate("widget_beam", u"[kN*m2]", None))
        self.label_16.setText(QCoreApplication.translate("widget_beam", u"[kN]", None))
        self.label_5.setText(QCoreApplication.translate("widget_beam", u"EA", None))
        self.cbTensionOnly.setText(QCoreApplication.translate("widget_beam", u"Tension only", None))
        self.label_8.setText(QCoreApplication.translate("widget_beam", u"<html><head/><body><p>E(steel) is ~210 GPa = 210*10^6 kN/m2</p></body></html>", None))
    # retranslateUi

