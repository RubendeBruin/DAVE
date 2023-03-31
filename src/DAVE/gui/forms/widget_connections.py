# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_connections.ui',
# licensing of 'widget_connections.ui' applies.
#
# Created: Fri Mar 31 15:20:04 2023
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ConnectionForm(object):
    def setupUi(self, ConnectionForm):
        ConnectionForm.setObjectName("ConnectionForm")
        ConnectionForm.resize(500, 692)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConnectionForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(ConnectionForm)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.widgetPicker = QNodePicker(self.frame)
        self.widgetPicker.setObjectName("widgetPicker")
        self.gridLayout.addWidget(self.widgetPicker, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.list = QtWidgets.QListWidget(self.frame)
        self.list.setObjectName("list")
        self.gridLayout.addWidget(self.list, 4, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.pbRemoveSelected = QtWidgets.QPushButton(self.frame)
        self.pbRemoveSelected.setObjectName("pbRemoveSelected")
        self.gridLayout.addWidget(self.pbRemoveSelected, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setWordWrap(True)
        self.label_3.setIndent(-1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.pbSetShortestRoute = QtWidgets.QPushButton(self.frame)
        self.pbSetShortestRoute.setObjectName("pbSetShortestRoute")
        self.gridLayout.addWidget(self.pbSetShortestRoute, 3, 0, 1, 1)
        self.lbDirection = QtWidgets.QLabel(self.frame)
        self.lbDirection.setWordWrap(True)
        self.lbDirection.setObjectName("lbDirection")
        self.gridLayout.addWidget(self.lbDirection, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(ConnectionForm)
        QtCore.QMetaObject.connectSlotsByName(ConnectionForm)

    def retranslateUi(self, ConnectionForm):
        ConnectionForm.setWindowTitle(QtWidgets.QApplication.translate("ConnectionForm", "Form", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("ConnectionForm", "Drag items to change order. You can also drag items from the node-tree to add them", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("ConnectionForm", "Add", None, -1))
        self.pbRemoveSelected.setText(QtWidgets.QApplication.translate("ConnectionForm", "Remove selected point", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("ConnectionForm", "Connections (Points/Circles)", None, -1))
        self.pbSetShortestRoute.setText(QtWidgets.QApplication.translate("ConnectionForm", "Determine shortest route", None, -1))
        self.lbDirection.setText(QtWidgets.QApplication.translate("ConnectionForm", "For circles the direction in which the cable runs over it is defined by the axis of the circle. Check the box to run over the circle in opposite direction.", None, -1))

from DAVE.gui.helpers.qnodepicker import QNodePicker
