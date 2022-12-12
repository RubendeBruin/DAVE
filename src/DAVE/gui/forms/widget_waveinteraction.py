# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_waveinteraction.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_waveinteraction(object):
    def setupUi(self, widget_waveinteraction):
        if not widget_waveinteraction.objectName():
            widget_waveinteraction.setObjectName(u"widget_waveinteraction")
        widget_waveinteraction.resize(444, 314)
        widget_waveinteraction.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_waveinteraction)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(widget_waveinteraction)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_13 = QLabel(self.widget_2)
        self.label_13.setObjectName(u"label_13")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_13)

        self.widgetParent = QNodePicker(self.widget_2)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.widgetParent)


        self.verticalLayout.addWidget(self.widget_2)

        self.label_12 = QLabel(widget_waveinteraction)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_12)

        self.comboBox = QComboBox(widget_waveinteraction)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(True)

        self.verticalLayout.addWidget(self.comboBox)

        self.widget = QWidget(widget_waveinteraction)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(361, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pbRescan = QPushButton(self.widget)
        self.pbRescan.setObjectName(u"pbRescan")

        self.horizontalLayout.addWidget(self.pbRescan)


        self.verticalLayout.addWidget(self.widget)

        self.label_7 = QLabel(widget_waveinteraction)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_waveinteraction)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_2.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_3.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox_3)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.HLine)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.frame_2)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.HLine)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.frame_6)


        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 163, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(widget_waveinteraction)

        QMetaObject.connectSlotsByName(widget_waveinteraction)
    # setupUi

    def retranslateUi(self, widget_waveinteraction):
        widget_waveinteraction.setWindowTitle(QCoreApplication.translate("widget_waveinteraction", u"Form", None))
        self.label_13.setText(QCoreApplication.translate("widget_waveinteraction", u"Parent", None))
        self.label_12.setText(QCoreApplication.translate("widget_waveinteraction", u"<html><head/><body><p>Wave-Interaction</p><p><br/>Hydrodynamic data can be read from a .dhyd or .hyd file.</p></body></html>", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("widget_waveinteraction", u"wirecube.obj", None))

        self.pbRescan.setText(QCoreApplication.translate("widget_waveinteraction", u"Rescan resources", None))
        self.label_7.setText(QCoreApplication.translate("widget_waveinteraction", u"<html><head/><body><p><span style=\" font-weight:600;\">Location of the hydrodynamic origin</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("widget_waveinteraction", u"X - offset", None))
        self.label_2.setText(QCoreApplication.translate("widget_waveinteraction", u"Y - offset", None))
        self.label_3.setText(QCoreApplication.translate("widget_waveinteraction", u"Z - offset", None))
    # retranslateUi

