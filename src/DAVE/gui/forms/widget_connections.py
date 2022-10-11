# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_connections.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_ConnectionForm(object):
    def setupUi(self, ConnectionForm):
        if not ConnectionForm.objectName():
            ConnectionForm.setObjectName(u"ConnectionForm")
        ConnectionForm.resize(500, 692)
        self.verticalLayout = QVBoxLayout(ConnectionForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(ConnectionForm)
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


        self.retranslateUi(ConnectionForm)

        QMetaObject.connectSlotsByName(ConnectionForm)
    # setupUi

    def retranslateUi(self, ConnectionForm):
        ConnectionForm.setWindowTitle(QCoreApplication.translate("ConnectionForm", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("ConnectionForm", u"Drag items to change order. You can also drag items from the node-tree to add them", None))
        self.pushButton.setText(QCoreApplication.translate("ConnectionForm", u"Add", None))
        self.pbRemoveSelected.setText(QCoreApplication.translate("ConnectionForm", u"Remove selected point", None))
        self.label_3.setText(QCoreApplication.translate("ConnectionForm", u"Connections (Points/Circles)", None))
        self.lbDirection.setText(QCoreApplication.translate("ConnectionForm", u"For circles the direction in which the cable runs over it is defined by the axis of the circle. Check the box to run over the circle in opposite direction.", None))
    # retranslateUi

