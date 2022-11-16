# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_linhyd.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_linhyd(object):
    def setupUi(self, widget_linhyd):
        if not widget_linhyd.objectName():
            widget_linhyd.setObjectName(u"widget_linhyd")
        widget_linhyd.resize(447, 809)
        self.verticalLayout = QVBoxLayout(widget_linhyd)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(widget_linhyd)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_17 = QLabel(self.widget_2)
        self.label_17.setObjectName(u"label_17")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_17)

        self.widgetParent = QNodePicker(self.widget_2)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.widgetParent)


        self.verticalLayout.addWidget(self.widget_2)

        self.frame_2 = QFrame(widget_linhyd)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        self.doubleSpinBox_1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_1.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_1, 1, 1, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setMaximumSize(QSize(16777215, 60))
        self.label_9.setAutoFillBackground(False)
        self.label_9.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 2)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_3.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 3, 1, 1, 1)

        self.label_10 = QLabel(self.frame_2)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMaximumSize(QSize(16777215, 100))
        self.label_10.setAutoFillBackground(False)
        self.label_10.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)

        self.BMT = QDoubleSpinBox(self.frame_2)
        self.BMT.setObjectName(u"BMT")
        self.BMT.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.BMT.setDecimals(3)
        self.BMT.setMinimum(-1000000000000000000.000000000000000)
        self.BMT.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.BMT, 5, 1, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_2.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.COFY = QDoubleSpinBox(self.frame_2)
        self.COFY.setObjectName(u"COFY")
        self.COFY.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.COFY.setDecimals(3)
        self.COFY.setMinimum(-1000000000000000000.000000000000000)
        self.COFY.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.COFY, 10, 1, 1, 1)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.kHeave = QDoubleSpinBox(self.frame_2)
        self.kHeave.setObjectName(u"kHeave")
        self.kHeave.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.kHeave.setDecimals(3)
        self.kHeave.setMinimum(-1000000000000000000.000000000000000)
        self.kHeave.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.kHeave, 12, 1, 1, 1)

        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 18, 0, 1, 1)

        self.COFX = QDoubleSpinBox(self.frame_2)
        self.COFX.setObjectName(u"COFX")
        self.COFX.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.COFX.setDecimals(3)
        self.COFX.setMinimum(-1000000000000000000.000000000000000)
        self.COFX.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.COFX, 8, 1, 1, 1)

        self.label_12 = QLabel(self.frame_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 10, 0, 1, 1)

        self.BML = QDoubleSpinBox(self.frame_2)
        self.BML.setObjectName(u"BML")
        self.BML.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.BML.setDecimals(3)
        self.BML.setMinimum(-1000000000000000000.000000000000000)
        self.BML.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.BML, 6, 1, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        self.label_11.setMaximumSize(QSize(16777215, 100))
        self.label_11.setAutoFillBackground(False)
        self.label_11.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.label_11, 7, 0, 1, 1)

        self.label_13 = QLabel(self.frame_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 12, 0, 1, 1)

        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)
        self.label_16.setMaximumSize(QSize(16777215, 100))
        self.label_16.setAutoFillBackground(False)
        self.label_16.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.label_16, 14, 0, 1, 1)

        self.waterline = QDoubleSpinBox(self.frame_2)
        self.waterline.setObjectName(u"waterline")
        self.waterline.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.waterline.setDecimals(3)
        self.waterline.setMinimum(-1000000000000000000.000000000000000)
        self.waterline.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.waterline, 16, 1, 1, 1)

        self.disp = QDoubleSpinBox(self.frame_2)
        self.disp.setObjectName(u"disp")
        self.disp.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.disp.setDecimals(3)
        self.disp.setMinimum(-1000000000000000000.000000000000000)
        self.disp.setMaximum(999999999999.000000000000000)

        self.gridLayout.addWidget(self.disp, 18, 1, 1, 1)

        self.label_14 = QLabel(self.frame_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.gridLayout.addWidget(self.label_14, 16, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)

        self.retranslateUi(widget_linhyd)

        QMetaObject.connectSlotsByName(widget_linhyd)
    # setupUi

    def retranslateUi(self, widget_linhyd):
        widget_linhyd.setWindowTitle(QCoreApplication.translate("widget_linhyd", u"Form", None))
        self.label_17.setText(QCoreApplication.translate("widget_linhyd", u"Parent", None))
        self.label_2.setText(QCoreApplication.translate("widget_linhyd", u"Y - position", None))
        self.label_9.setText(QCoreApplication.translate("widget_linhyd", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">CoB position</span></p><p>[Defined in parent axis system]</p><p><br/></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("widget_linhyd", u"X - position", None))
        self.label_5.setText(QCoreApplication.translate("widget_linhyd", u"BM-t (heel)", None))
        self.label_10.setText(QCoreApplication.translate("widget_linhyd", u"<html><head/><body><br/><span style=\" font-weight:600; text-decoration: underline;\">Stability</span><br/></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("widget_linhyd", u"Z - position", None))
        self.label_6.setText(QCoreApplication.translate("widget_linhyd", u"BM-l (trim)", None))
        self.label_15.setText(QCoreApplication.translate("widget_linhyd", u"Displacement [kN]", None))
        self.label_12.setText(QCoreApplication.translate("widget_linhyd", u"CoF - Y (relative to CoB)", None))
        self.label_11.setText(QCoreApplication.translate("widget_linhyd", u"<html><head/><body><br/><span style=\" font-weight:600; text-decoration: underline;\">Heave effect</span><br/></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("widget_linhyd", u"Heave stiffness [kN/m]", None))
        self.label_8.setText(QCoreApplication.translate("widget_linhyd", u"CoF - X (relative to CoB)", None))
        self.label_16.setText(QCoreApplication.translate("widget_linhyd", u"<html><head/><body><br/><span style=\" font-weight:600; text-decoration: underline;\">Draft</span><br/></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("widget_linhyd", u"Waterline elevation \n"
"(relative to CoB, usually positive)", None))
    # retranslateUi

