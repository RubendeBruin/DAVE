# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_cable.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_Cable_form(object):
    def setupUi(self, Cable_form):
        if not Cable_form.objectName():
            Cable_form.setObjectName(u"Cable_form")
        Cable_form.resize(299, 690)
        Cable_form.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(Cable_form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(Cable_form)
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

        self.frame_2 = QFrame(Cable_form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        self.doubleSpinBox_1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_1.setMaximum(999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(0.000000000000000)
        self.doubleSpinBox_2.setMaximum(999999999999.000000000000000)
        self.doubleSpinBox_2.setSingleStep(1000.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.doubleSpinBox = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setSingleStep(0.001000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setSingleStep(0.001000000000000)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.doubleSpinBox_3)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_9)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMaximum(999999.000000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.doubleSpinBox_4)


        self.verticalLayout.addWidget(self.frame_2)

        self.label_6 = QLabel(Cable_form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_6)

        self.frame = QFrame(Cable_form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widgetPicker = QNodePicker(self.frame)
        self.widgetPicker.setObjectName(u"widgetPicker")

        self.gridLayout.addWidget(self.widgetPicker, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.list = QListWidget(self.frame)
        self.list.setObjectName(u"list")

        self.gridLayout.addWidget(self.list, 4, 0, 1, 2)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.pbRemoveSelected = QPushButton(self.frame)
        self.pbRemoveSelected.setObjectName(u"pbRemoveSelected")

        self.gridLayout.addWidget(self.pbRemoveSelected, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)
        self.label_3.setIndent(-1)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)

        self.lbDirection = QLabel(self.frame)
        self.lbDirection.setObjectName(u"lbDirection")
        self.lbDirection.setWordWrap(True)

        self.gridLayout.addWidget(self.lbDirection, 5, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame)

        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)

        self.retranslateUi(Cable_form)

        QMetaObject.connectSlotsByName(Cable_form)
    # setupUi

    def retranslateUi(self, Cable_form):
        Cable_form.setWindowTitle(QCoreApplication.translate("Cable_form", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("Cable_form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Cable properties</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Cable_form", u"Length at rest [m]", None))
        self.label_2.setText(QCoreApplication.translate("Cable_form", u"Stiffness EA [kN]", None))
        self.label_4.setText(QCoreApplication.translate("Cable_form", u"Diameter [m]", None))
        self.label_5.setText(QCoreApplication.translate("Cable_form", u"Mass per length [mT/m] *", None))
        self.label_9.setText(QCoreApplication.translate("Cable_form", u"Mass [mT]", None))
        self.label_6.setText(QCoreApplication.translate("Cable_form", u"* Intended for lift-rigging calculations. Mass is only accurately accounted for when cable is tension exceeds its own weight. Mass is calculated from mass_per_length.", None))
        self.label_8.setText(QCoreApplication.translate("Cable_form", u"Drag items to change order. You can also drag items from the node-tree to add them", None))
        self.pushButton.setText(QCoreApplication.translate("Cable_form", u"Add", None))
        self.pbRemoveSelected.setText(QCoreApplication.translate("Cable_form", u"Remove selected point", None))
        self.label_3.setText(QCoreApplication.translate("Cable_form", u"A cable connects points/circles nodes.", None))
        self.lbDirection.setText(QCoreApplication.translate("Cable_form", u"For circles the direction in which the cable runs over it is defined by the axis of the circle. Check the box to run over the circle in opposite direction.", None))
    # retranslateUi

