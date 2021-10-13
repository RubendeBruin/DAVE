# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_component.ui',
# licensing of 'widget_component.ui' applies.
#
# Created: Thu Oct  7 11:20:03 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_component(object):
    def setupUi(self, component):
        component.setObjectName("component")
        component.resize(321, 31)
        component.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(component)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.pbReScan = QtWidgets.QPushButton(component)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbReScan.sizePolicy().hasHeightForWidth())
        self.pbReScan.setSizePolicy(sizePolicy)
        self.pbReScan.setObjectName("pbReScan")
        self.gridLayout.addWidget(self.pbReScan, 1, 2, 1, 1)
        self.cbPath = QtWidgets.QComboBox(component)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbPath.sizePolicy().hasHeightForWidth())
        self.cbPath.setSizePolicy(sizePolicy)
        self.cbPath.setEditable(True)
        self.cbPath.setObjectName("cbPath")
        self.gridLayout.addWidget(self.cbPath, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(component)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.retranslateUi(component)
        QtCore.QMetaObject.connectSlotsByName(component)

    def retranslateUi(self, component):
        component.setWindowTitle(QtWidgets.QApplication.translate("component", "Form", None, -1))
        self.pbReScan.setText(QtWidgets.QApplication.translate("component", "Re-scan", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("component", "File:", None, -1))

