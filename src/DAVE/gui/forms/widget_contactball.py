# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_contactball.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_contactball(object):
    def setupUi(self, widget_contactball):
        if not widget_contactball.objectName():
            widget_contactball.setObjectName(u"widget_contactball")
        widget_contactball.resize(353, 418)
        widget_contactball.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_contactball)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(widget_contactball)
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

        self.label_7 = QLabel(widget_contactball)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_contactball)
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

        self.sbR = QDoubleSpinBox(self.frame)
        self.sbR.setObjectName(u"sbR")
        sizePolicy2.setHeightForWidth(self.sbR.sizePolicy().hasHeightForWidth())
        self.sbR.setSizePolicy(sizePolicy2)
        self.sbR.setDecimals(3)
        self.sbR.setMinimum(0.000000000000000)
        self.sbR.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sbR)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.sbK = QDoubleSpinBox(self.frame)
        self.sbK.setObjectName(u"sbK")
        sizePolicy2.setHeightForWidth(self.sbK.sizePolicy().hasHeightForWidth())
        self.sbK.setSizePolicy(sizePolicy2)
        self.sbK.setDecimals(3)
        self.sbK.setMinimum(0.000000000000000)
        self.sbK.setMaximum(99999999999999.000000000000000)
        self.sbK.setSingleStep(100.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sbK)


        self.verticalLayout.addWidget(self.frame)

        self.label_9 = QLabel(widget_contactball)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_9)

        self.lwMeshes = QListWidget(widget_contactball)
        self.lwMeshes.setObjectName(u"lwMeshes")
        self.lwMeshes.setAcceptDrops(True)

        self.verticalLayout.addWidget(self.lwMeshes)

        self.pbRemoveSelected = QPushButton(widget_contactball)
        self.pbRemoveSelected.setObjectName(u"pbRemoveSelected")

        self.verticalLayout.addWidget(self.pbRemoveSelected)

        QWidget.setTabOrder(self.sbR, self.sbK)

        self.retranslateUi(widget_contactball)

        QMetaObject.connectSlotsByName(widget_contactball)
    # setupUi

    def retranslateUi(self, widget_contactball):
        widget_contactball.setWindowTitle(QCoreApplication.translate("widget_contactball", u"Form", None))
        self.label_13.setText(QCoreApplication.translate("widget_contactball", u"Parent", None))
        self.label_7.setText(QCoreApplication.translate("widget_contactball", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Ball</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("widget_contactball", u"Radius [m]", None))
        self.label_2.setText(QCoreApplication.translate("widget_contactball", u"Stiffness [kN/m]", None))
        self.label_9.setText(QCoreApplication.translate("widget_contactball", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Meshes</span></p><p>Meshes that this ball can make contact with need to be listed here explicitly</p><p>To add meshes, drag and drop them from the node-tree</p><p><br/></p></body></html>", None))
        self.pbRemoveSelected.setText(QCoreApplication.translate("widget_contactball", u"remove selected point", None))
    # retranslateUi

