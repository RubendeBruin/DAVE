# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_geometricconnection.ui',
# licensing of 'widget_geometricconnection.ui' applies.
#
# Created: Thu May  7 11:40:14 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_GeometricConnection(object):
    def setupUi(self, GeometricConnection):
        GeometricConnection.setObjectName("GeometricConnection")
        GeometricConnection.resize(238, 523)
        self.verticalLayout = QtWidgets.QVBoxLayout(GeometricConnection)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblInfo = QtWidgets.QLabel(GeometricConnection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInfo.sizePolicy().hasHeightForWidth())
        self.lblInfo.setSizePolicy(sizePolicy)
        self.lblInfo.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblInfo.setAutoFillBackground(False)
        self.lblInfo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblInfo.setObjectName("lblInfo")
        self.verticalLayout.addWidget(self.lblInfo)
        self.cbFlip = QtWidgets.QCheckBox(GeometricConnection)
        self.cbFlip.setObjectName("cbFlip")
        self.verticalLayout.addWidget(self.cbFlip)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(GeometricConnection)
        QtCore.QMetaObject.connectSlotsByName(GeometricConnection)

    def retranslateUi(self, GeometricConnection):
        GeometricConnection.setWindowTitle(QtWidgets.QApplication.translate("GeometricConnection", "Form", None, -1))
        self.lblInfo.setText(QtWidgets.QApplication.translate("GeometricConnection", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Info</span></p></body></html>", None, -1))
        self.cbFlip.setText(QtWidgets.QApplication.translate("GeometricConnection", "Flip ", None, -1))

